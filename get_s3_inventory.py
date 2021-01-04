from datetime import datetime
from S3 import *
from S3Inventory import S3Inventory, WriteResults

# Get the full inventory of S3 objects
start = datetime.now()

subject = S3Inventory("svz-master-pictures-new", S3())
results = subject.create_inventory("svz-master-pictures-new", "inventory", "")

end = datetime.now()
duration = end - start
print("Duration:")
print(duration)

assert results.line_count >= 80000, "Expected to find more than 100,000 objects"
