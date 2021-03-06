# Get Dropbox folder synced with S3
find ~/Dropbox/ZieglerPics/svz-master-pictures > dropbox_sync_s3.txt


# Compare S3 folder counts from original file to the latest to see what got accidentally deleted
export pattern="original"
export original="$(grep -E "$pattern" inventory_pre_delete.csv | wc -l)"
export latest="$(grep -E "$pattern" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
echo ""
echo "Pattern     Prev         Cur"
echo "$pattern $original -> $latest"
echo ""

echo ""
echo "Pattern           Prev ->     Cur  |  Starred"
for i in $(seq 2020 -1 2003) 
do
    export pattern="original"
    export original="$(grep -E "$pattern/$i" inventory_pre_delete.csv | wc -l)"
    export latest="$(grep -E "$pattern/$i" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
    export starred="$(grep -E "Master Starred Pictures.*$i" external_drive_find_output/all_pictures_drive_a_beatup.txt | wc -l)"
    echo "$pattern/$i $original -> $latest | $starred"
done


echo ""
export pattern="original-backup"
export original="$(grep -E "$pattern" inventory_pre_delete.csv | wc -l)"
export latest="$(grep -E "$pattern" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
echo "$pattern $original -> $latest"
echo "Pattern                  Prev ->     Cur  "
for i in $(seq 2020 -1 2003) 
do
    export pattern="original-backup"
    export original="$(grep -E "$pattern/$i" inventory_pre_delete.csv | wc -l)"
    export latest="$(grep -E "$pattern/$i" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
    echo "$pattern/$i $original -> $latest "
done


echo ""
export pattern="small"
export original="$(grep -E "$pattern" inventory_pre_delete.csv | wc -l)"
export latest="$(grep -E "$pattern" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
echo "$pattern $original -> $latest"
echo "Pattern        Prev ->     Cur  "
for i in $(seq 2020 -1 2003) 
do
    export original="$(grep -E "$pattern/$i" inventory_pre_delete.csv | wc -l)"
    export latest="$(grep -E "$pattern/$i" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
    echo "$pattern/$i $original -> $latest "
done


echo ""
export pattern="thumbnail"
export original="$(grep -E "$pattern" inventory_pre_delete.csv | wc -l)"
export latest="$(grep -E "$pattern" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
echo "$pattern $original -> $latest"
echo "Pattern            Prev ->     Cur  "
for i in $(seq 2020 -1 2003) 
do
    export original="$(grep -E "$pattern/$i" inventory_pre_delete.csv | wc -l)"
    export latest="$(grep -E "$pattern/$i" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
    echo "$pattern/$i $original -> $latest "
done



echo ""
export pattern="raw-photos"
export original="$(grep -E "$pattern" inventory_pre_delete.csv | wc -l)"
export latest="$(grep -E "$pattern" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
echo "$pattern $original -> $latest"

echo "Pattern             Prev ->     Cur  "
for i in $(seq 2020 -1 2003) 
do
    export pattern="raw-photos"
    export original="$(grep -E "$pattern/$i" inventory_pre_delete.csv | wc -l)"
    export latest="$(grep -E "$pattern/$i" get_inventory_files_from_s3/inventory/_inventory.csv | wc -l)"
    echo "$pattern/$i $original -> $latest "
done


