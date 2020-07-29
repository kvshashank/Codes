## THis code samples points randomly on the landscape; delineates the upstream watersheds and counts the number of pixels occupied by alder in those watersheds 

r.mask -r
g.mapset mapset=niche_model_inputs_2 location=alaska_aea
watershed=council
g.region rast=${watershed}_flow_dir -p

## Create a flow accumulation map with only cell values >= 10; using the flow_acc_thresh10 map as mask, create a new plant community map; perform sampling on the new map
r.accumulate -n direction=${watershed}_flow_dir accumulation=${watershed}_flow_accumulation --overwrite
r.mapcalc "${watershed}_flow_accumulation_thresh10 = if(${watershed}_flow_accumulation<10, null(), ${watershed}_flow_accumulation)" --overwrite
r.mask ${watershed}_flow_accumulation_thresh10
r.resample input=${watershed}_extended_predictions_map_recoded_clipped_wo_water_mask_classes output=${watershed}_predict_map_mask_flow_accum --overwrite
r.mask -r
r.sample.category ${watershed}_predict_map_mask_flow_accum output=${watershed}_sample_points npoints=111,214,217,641,23,38,114 random_seed=0 --overwrite

## Convert the sample points vector map to raster and mask the plant community map
v.to.rast input=${watershed}_sample_points type=point output=${watershed}_sample_points use="val" --overwrite
r.mask ${watershed}_sample_points
r.resample input=${watershed}_extended_predictions_map_recoded_clipped_wo_water_mask_classes output=${watershed}_prediction_masked_sample_pts --overwrite
r.mask -r

## calculate r.stats -1gn on the prediction_masked_sample_points map
r.stats -1gn input=${watershed}_prediction_masked_sample_pts output=${watershed}_sample_pts_coords_plant_comm --overwrite

rm ${watershed}_alder_count_each_subwatershed_for_sample_pts
touch ${watershed}_alder_count_each_subwatershed_for_sample_pts

ncoords=$(wc -l ${watershed}_sample_pts_coords_plant_comm | cut -d" " -f1)

for i in `seq 1 ${ncoords}`; do
g.region rast=${watershed}_flow_dir -p
echo working on sample ${i} out of ${ncoords}......

# Extract x and y coordinates for each sample point
x_coord=$(head -${i} ${watershed}_sample_pts_coords_plant_comm | tail -1 | cut -d" " -f1)
y_coord=$(head -${i} ${watershed}_sample_pts_coords_plant_comm | tail -1 | cut -d" " -f2)
plant_comm=$(head -${i} ${watershed}_sample_pts_coords_plant_comm | tail -1 | cut -d" " -f3)

# Delineate drainage area for each sample point
r.accumulate direction=${watershed}_flow_dir subwatershed=subwatershed coordinates=${x_coord},${y_coord} --overwrite
g.region rast=subwatershed zoom=subwatershed
r.mask subwatershed

r.stats -nc input=${watershed}_extended_predictions_map_recoded_clipped_wo_water_mask_classes output=rstats_subwatershed --overwrite

# Count alder and total number of pixels for every subwatershed
total_count=$(cat rstats_subwatershed | cut -d" " -f2 | paste -sd+ | bc)
alder_count=$(awk '$1==29' rstats_subwatershed | cut -d" " -f2)

echo ${x_coord}" "${y_coord}" "${plant_comm}" "${alder_count}" "${total_count} >> ${watershed}_alder_count_each_subwatershed_for_sample_pts

r.mask -r
done 
