g.mapset mapset=earliest_date_maps_CONUS_8crops
g.region rast=hh_500_map
r.mask -r

cd create_5pct_thresh_ecoregion_maps_8crops
for crop in 5 24 61 37 36 4 3; do
recode_file=recode_rules_crop_${crop}
r.recode input=hh_500_map output=hh_500_map_5pct_thresh_crop_${crop} rules=${recode_file}
done
