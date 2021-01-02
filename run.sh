# Main script to create and download the S3 file inventory
python3 get_s3_inventory.py  
aws s3 cp s3://svz-master-pictures-new/inventory/inventory.csv .
