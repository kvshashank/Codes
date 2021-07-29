## Data for this code is present at /home/vk5/postdoc/MCD64

g.mapset mapset=map1 location=MCD64
g.region rast=A2008092_burn_date -p
r.mask -r
maps=$(g.list type=raster pattern=*burn_date)

for map in ${maps}; do
code=$(echo ${map} | cut -d"_" -f1)

## Remove pixels with fill values and water
r.recode input=${map} output=${map}_recoded --overwrite rules=- << EOF 
0:365:0:365
EOF

## Apply burn date uncertainty mask
uncertainty_map=${code}_burn_data_uncertainty
r.recode input=${uncertainty_map} output=${uncertainty_map}_recoded --overwrite rules=- << EOF
0:7:0:7
EOF

r.mask ${uncertainty_map}_recoded
r.resample input=${map} output=${map}_wo_uncertain --overwrite
r.mask -r
 
## Apply qa flag mask
r.mask ${code}_qa maskcats=3
r.resample input=${map}_wo_uncertain output=${map}_wo_uncertain_qa --overwrite
r.mask -r

g.remove -f type=raster name=${map}_wo_uncertain
g.remove -f type=raster name=${uncertainty_map}_recoded
g.remove -f type=raster name=${map}_recoded
done
