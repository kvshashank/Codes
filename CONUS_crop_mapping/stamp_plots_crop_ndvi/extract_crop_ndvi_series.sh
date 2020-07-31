## Data for this code is present at /data2/vk5/stamp_plots_crop_ndvi on mutiny

rc=$1
year=$2
export GISRC=/home/vk5/.grass7/map${rc}_rc
g.gisenv

for crop in 1 2 3 4 5 23 24 26 36 37 43 61; do
echo working on crop ${crop} for year ${year}...
## Copy required rasters from crop_data_layer mapset to this mapset
g.copy raster=${year}_cdl_250_no_veg_hh_500_266_crop_${crop}@ndvi,${year}_cdl_250_no_veg_hh_500_266_crop_${crop}
g.region rast=${year}_cdl_250_no_veg_hh_500_266_crop_${crop} zoom=${year}_cdl_250_no_veg_hh_500_266_crop_${crop} -p
r.mask raster=${year}_cdl_250_no_veg_hh_500_266_crop_${crop} --overwrite
r.stats -n input=MCD13.A${year}.band01@ndvi,MCD13.A${year}.band02@ndvi,MCD13.A${year}.band03@ndvi,MCD13.A${year}.band04@ndvi,MCD13.A${year}.band05@ndvi,MCD13.A${year}.band06@ndvi,MCD13.A${year}.band07@ndvi,MCD13.A${year}.band08@ndvi,MCD13.A${year}.band09@ndvi,MCD13.A${year}.band10@ndvi,MCD13.A${year}.band11@ndvi,MCD13.A${year}.band12@ndvi,MCD13.A${year}.band13@ndvi,MCD13.A${year}.band14@ndvi,MCD13.A${year}.band15@ndvi,MCD13.A${year}.band16@ndvi,MCD13.A${year}.band17@ndvi,MCD13.A${year}.band18@ndvi,MCD13.A${year}.band19@ndvi,MCD13.A${year}.band20@ndvi,MCD13.A${year}.band21@ndvi,MCD13.A${year}.band22@ndvi,MCD13.A${year}.band23@ndvi,MCD13.A${year}.band24@ndvi,MCD13.A${year}.band25@ndvi,MCD13.A${year}.band26@ndvi,MCD13.A${year}.band27@ndvi,MCD13.A${year}.band28@ndvi,MCD13.A${year}.band29@ndvi,MCD13.A${year}.band30@ndvi,MCD13.A${year}.band31@ndvi,MCD13.A${year}.band32@ndvi,MCD13.A${year}.band33@ndvi,MCD13.A${year}.band34@ndvi,MCD13.A${year}.band35@ndvi,MCD13.A${year}.band36@ndvi,MCD13.A${year}.band37@ndvi,MCD13.A${year}.band38@ndvi,MCD13.A${year}.band39@ndvi,MCD13.A${year}.band40@ndvi,MCD13.A${year}.band41@ndvi,MCD13.A${year}.band42@ndvi,MCD13.A${year}.band43@ndvi,MCD13.A${year}.band44@ndvi,MCD13.A${year}.band45@ndvi,MCD13.A${year}.band46@ndvi output=r.stats_ecoregion_266_crop_${crop}_${year} --overwrite
done

r.mask -r
