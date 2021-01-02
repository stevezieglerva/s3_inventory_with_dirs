
for i in {2003..2020}
do
    echo ""
    echo "************"
    echo "   $i"
    /usr/local/bin/aws s3 sync /Volumes/My\ Passport/ZieglerPics/$i s3://svz-master-pictures/raw-photos/$i 
done


