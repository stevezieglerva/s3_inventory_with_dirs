# Main script to create and download the S3 file inventory
python3 get_s3_inventory.py svz-master-pictures-new svz-master-pictures-new "inventory/"
aws s3 cp s3://svz-master-pictures-new/inventory/_inventory.csv ./get_inventory_files_from_s3/inventory/

# Check the various count

export year="2011"
echo "$year"
grep -E "$year" ./get_inventory_files_from_s3/inventory/_inventory.csv | wc -l

export year="2012"
echo "$year"
grep -E "$year" ./get_inventory_files_from_s3/inventory/_inventory.csv | wc -l

export year="2018"
echo "$year"
grep -E "$year" ./get_inventory_files_from_s3/inventory/_inventory.csv | wc -l

export year="2019"
echo "$year"
grep -E "$year" ./get_inventory_files_from_s3/inventory/_inventory.csv | wc -l

export year="2020"
echo "$year"
grep -E "$year" ./get_inventory_files_from_s3/inventory/_inventory.csv | wc -l
