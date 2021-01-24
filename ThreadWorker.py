from queue import Queue
from threading import Thread
from S3Inventory import S3Inventory


class ThreadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            value = self.queue.get()
            try:
                s3 = S3Inventory(
                    "svz-master-pictures-new",
                )
                print(f"\n\n\n*** Getting inventory from: {value}")
                inventory_file_suffix = value.replace("/", "__")
                s3.create_inventory(
                    "svz-master-pictures-new",
                    f"inventory/{inventory_file_suffix}",
                    value,
                )
            finally:
                self.queue.task_done()
