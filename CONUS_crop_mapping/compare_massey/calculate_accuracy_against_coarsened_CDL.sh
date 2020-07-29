## This code calculates the accuracy of the predcted crop map against coarsened CDL for the years 2015 through 2018
## The output for this code is present at /home/vk5/compare_massey/coarsened_cdl_accuracy on theseus
## This code was just a experiment and the results from this were not included in the final paper
## We wanted to see if calculating accuracy at the coarsened scale helps improve the accuracy significantly

year=2018

#g.mapset mapset=create_coarse_cdl
#g.region rast=crop_map_predicted_2015_250m -p
#r.mask -r

### Generate areas under overlapped areas between cdl and pheno-reclassed map
r.stats -cn input=crop_map_predicted_${year}_250m,coarsened_cdl_250m_${year}_no_veg output=r.stats_predicted_cdl_${year}

# Calculate accuracies for 
crops=( 1 5 24 61 37 36 4 3 )
n_crops=${#crops[@]}
#
rm accuracy_${year}_coarsened 
touch accuracy_${year}_coarsened

for ((i=0; i<${n_crops}; i++)); do
crop=${crops[${i}]}

## calculate accuracies
correctly_classified=$(awk -v crop=${crop} '$1==crop && $2==crop' r.stats_predicted_cdl_${year} | cut -d" " -f3)
numerator=`echo ${correctly_classified}*100 | bc`
total_crop_cdl=$(awk -v crop=${crop} '$2==crop' r.stats_predicted_cdl_${year} | cut -d" " -f3 | paste -sd+ | bc)
total_crop_reclassed=$(awk -v crop=${crop} '$1==crop' r.stats_predicted_cdl_${year} | cut -d" " -f3 | paste -sd+ | bc)
producer_acc=`echo ${numerator}/${total_crop_cdl} | bc`
user_acc=`echo ${numerator}/${total_crop_reclassed} | bc`

## add accuracies to the file
list=( ${crop} ${producer_acc} ${user_acc} )
echo ${list[@]} >> accuracy_${year}_coarsened
done
