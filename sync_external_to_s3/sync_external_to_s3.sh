
for i in $(seq 2020 -1 2003) #{2003..2020}
do
    echo ""
    echo "************"
    echo "   $i"
    /usr/local/bin/aws s3 sync /Volumes/My\ Passport/ZieglerPics/$i s3://svz-master-pictures-new/raw-photos/$i 
done



