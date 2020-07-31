## This code is present at /home/vk5/aggregate_results_spatially/obs_vs_pred_scatterplot on theseus
## Codes in this directory were used to create the scatterplot between obs and predicted acreages at county-, state- and CONUS-scale 

g.region rast=2016_30m_cdl_no_veg -p
g.mapset mapset=run_mapcurves
r.mask -r
# Ecoregionwise
# Observed Acreages for three years
r.stats -cn input=hh_500_map,2015_30m_cdl_no_veg output=r.stats_2015_ecoregion_cdl_count &
r.stats -cn input=hh_500_map,2016_30m_cdl_no_veg output=r.stats_2016_ecoregion_cdl_count &
r.stats -cn input=hh_500_map,2017_30m_cdl_no_veg output=r.stats_2017_ecoregion_cdl_count &
r.stats -cn input=hh_500_map,2018_30m_cdl_no_veg output=r.stats_2018_ecoregion_cdl_count &

# Predicted acreages for three years
r.stats -cn input=hh_500_map,2015_30m_pheno_reclassed_46_img output=r.stats_2015_ecoregion_reclassed_pheno_count &
r.stats -cn input=hh_500_map,2016_30m_pheno_reclassed_46_img output=r.stats_2016_ecoregion_reclassed_pheno_count &
r.stats -cn input=hh_500_map,2017_30m_pheno_reclassed_46_img output=r.stats_2017_ecoregion_reclassed_pheno_count &

# Statewise
# Observed acreages for three years
r.stats -cn input=state_map,2015_30m_cdl_no_veg output=r.stats_2015_state_cdl_count &
r.stats -cn input=state_map,2016_30m_cdl_no_veg output=r.stats_2016_state_cdl_count &
r.stats -cn input=state_map,2017_30m_cdl_no_veg output=r.stats_2017_state_cdl_count &
r.stats -cn input=state_map,2018_30m_cdl_no_veg output=r.stats_2018_state_cdl_count &

# Predicted acreages for three years
r.stats -cn input=state_map,2015_30m_pheno_reclassed_46_img output=r.stats_2015_state_reclassed_pheno_count &
r.stats -cn input=state_map,2016_30m_pheno_reclassed_46_img output=r.stats_2016_state_reclassed_pheno_count &
r.stats -cn input=state_map,2017_30m_pheno_reclassed_46_img output=r.stats_2017_state_reclassed_pheno_count &
