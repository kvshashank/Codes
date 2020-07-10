## Run code simultaneously on multiple cores
## Code location /home/vk5/mapcurves_2015_ecoregion_state_CONUS/mapcurves_2015_ecoregion on theseus

sh create_rstats_cdl_ecoregion.sh 2010 1 100 &
sh create_rstats_cdl_ecoregion.sh 2011 101 200 &
sh create_rstats_cdl_ecoregion.sh 2012 201 300 &
sh create_rstats_cdl_ecoregion.sh 2013 301 400 &
sh create_rstats_cdl_ecoregion.sh 2014 401 500
