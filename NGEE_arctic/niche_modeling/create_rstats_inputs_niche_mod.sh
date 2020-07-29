## This code creates the input files for the niche model with the following columns: Topography(Slope, sin(aspect), cos(aspect), elevation, Topo_wetness_index, Avg_Summer_Solar_Irrd, Avg_Winter_Solar_Irrd) and Climate(Mean_Annual_Temp, Mean_Summer_Temp, Mean_Winter_Temp, Temp_Std_Dev, Mean_Annual_Precip, Mean_Summer_Precip, Mean_Winter_Precip, Precip_Std_Dev)
## Winter: Dec, Jan, Feb, Mar; Summer: June, July, Aug, Sept 

g.mapset mapset=niche_model_inputs_2 location=alaska_aea

## Set the region to council watershed
#g.region rast=avg_summer_solar_irr_council -p
#r.mask avg_summer_solar_irr_council --overwrite
#watershed=council

## Region for kougarok
#g.region rast=avg_summer_solar_irr_kougarok -p
#r.mask avg_summer_solar_irr_kougarok --overwrite
#watershed=kougarok

## Region for teller
g.region rast=avg_summer_solar_irr_teller -p
r.mask avg_summer_solar_irr_teller --overwrite
watershed=teller

r.stats -1gn input=slope,sin_aspect,cos_aspect,elevation,topo_wetness_index,avg_summer_solar_irr_${watershed},avg_winter_solar_irr_${watershed},tas_mean_${watershed}_2010_19_mean,tas_mean_${watershed}_2010_19_summer_mean,tas_mean_${watershed}_2010_19_winter_mean,tas_mean_${watershed}_2010_19_std_dev,pr_total_${watershed}_2010_19_mean,pr_total_${watershed}_2010_19_summer_mean,pr_total_${watershed}_2010_19_winter_mean,pr_total_${watershed}_2010_19_std_dev,${watershed}_extended_predictions_map_recoded_clipped output=${watershed}_niche_model_inputs --overwrite

r.mask -r
