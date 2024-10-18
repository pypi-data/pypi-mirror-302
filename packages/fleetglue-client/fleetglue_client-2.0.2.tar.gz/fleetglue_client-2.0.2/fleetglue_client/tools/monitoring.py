import time
import logging
from threading import Thread
from typing import Callable

from fleetglue_client.api_handler import APIError, UnauthorizedError
from fleetglue_client.account import Account

top_logger = logging.getLogger(__name__)


class MonitorThread(Thread):

    def __init__(
        self,
        service: str,
        service_id: int,
        account: Account,
        data_callback: Callable,
        sleep_time: int = 1,
        logger=None,
        **extra_args,
    ):
        super().__init__()
        self.service = service
        self.account = account
        self.sleep_time = sleep_time
        self.data_callback = data_callback
        self.is_alive = False
        self.extra_args = extra_args
        self.logger = top_logger
        if logger:
            self.logger = logger

    def run(self):
        self.is_alive = True
        callback_retries = 0

        while self.is_alive:
            try:
                data = self.data_callback()
                if not isinstance(data, dict):
                    self.logger.error(
                        f"Invalid callback result of type `{type(data)}` "
                        f"should be dict instead. Stopping monitor thread",
                        exc_info=True,
                    )
                    break
                # Adding extra information to message
                data.update(self.extra_args)
                callback_retries = 0  # Reset retries count
            except Exception as e:
                callback_retries += 1
                if callback_retries == 6:
                    self.logger.error(
                        "Callback failed too many times consequentially. Stopping monitor thread"
                    )
                    break
                else:
                    self.logger.warning(
                        f"Error while executing callback: {e}", exc_info=True
                    )
                    time.sleep(1)
                    continue

            # Pushing monitoring data to API
            try:
                self.account.put_monitoring(self.service, data)
                self.logger.debug(f"Sent monitoring details: {data}")
                time.sleep(self.sleep_time)
            except UnauthorizedError:
                self.logger.error(
                    "Unauthorized to send monitoring data. Finishing monitor thread"
                )
                break
            except APIError as e:
                self.logger.warning(f"Received APIError {e}")
                time.sleep(1)

        self.stop()

    def stop(self):
        global monitor_thread
        self.is_alive = False
        # If current monitor thread is the global one, remove it
        if monitor_thread == self:
            monitor_thread = None


monitor_thread = None


def initialize_monitoring(
    service: str, service_id: int, account: Account, data_callback: Callable, **kwargs
):
    """Starts a monitoring thread that will upload details for the current
    service status to the API.

    Parameters:
        service (str): The service or application name.
        service_id (int): The service id (in case it have multiple instances)
        account (Account): The Account instance to use for connecting with the API.
        data_callback (Callable): The callback that will generate the monitoring data.
        **kwargs: Extra keyword arguments for MonitorThread.
    """
    global monitor_thread
    if monitor_thread is not None:
        raise MonitoringError(
            "Monitor thread is already running, cannot create a new instance"
        )

    monitor_thread = MonitorThread(
        service, service_id, account, data_callback, **kwargs
    )
    monitor_thread.start()


def stop_monitoring():
    global monitor_thread
    if monitor_thread is None:
        raise MonitoringError("There is no monitor thread running")

    monitor_thread.stop()
    monitor_thread.join()


class MonitoringError(Exception):
    pass
