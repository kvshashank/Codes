for crop in 1; do
cd crop_${crop}
rm accuracy_2015_crop_${crop}_user_acc
touch accuracy_2015_crop_${crop}_user_acc

for file in $(ls *crop_${crop}); do
eco=$(echo ${file} | cut -d"_" -f5)
img=$(echo ${file} | cut -d"_" -f7)
echo working on ecoregion ${eco} and img ${img} for crop ${crop}..
rm temp
touch temp
correctly_classified=$(awk -v crop=${crop} '$1==crop && $2==crop' ${file} | cut -d" " -f3)
numerator=`echo ${correctly_classified}*100 | bc`
total_crop_reclassed=$(awk -v crop=${crop} '$1==crop' ${file} | cut -d" " -f3 | paste -sd+ | bc)
user_acc=`echo ${numerator}/${total_crop_reclassed} | bc`
list=( ${crop} ${user_acc} ${eco} ${img} )
echo ${list[@]} >> temp
awk 'NF>3' temp >> accuracy_2015_crop_${crop}_user_acc
done
rm temp
cd ..
done
