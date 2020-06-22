# This code creates r.stats files for the creation of avg temp, avg summer temp, avg winter temp and temp std. dev. and ditto for precip for the decade 2010-2019 on the theseus machine  

g.mapset mapset=SNAP_climate location=alaska_aea
#cd /home/vk5/ngee_arctic/niche_modeling/generate_maps_bioclim_vars

## Set the region to council watershed
#g.region rast=council_extent
#g.region nsres=771 ewres=771 -p
#watershed=council

## Region for kougarok
#g.region rast=kougarok_extent
#g.region nsres=771 ewres=771 -p
#watershed=kougarok

## Region for teller
g.region rast=teller_extent
g.region nsres=771 ewres=771 -p
watershed=teller

for var in tas_mean pr_total; do

# Avg temp/precip
r.stats -1gn input=`g.list type=raster pattern=${var}* separator=comma` output=${var}_${watershed}_2010_19

# Avg summer(Jun, Jul, Aug and Sep), Avg winter(Dec, Jan, Feb, Mar)
# Winter
a=$(g.list type=raster pattern=${var}_*_0[1-3]_* separator=comma)
b=$(g.list type=raster pattern=${var}_*_12_* separator=comma)
winter_files=$(echo $a,$b)
r.stats -1gn input=${winter_files} output=${var}_${watershed}_2010_19_winter

# Summer
r.stats -1gn input=`g.list type=raster pattern=${var}*_0[6-9]_* separator=comma` output=${var}_${watershed}_2010_19_summer
done
