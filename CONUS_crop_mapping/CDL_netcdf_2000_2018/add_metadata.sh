## Add metadata to CDL maps in netcdf format using NCO language commands
## Netcdf files are present in the folder /home/vk5/cdl_2000_2018 on theseus

for year in `seq 2001 2018`; do
ncrename -v Band1,Crop_Type crop_map_predicted_${year}_250m.nc
#mv crop_map_predicted_${year}_250m_netcdf crop_map_predicted_${year}_250m.nc
echo working on netcdf file crop_map_predicted_${year}_250m_netcdf
ncatted -O -h -a Author,global,o,c,"Venkata Shashank Konduri, Jitendra Kumar, William W. Hargrove, Forrest M. Hoffman, Auroop R. Ganguly" crop_map_predicted_${year}_250m_netcdf
ncatted -O -h -a Institution,global,o,c,"Oak Ridge National Laboratory, Northeastern University, USDA Forest Service" crop_map_predicted_${year}_250m_netcdf
ncatted -O -h -a Contact,global,o,c,"Venkata Shashank Konduri (konduri.v@husky.neu.edu)" crop_map_predicted_${year}_250m_netcdf
ncatted -O -h -a Data_DOI,global,o,c,"https://doi.org/10.5281/zenodo.3478336" crop_map_predicted_${year}_250m_netcdf
done

