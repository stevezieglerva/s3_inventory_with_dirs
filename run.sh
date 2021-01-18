# Main script to create and download the S3 file inventory
python3 get_s3_inventory.py  
aws s3 cp s3://svz-master-pictures-new/inventory/inventory.csv .

# Check the various count

export year="2012"
echo "$year"
grep -E "$year" inventory.csv | wc -l

export year="2012"
echo "$year"
grep -E "$year" inventory.csv | wc -l

export year="2018"
echo "$year"
grep -E "$year" inventory.csv | wc -l

export year="2019"
echo "$year"
grep -E "$year" inventory.csv | wc -l

export year="2020"
echo "$year"
grep -E "$year" inventory.csv | wc -l
