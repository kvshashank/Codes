rc=$1
crop=$2
cd crop_${crop}

export GISRC=/home/vk5/.grass7/map${rc}_rc
g.gisenv

# Copy maps from other mapsets
g.copy rast=greenup_dates_img_36@users_acc_progression,greenup_dates_img_36
g.copy rast=2015_30m_cdl_no_veg@users_acc_progression,2015_30m_cdl_no_veg
g.copy rast=hh_500_map_5pct_thresh_crop_${crop}@earliest_date_maps_CONUS_8crops,hh_500_map_5pct_thresh_crop_${crop}

r.mask -r
g.region rast=2015_30m_cdl_no_veg -p

r.mask 2015_30m_cdl_no_veg maskcats=${crop}
echo resampling the greenup map for crop ${crop}....
r.resample input=greenup_dates_img_36 output=greenup_dates_img_36_crop_${crop}
r.mask -r

r.stats -nc input=hh_500_map_5pct_thresh_crop_${crop},greenup_dates_img_36_crop_${crop} output=ecoregionwise_crop_${crop}_pixel_greenup
