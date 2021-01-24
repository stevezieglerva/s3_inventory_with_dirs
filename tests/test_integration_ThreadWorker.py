import unittest
from queue import Queue
from threading import Thread
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from ThreadWorker import ThreadWorker


class ThreadWorkerUnitTests(unittest.TestCase):
    def test_run__given_simple_cases__no_exceptions(self):
        # Arrange
        queue = Queue()
        # Create 8 worker threads
        for x in range(3):
            worker = ThreadWorker(queue)
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            worker.start()

        # Act
        queue.put("failed/2017")
        queue.join()

        # Assert


if __name__ == "__main__":
    unittest.main()
