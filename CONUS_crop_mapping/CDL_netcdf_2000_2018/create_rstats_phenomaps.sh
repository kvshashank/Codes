## This code creates ecoregion-wise r.stats files for phenoregion maps. Ecoregion-wise analysis helps in assigning crop labels at a fine scale to avoid problems due to spatial variablility in phenology
## For every ecoregion, apply a mask of the CDL (to consider only phenoregions corresponding to croplands), and then do an r.stats -1gn of phenoregion maps  
## Using rc files, this code can be run in parallel for multiple years 

rc=$1
year=$2
export GISRC=/home/vk5/.grass7/map${rc}_rc
g.gisenv
r.mask -r
#g.copy rast=hh_500_map@run_mapcurves,hh_500_map
#g.copy rast=${year}_30m_cdl_no_veg@run_mapcurves,${year}_30m_cdl_no_veg
#g.copy rast=phenology_2000-2016.5000.${year}@run_mapcurves,phenology_2000-2016.5000.${year}

#g.region rast=phenology_2000-2016.5000.${year} -p
#r.resample input=${year}_30m_cdl_no_veg output=${year}_250m_cdl_no_veg

r.mask ${year}_250m_cdl_no_veg
r.resample input=hh_500_map output=hh_500_map_masked_${year}_cdl_250m
r.mask -r

for i in `seq 1 500`; do
eco_num=$(printf %03d ${i})
cd ecoregion_${eco_num}
echo generating r.stats file for ecoregion ${eco_num} for year ${year}...
r.mask -o input=hh_500_map_masked_${year}_cdl_250m maskcats=${i}
r.stats -1gn input=phenology_2000-2016.5000.${year} output=rstats_phenoregion_eco_${eco_num}_${year} --overwrite
cd ..
done

r.mask -r
