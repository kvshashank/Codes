rc=$1
export GISRC=/home/vk5/.grass7/map${rc}_rc
r.mask -r
g.gisenv

crop=$2
cd crop_${crop}

## Copy greenup maps to this mapset
#echo copying greenup maps...
#for int in 12 16 20 24 28 32 36; do 
#g.copy rast=greenup_dates_img_${int}_masked@earliest_date_maps_CONUS_8crops,greenup_dates_img_${int}_masked
#done
#
#crop=$2
#g.copy rast=hh_500_map_5pct_thresh_crop_${crop}@earliest_date_maps_CONUS_8crops,hh_500_map_5pct_thresh_crop_${crop}
#mkdir crop_${crop}
#cd crop_${crop}
#
## Create a map of crop-specific ecoregions masked to the greenup map
#echo masking ecoregion map to include only greened up pixels...
#for int in 12 16 20 24 28 32 36; do
#g.region rast=greenup_dates_img_${int}_masked -p
#r.mask -o greenup_dates_img_${int}_masked
#r.resample input=hh_500_map_5pct_thresh_crop_${crop} output=hh_500_map_5pct_thresh_crop_${crop}_masked_img_${int}
#done
#
#r.mask -r

# Calculate r.stats for each ecoregion 
g.region rast=hh_500_map_5pct_thresh_crop_${crop}
r.category hh_500_map_5pct_thresh_crop_${crop} > ecoregions_crop_${crop}
n_eco=$(wc -l ecoregions_crop_${crop} | cut -d" " -f1)

for int in 12 16 20 24 28 32 36; do
for i in `seq 1 ${n_eco}`; do
ecoregion=$(head -${i} ecoregions_crop_${crop} | tail -1 | cut -d$'\t' -f1)
echo working on img ${int} and ecoregion ${ecoregion}.....

# Apply ecoregion mask and zoom to ecoregion
r.mask -o hh_500_map_5pct_thresh_crop_${crop}_masked_img_${int} maskcats=${ecoregion}
echo zooming to ecoregion ${ecoregion}...
g.region rast=hh_500_map_5pct_thresh_crop_${crop} zoom=hh_500_map_5pct_thresh_crop_${crop} 

# Change resolution to 30m
g.region nsres=32.59401346 ewres=30.42502556 -p
output_file=rstats_phenoreclass_cdl_eco_${ecoregion}_img_${int}_crop_${crop}
echo ${output_file}
r.stats -nc input=2015_30m_pheno_reclassed_${int}_img@run_mapcurves,2015_30m_cdl_no_veg@run_mapcurves output=${output_file} --overwrite
done
done

for int in 40 43 46; do
for i in `seq 1 ${n_eco}`; do

ecoregion=$(head -${i} ecoregions_crop_${crop} | tail -1 | cut -d$'\t' -f1)
echo working on img ${int} and ecoregion ${ecoregion}.....

# Apply ecoregion mask and zoom to ecoregion
r.mask -o hh_500_map_5pct_thresh_crop_${crop} maskcats=${ecoregion}
echo zooming to ecoregion ${ecoregion}...
g.region rast=hh_500_map_5pct_thresh_crop_${crop} zoom=hh_500_map_5pct_thresh_crop_${crop}

# Change resolution to 30m
g.region nsres=32.59401346 ewres=30.42502556 -p

output_file=rstats_phenoreclass_cdl_eco_${ecoregion}_img_${int}_crop_${crop}
r.stats -nc input=2015_30m_pheno_reclassed_${int}_img@run_mapcurves,2015_30m_cdl_no_veg@run_mapcurves output=${output_file} --overwrite
done
done

r.mask -r
