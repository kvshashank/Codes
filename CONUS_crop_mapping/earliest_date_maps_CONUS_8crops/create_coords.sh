g.mapset mapset=earliest_date_maps_CONUS_8crops 
r.mask -r
g.region rast=hh_500_map -p

for crop in 1 5 24 61 37 36 4 3; do
cd crop_${crop}
echo working on crop ${crop}...
#r.stats -1gn input=hh_500_map_5pct_thresh_crop_${crop} output=ecoregion_coords_crop_${crop} --overwrite
#awk '{print $3" "$1" "$2}' ecoregion_coords_crop_${crop} > ecoregion_coords_crop_${crop}_2
#awk 'NR==FNR{n[$1]=$2; next} ($1 in n) {print $0,n[$1]}' crop_${crop}_ecoregion_doy_thresholds_2015 ecoregion_coords_crop_${crop}_2 > ecoregionwise_earliest_classification_date_crop_${crop}
rm ecoregion_coords_crop_${crop}_2
r.in.xyz input=ecoregionwise_earliest_classification_date_crop_${crop} output=earliest_classification_date_map_crop_${crop}_CONUS x=2 y=3 z=4 fs=space type=CELL
cd ..
done

 
