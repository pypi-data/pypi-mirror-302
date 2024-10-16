import contextlib
import ctypes
import logging.config
import platform
import warnings
from typing import Optional, assert_never

import tblib.pickling_support

from caqtus.experiment_control.manager import (
    LocalExperimentManager,
    RemoteExperimentManagerClient,
    RemoteExperimentManagerServer,
)

# noinspection PyProtectedMember
from caqtus.gui.condetrol._condetrol import Condetrol
from caqtus.session.sql import PostgreSQLConfig, PostgreSQLExperimentSessionMaker
from ._caqtus_extension import CaqtusExtension
from .device_extension import DeviceExtension
from .time_lane_extension import TimeLaneExtension
from ..device.configuration import DeviceServerName
from ..device.remote import Server, RPCConfiguration
from ..experiment_control import ExperimentManager
from ..experiment_control.manager import (
    ExperimentManagerConnection,
    LocalExperimentManagerConfiguration,
    RemoteExperimentManagerConfiguration,
)
from ..experiment_control.sequence_execution import ShotRetryConfig
from ..session import ExperimentSessionMaker, ExperimentSession
from ..session.sql._session_maker import (
    SQLiteConfig,
    SQLiteExperimentSessionMaker,
    SQLExperimentSessionMaker,
)


class Experiment:
    """Configure parameters and register extensions for a specific experiment.

    There should be only a single instance of this class in the entire application.
    It is used to configure the experiment and knows how to launch the different
    components of the application after it has been configured.
    """

    def __init__(self) -> None:
        self._session_maker_config: Optional[PostgreSQLConfig | SQLiteConfig] = None
        self._extension = CaqtusExtension()
        self._experiment_manager: Optional[LocalExperimentManager] = None
        self._experiment_manager_location: ExperimentManagerConnection = (
            LocalExperimentManagerConfiguration()
        )
        self._shot_retry_config: Optional[ShotRetryConfig] = None

    def setup_default_extensions(self) -> None:
        """Register some commonly used extensions to this experiment.

        This method registers the following extensions:

        * digital time lanes
        * analog time lanes
        * camera time lanes
        """

        from caqtus.extension.time_lane_extension import (
            digital_time_lane_extension,
            analog_time_lane_extension,
            camera_time_lane_extension,
        )

        self.register_time_lane_extension(digital_time_lane_extension)
        self.register_time_lane_extension(analog_time_lane_extension)
        self.register_time_lane_extension(camera_time_lane_extension)

    def configure_storage(
        self, backend_config: PostgreSQLConfig | SQLiteConfig
    ) -> None:
        """Configure the storage backend to be used by the application.

        After this method is called, the application will read and write data and
        configurations to the storage specified.

        It is necessary to call this method before launching the application.

        Warning:
            Calling this method multiple times will overwrite the previous
            configuration.
        """

        if self._session_maker_config is not None:
            warnings.warn("Storage configuration is being overwritten.", stacklevel=2)
        self._session_maker_config = backend_config

    def configure_shot_retry(
        self, shot_retry_config: Optional[ShotRetryConfig]
    ) -> None:
        """Configure the shot retry policy to be used when running sequences.

        After this method is called, shots that raise errors will be retried according
        to the policy specified.

        It is necessary to call this method before launching the experiment manager.

        Warning:
            Calling this method multiple times will overwrite the previous
            configuration.
        """

        self._shot_retry_config = shot_retry_config

    def configure_experiment_manager(
        self, location: ExperimentManagerConnection
    ) -> None:
        """Configure the location of the experiment manager with respect to Condetrol.

        The :class:`ExperimentManager` is responsible for running sequences on the
        experiment.

        It can be either running in the same process as the Condetrol application or in
        a separate process.

        This is configured by passing an instance of either
        :class:`LocalExperimentManagerConfiguration` or
        :class:`RemoteExperimentManagerConfiguration`.

        If this method is not called, the experiment manager will be assumed to be
        running in the same local process as the Condetrol application.

        If the experiment manager is configured to run in the same process, it will be
        created when the Condetrol application is launched.
        An issue with this approach is that if the Condetrol application crashes, the
        experiment manager will also stop abruptly, potentially leaving the experiment
        in an undesired state.

        If the experiment manager is configured to run in a separate process, it will be
        necessary to have an experiment manager server running before launching the
        Condetrol application.
        The Condetrol application will then connect to the server and transmit the
        commands to the other process.
        If the Condetrol application crashes, the experiment manager will be unaffected.

        Warning:
            Calling this method multiple times will overwrite the previous
            configuration.
        """

        self._experiment_manager_location = location

    def register_device_extension(self, device_extension: DeviceExtension) -> None:
        """Register a new device extension.

        After this method is called, the device extension will be available to the
        application, both in the device editor tab in Condetrol and while running the
        experiment.
        """

        self._extension.register_device_extension(device_extension)

    def register_time_lane_extension(
        self, time_lane_extension: TimeLaneExtension
    ) -> None:
        """Register a new time lane extension.

        After this method is called, the time lane extension will be available to the
        application, both in the time lane editor tab in Condetrol and while running the
        experiment.
        """

        self._extension.register_time_lane_extension(time_lane_extension)

    def register_device_server(
        self, name: DeviceServerName, config: RPCConfiguration
    ) -> None:
        """Register a new device server.

        After this method is called, the device server will be available to the
        application to connect to devices.
        """

        self._extension.register_device_server_config(name, config)

    def get_session_maker(self) -> ExperimentSessionMaker:
        """Get the session maker to be used by the application.

        The session maker is responsible for interacting with the storage of the
        experiment.

        The method :meth:`configure_storage` must be called before this method.
        """

        return self._get_session_maker(check_schema=True)

    def _get_session_maker(self, check_schema: bool = True) -> ExperimentSessionMaker:
        if self._session_maker_config is None:
            error = RuntimeError("Storage configuration has not been set.")
            error.add_note(
                "Call `configure_storage` with the appropriate configuration."
            )
            raise error
        if isinstance(self._session_maker_config, SQLiteConfig):
            session_maker = self._extension.create_session_maker(
                SQLiteExperimentSessionMaker,
                config=self._session_maker_config,
            )
        elif isinstance(self._session_maker_config, PostgreSQLConfig):
            session_maker = self._extension.create_session_maker(
                PostgreSQLExperimentSessionMaker,
                config=self._session_maker_config,
            )
        else:
            assert_never(self._session_maker_config)
        if check_schema:
            session_maker.check()
        return session_maker

    def connect_to_experiment_manager(self) -> ExperimentManager:
        """Connect to the experiment manager."""

        location = self._experiment_manager_location
        if isinstance(location, LocalExperimentManagerConfiguration):
            return self.get_local_experiment_manager()
        elif isinstance(location, RemoteExperimentManagerConfiguration):
            client = RemoteExperimentManagerClient(
                address=(location.address, location.port),
                authkey=bytes(location.authkey, "utf-8"),
            )
            return client.get_experiment_manager()
        else:
            assert_never(location)

    def get_local_experiment_manager(self) -> LocalExperimentManager:
        """Return the local experiment manager.

        This method is used to create an instance of the experiment manager that runs
        in the local process.

        The first time this method is called, the experiment manager will be created.
        If it is called again, the instance previously created will be returned.
        """

        if self._experiment_manager is None:
            self._experiment_manager = LocalExperimentManager(
                session_maker=self.get_session_maker(),
                device_manager_extension=self._extension.device_manager_extension,
                shot_retry_config=self._shot_retry_config,
            )
        return self._experiment_manager

    def launch_condetrol(self) -> None:
        """Launch the Condetrol application.

        The Condetrol application is the main user interface to the experiment.
        It allows to edit and launch sequences, as well as edit the device
        configurations.
        """

        setup_logs("caqtus.log")

        tblib.pickling_support.install()

        if platform.system() == "Windows":
            # This is necessary to use the UI icon in the taskbar and not the default
            # Python icon.
            app_id = "caqtus.condetrol"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        app = Condetrol(
            self.get_session_maker(),
            extension=self._extension.condetrol_extension,
            connect_to_experiment_manager=self.connect_to_experiment_manager,
        )
        try:
            app.run()
        except:
            logging.exception("An error occurred.", exc_info=True)
            raise

    def launch_experiment_server(self) -> None:
        """Launch the experiment server.

        The experiment server is used to run procedures on the experiment manager from a
        remote process.
        """

        setup_logs("experiment_server.log")

        tblib.pickling_support.install()

        if platform.system() == "Windows":
            # This is necessary to use the UI icon in the taskbar and not the default
            # Python icon.
            app_id = "caqtus.experiment_server"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        if not isinstance(
            self._experiment_manager_location, RemoteExperimentManagerConfiguration
        ):
            error = RuntimeError(
                "The experiment manager is not configured to run remotely."
            )
            error.add_note(
                "Please call `configure_experiment_manager` with a remote "
                "configuration."
            )
            raise error

        server = RemoteExperimentManagerServer(
            session_maker=self.get_session_maker(),
            address=("localhost", self._experiment_manager_location.port),
            authkey=bytes(self._experiment_manager_location.authkey, "utf-8"),
            shot_retry_config=self._shot_retry_config,
            device_manager_extension=self._extension.device_manager_extension,
        )

        with server:
            print("Ready")
            server.serve_forever()

    @staticmethod
    def launch_device_server(
        config: RPCConfiguration, name: str = "device_server"
    ) -> None:
        """Launch a device server in the current process.

        This method will block until the server is stopped.

        Args:
            config: The configuration of the server.
            name: The name of the server. It is used to create the log file.
        """

        setup_logs(f"{name}.log")

        tblib.pickling_support.install()

        if platform.system() == "Windows":
            # This is necessary to use the UI icon in the taskbar and not the default
            # Python icon.
            app_id = "caqtus.device_server"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

        with Server(config) as server:
            print("Ready")
            server.wait_for_termination()

    def storage_session(self) -> contextlib.AbstractContextManager[ExperimentSession]:
        """Return a context manager that provides a session to the storage backend.

        A session can be used to access the data stored in the experiment.
        """

        return self.get_session_maker().session()


