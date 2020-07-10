# This code creates r.stats -1gn for phenoregion maps (2008-2014) masked one ecoregion at a time. 

year=$1
min=$2
max=$3

export GISRC=/home/vk5/.grass7/map${year}_rc

# go inside every ecoregion
r.mask -r
for eco in `seq ${min} ${max}`; do
eco_num=$(printf %03d ${eco})
cd ecoregion_${eco_num}
echo working on ecoregion $eco

# Apply ecoregion mask, zoom while at 231m and then change it to 30m
g.region rast=hh_500_map@run_mapcurves
r.mask input=hh_500_map@run_mapcurves maskcats=$eco
g.region rast=hh_500_map@run_mapcurves zoom=hh_500_map@run_mapcurves
g.region nsres=32.59401346 ewres=30.42502556
g.region -p

r.stats -1gn input=phenology_2000-2016.5000.2015_resampled@run_mapcurves output=2015_rstats_phenoregion_eco_${eco_num}
r.mask -r

cd ..
done
