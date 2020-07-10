## This code calculates the users and producers accuracy at CONUS scale. The goal is to compare the accuracy at CONUS, state and ecoregion level.. 
## THe data for this code is available at /home/vk5/mapcurves_2015_ecoregion_state_CONUS/mapcurves_2015_CONUS on theseus..

## Remove " = " and " """ symbols from map2.reclass files in every ecoregion folder
#num_ecoregions=$(ls -d ecoregion_* | wc -l)
#for i in `seq 1 ${num_ecoregions}`; do
#folder=$(ls -d ecoregion_* | head -${i} | tail -1)
#cd $folder
#echo working on $folder
#eco=$(echo ${folder} | cut -d"_" -f2)
#
##sed -i -e 's/ = / /' map2.reclass
##sed -i -e 's/ ""//' map2.reclass
#
## Rearrange columns to apply awk and then replace all phenoregion values in the r.stats file with cdl labels from map2.reclass
#awk '{print $3" "$1" "$2}' 2015_rstats_phenoregion_eco_${eco} > 2015_rstats_phenoregion_eco_${eco}_2
#awk 'NR==FNR{n[$1]=$2; next} ($1 in n) {print $0,n[$1]}' map2.reclass 2015_rstats_phenoregion_eco_${eco}_2 > pheno_reclassed_data_${eco}_2015
#
#cp pheno_reclassed_data_${eco}_2015 ..
#cd ..
#done
#
#echo working on joining all files
#cat pheno_reclassed_data_* > pheno_reclassed_data_all_ecoregions_2015
#
## Create the reclassed map
#r.mask -r
#g.mapset mapset=run_mapcurves
#g.region rast=2008_30m_cdl_train -p
#r.in.xyz input=pheno_reclassed_data_all_ecoregions_2015 output=2015_pheno_reclassed_ecolevel_mapcurves fs=space x=2 y=3 z=4 type=CELL percent=10 --o

# Generate areas under overlapped areas between cdl and pheno-reclassed map
r.stats -cn input=2015_pheno_reclassed_CONUSlevel_mapcurves,2015_30m_cdl_no_veg output=r.stats_phenoregion_cdl_2015

# Calculate accuracies for 
crops=( 1 3 4 5 24 36 37 61 )
n_crops=${#crops[@]}

rm accuracy_2015_CONUS_level
touch accuracy_2015_CONUS_level

for ((i=0; i<${n_crops}; i++)); do
crop=${crops[${i}]}

# calculate accuracies
correctly_classified=$(awk -v crop=${crop} '$1==crop && $2==crop' r.stats_phenoregion_cdl_2015 | cut -d" " -f3)
numerator=`echo ${correctly_classified}*100 | bc`
total_crop_cdl=$(awk -v crop=${crop} '$2==crop' r.stats_phenoregion_cdl_2015 | cut -d" " -f3 | paste -sd+ | bc)
total_crop_reclassed=$(awk -v crop=${crop} '$1==crop' r.stats_phenoregion_cdl_2015 | cut -d" " -f3 | paste -sd+ | bc)
producer_acc=`echo ${numerator}/${total_crop_cdl} | bc`
user_acc=`echo ${numerator}/${total_crop_reclassed} | bc`

# add accuracies to the file
list=( ${crop} ${producer_acc} ${user_acc} )
echo ${list[@]} >> accuracy_2015_CONUS_level
done
