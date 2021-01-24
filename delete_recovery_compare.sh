# Get Dropbox folder synced with S3
find ~/Dropbox/ZieglerPics/svz-master-pictures > dropbox_sync_s3.txt


# Compare S3 folder counts from original file to the latest to see what got accidentally deleted
export pattern="original"
export original="$(grep -E "$pattern" inventory_pre_delete.csv | wc -l)"
export latest="$(grep -E "$pattern" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
echo "$pattern $original -> $latest"


for i in $(seq 2020 -1 2003) 
do
    export pattern="original"
    export original="$(grep -E "$pattern/$i" inventory_pre_delete.csv | wc -l)"
    export latest="$(grep -E "$pattern/$i" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
    export dropbox="$(grep -E "$pattern/$i" dropbox_sync_s3.txt | wc -l)"
    echo "$pattern/$i $original -> $latest | $dropbox"
done

echo "******"

export pattern="original-backup"
export original="$(grep -E "$pattern" inventory_pre_delete.csv | wc -l)"
export latest="$(grep -E "$pattern" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
echo "$pattern $original -> $latest"


export pattern="small"
export original="$(grep -E "$pattern" inventory_pre_delete.csv | wc -l)"
export latest="$(grep -E "$pattern" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
echo "$pattern $original -> $latest"

export pattern="thumbnail"
export original="$(grep -E "$pattern" inventory_pre_delete.csv | wc -l)"
export latest="$(grep -E "$pattern" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
echo "$pattern $original -> $latest"

echo "******"


export pattern="raw-photos"
export original="$(grep -E "$pattern" inventory_pre_delete.csv | wc -l)"
export latest="$(grep -E "$pattern" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
echo "$pattern $original -> $latest"


for i in $(seq 2020 -1 2003) 
do
    export pattern="raw-photos"
    export original="$(grep -E "$pattern/$i" inventory_pre_delete.csv | wc -l)"
    export latest="$(grep -E "$pattern/$i" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
    echo "$pattern/$i $original -> $latest | $dropbox"
done


