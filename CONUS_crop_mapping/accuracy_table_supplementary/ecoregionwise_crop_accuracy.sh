# Create a new file with four columns: "Ecoregion" "Crop" "no._of_pixels" "user's_acc"
## Data for this is present at /home/vk5/ecoregionwise_overall_acc on theseus
## This is used to create Table S2 in the supplementary section

rm ecoregionwise_crop_accuracy
touch ecoregionwise_crop_accuracy

n_eco=$(wc -l hh_500_20pct_thresh | cut -d" " -f1)

for i in `seq 1 ${n_eco}`; do
# Consider only crop-intensive ecoregions; select one such ecoregion at a time
eco=$(head -${i} hh_500_20pct_thresh | tail -1)
file=rstats_phenoregion_cdl_2015_ecoregion_${eco}

# Find unique crops in each ecoregion
uniq_crops=$(cat ${file} | cut -d" " -f1 | uniq)

# For each crop calculate user's accuracy
for crop in ${uniq_crops}; do
correctly_classified=$(awk -v crop=${crop} '$1==crop && $2==crop' ${file} | cut -d" " -f3)
numerator=`echo ${correctly_classified}*100 | bc`
total_crop_reclassed=$(awk -v crop=${crop} '$1==crop' ${file} | cut -d" " -f3 | paste -sd+ | bc)
user_acc=`echo ${numerator}/${total_crop_reclassed} | bc`

# add accuracies to the file
list=( ${eco} ${crop} ${total_crop_reclassed} ${user_acc} )
echo ${list[@]} >> ecoregionwise_crop_accuracy
done
done
