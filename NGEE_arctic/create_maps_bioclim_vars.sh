## This code creates annual_avg, summer and winter avg, std_dev for annual temperature and precip maps for the three extended watersheds
## The data for this code is available at /home/vk5/ngee_arctic/niche_modeling/generate_maps_bioclim_vars on theseus machine

g.mapset mapset=niche_model_inputs_2 location=alaska_aea
#cd /home/vk5/ngee_arctic/niche_modeling/generate_maps_bioclim_vars

## Set the region to council watershed
#g.region rast=avg_summer_solar_irr_council
#g.region nsres=771 ewres=771 -p
#watershed=council

## Region for kougarok
#g.region rast=avg_summer_solar_irr_kougarok
#g.region nsres=771 ewres=771 -p
#watershed=kougarok

## Region for teller
g.region rast=avg_summer_solar_irr_teller
g.region nsres=771 ewres=771 -p
watershed=teller

for var in pr_total tas_mean; do
# Mean climate and std dev 
r.in.xyz input=${var}_${watershed}_2010_19_stats x=1 y=2 z=3 output=${var}_${watershed}_2010_19_mean separator=space
r.in.xyz input=${var}_${watershed}_2010_19_stats x=1 y=2 z=4 output=${var}_${watershed}_2010_19_std_dev separator=space

# Mean climate during summer and winter
r.in.xyz input=${var}_${watershed}_2010_19_summer_stats x=1 y=2 z=3 output=${var}_${watershed}_2010_19_summer_mean separator=space
r.in.xyz input=${var}_${watershed}_2010_19_winter_stats x=1 y=2 z=3 output=${var}_${watershed}_2010_19_winter_mean separator=space
done