def upgrade_database(experiment: Experiment) -> None:
    """Upgrade the database schema of the experiment to the latest version.

    .. Warning::

        It is strongly recommended to back up the database before running this
        function in case something goes wrong.

    Args:
        experiment: The experiment to upgrade the database for.
            It must have been configured with a PostgreSQL storage backend.
    """

    session_maker = experiment._get_session_maker(check_schema=False)
    if not isinstance(session_maker, SQLExperimentSessionMaker):
        error = RuntimeError("The session maker is not a SQL session maker.")
        error.add_note(
            "The upgrade_database method is only available for SQL session makers."
        )
        raise error
    session_maker.upgrade()


def stamp_database(experiment: Experiment) -> None:
    """Mark old databases schema with the original revision.

    This should only be called on databases that were created before version 6.3.0.
    """

    from alembic.command import stamp

    session_maker = experiment._get_session_maker(check_schema=False)
    if not isinstance(session_maker, PostgreSQLExperimentSessionMaker):
        raise RuntimeError("The session maker is not a PostgreSQL session maker.")
    config = session_maker._get_alembic_config()

    stamp(config, "038164d73465")


def setup_logs(file_name: str):
    log_config = {
        "version": 1,
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "warnings": {
                "level": "WARNING",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "errors": {
                "level": "ERROR",
                "formatter": "standard",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": file_name,
                "maxBytes": 1_000_000,
            },
        },
        "loggers": {
            "": {"level": "INFO", "handlers": ["default", "warnings", "errors"]},
            "alembic": {
                "level": "WARNING",
                "handlers": ["default", "warnings", "errors"],
            },
        },
    }

    logging.config.dictConfig(log_config)
