"""Main module."""
import time
import redis
import struct

from .exceptions import TooLateError


class ProcSync:
    """

    """

    def __init__(self, redis_client: redis.Redis, run_id: str = "", delay: float = 1.0):
        """

        :param redis_client: A `redis.Redis` instance that's connected to a redis server.
        :param run_id: An arbitrary id (str) that identifies this specific run. (Should be unique across all runs)
        :param delay: Time spent waiting after the continue time is announced. (Default is 1 sec)
        """
        self._delay = delay
        self._nodewait_key_prefix = f"nodewait:{run_id}:"
        self._continue_channel_prefix = f"continue:{run_id}:"

        # setup redis
        self._redis_client = redis_client
        self._redis_pubsub = self._redis_client.pubsub()
        self._redis_pubsub.psubscribe(self._continue_channel_prefix + "*")

    @staticmethod
    def _sleep_until(timestamp: float):
        # Catching the exception is a little faster then checking it with an if (see. perf_tests)
        # (that's what happens internally anyways)
        # But only when there isn't an exception. If the result is negative for some reason,
        # than this is is actually slower
        try:
            time.sleep(timestamp - time.time())  # TODO: use a precision timer
        except ValueError:  # sleep length must be non-negative error
            raise TooLateError(
                """Syncronization time have already expired.
                This could be caused by high network latency or unsynchronized system clocks.
                Try increasing delay."""
            )

    def sync(self, event_name: str, nodes: int):
        """
        Start waiting for a syncronize

        The function returns at the same time (according to system clock) on all nodes.

        :param event_name: The name of the event. This should be the same across all nodes that want to synchronize.
        :param nodes: Amount of nodes to sync the event between.
        """
        nodewait_key = (self._nodewait_key_prefix + event_name).encode()
        continue_channel = (self._continue_channel_prefix + event_name).encode()

        if self._redis_client.incr(nodewait_key) >= nodes:
            # this was the last node, announcing continue time
            cont_time = time.time() + self._delay  # each client have _delay seconds to receive sync time and prepare

            # struct packing faster than using strings (see. perf_tests)
            self._redis_client.publish(continue_channel, struct.pack("!d", cont_time))
            self._redis_client.expire(nodewait_key, int(self._delay) + 1)  # Rounding up without ceil()

        # waiting for continue time to be announced (this will consume the message emitted above as well)
        while True:
            cont_message = self._redis_pubsub.get_message(ignore_subscribe_messages=True, timeout=0.1)
            if cont_message and cont_message['channel'] == continue_channel:
                cont_time = struct.unpack("!d", cont_message['data'])[0]  # Using struct is a lot faster than strings
                break

        self._sleep_until(cont_time)

    def close(self):
        """
        Close Redis connection.
        After calling this method. The instance should not be used anymore.
        """
        self._redis_pubsub.close()
        self._redis_client.close()
