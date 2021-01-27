from datetime import datetime
from S3 import *
from S3Inventory import S3Inventory, WriteResults
import sys

# Get the command-line args
assert (
    len(sys.argv) == 4
), "Did not receive the expected source bucket, destination bucket, and inventory prefix command line arguments"
source_bucket = sys.argv[1]
destination_bucket = sys.argv[2]
destination_prefix = sys.argv[3]

# Get the full inventory of S3 objects
start = datetime.now()

subject = S3Inventory(destination_bucket, S3())
results = subject.create_inventory(source_bucket, destination_prefix, "")

end = datetime.now()
duration = end - start
print(f"Duration: {duration}")

print(f"Objects found: {results.line_count}")