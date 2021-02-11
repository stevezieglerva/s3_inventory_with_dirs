import unittest
from datetime import datetime
from queue import Queue
from threading import Thread
from unittest.mock import MagicMock, Mock, PropertyMock, patch

from ThreadWorker import ThreadWorker


class ThreadWorkerUnitTests(unittest.TestCase):
    def test_run__given_multiple_thread__no_exceptions(self):
        start = datetime.now()
        # Arrange
        queue = Queue()
        # Create 8 worker threads
        for x in range(3):
            worker = ThreadWorker(queue)
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            worker.start()

        # Act
        for path in [
            "failed",
            "intake",
            "inventory",
            "failed",
            "nixplay",
            "original-backup",
            "original",
            "processed",
            "raw-photos",
            "shuffle",
            "small",
            "thumbnail",
        ]:
            queue.put(f"{path}")
        queue.join()

        # Assert
        end = datetime.now()
        print(start)
        print(end)
        delta = end - start
        delta = end - start
        print(f"\n\n\n***********\n\nDuration: {delta.seconds}\n\n\n")
        with open("thread_timing_results.txt", "a") as file:
            file.write(f"{end} multiple threads: {delta.seconds}\n")

    def test_run__given_one_thread__no_exceptions(self):
        start = datetime.now()
        # Arrange
        queue = Queue()
        # Create 8 worker threads
        for x in range(3):
            worker = ThreadWorker(queue)
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            worker.start()

        # Act
        queue.put("")
        queue.join()

        # Assert
        end = datetime.now()
        print("\n_____\nResults:")
        print(start)
        print(end)
        delta = end - start
        print(f"\n\n\n***********\n\nDuration: {delta.seconds}\n\n\n")
        with open("thread_timing_results.txt", "a") as file:
            file.write(f"{end} one thread: {delta.seconds}\n")


if __name__ == "__main__":
    unittest.main()
