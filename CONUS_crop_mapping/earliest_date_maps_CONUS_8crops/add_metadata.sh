for crop in corn soybeans winter_wheat fallow other_hay_non_alfalfa alfalfa sorghum; do
echo working on earliest_classification_date_${crop}_CONUS.nc....
#ncrename -v earliest_classification_day_of_the_year,earliest_classification_day_of_the_year_${crop} earliest_classification_date_${crop}_CONUS.nc
#ncatted -O -h -a Author,global,o,c,"Venkata Shashank Konduri, Jitendra Kumar, William W. Hargrove, Forrest M. Hoffman, Auroop R. Ganguly" earliest_classification_date_${crop}_CONUS.nc
#ncatted -O -h -a Institution,global,o,c,"Oak Ridge National Laboratory, Northeastern University, USDA Forest Service" earliest_classification_date_${crop}_CONUS.nc
#ncatted -O -h -a Contact,global,o,c,"Venkata Shashank Konduri (konduri.v@husky.neu.edu)" earliest_classification_date_${crop}_CONUS.nc
ncatted -O -h -a Data_DOI,global,o,c,"https://doi.org/10.5281/zenodo.3878979" earliest_classification_date_${crop}_CONUS.nc
done
