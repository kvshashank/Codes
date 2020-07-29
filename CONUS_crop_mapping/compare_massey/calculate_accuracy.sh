## This code calculates the accuracies for the year 2008 without combining crop types
## The data for this is available at /home/vk5/compare_massey

#Calculate accuracies for 
crops=( 1 3 4 5 24 36 37 61 )
year=2008
n_crops=${#crops[@]}

rm accuracy_${year}_no_combined
touch accuracy_${year}_no_combined

for ((i=0; i<${n_crops}; i++)); do
crop=${crops[${i}]}

# calculate accuracies
correctly_classified=$(awk -v crop=${crop} '$1==crop && $2==crop' r.stats_phenoregion_cdl_2008 | cut -d" " -f3)
numerator=`echo ${correctly_classified}*100 | bc`
total_crop_cdl=$(awk -v crop=${crop} '$2==crop' r.stats_phenoregion_cdl_2008 | cut -d" " -f3 | paste -sd+ | bc)
total_crop_reclassed=$(awk -v crop=${crop} '$1==crop' r.stats_phenoregion_cdl_2008 | cut -d" " -f3 | paste -sd+ | bc)
producer_acc=`echo ${numerator}/${total_crop_cdl} | bc`
user_acc=`echo ${numerator}/${total_crop_reclassed} | bc`

# add accuracies to the file
list=( ${crop} ${producer_acc} ${user_acc} )
echo ${list[@]} >> accuracy_${year}_no_combined
done

