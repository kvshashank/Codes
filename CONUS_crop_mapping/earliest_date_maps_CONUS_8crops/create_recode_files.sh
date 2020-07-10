cd create_5pct_thresh_ecoregion_maps_8crops

files=$(ls major_ecoregions_*)

for file in ${files}; do
crop=$(echo ${file} | cut -d"_" -f4)
cat ${file} | cut -d" " -f1 > ecoregions
paste -d":" ecoregions ecoregions ecoregions ecoregions > recode_rules_crop_${crop}
done

rm ecoregions
