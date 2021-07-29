## Extract tif files from HDF 
cd /home/vk5/icesat_2/MCD64/raw_hdfs
files=$(ls *.hdf)
for file in ${files}; do
file_code=$(echo ${file} | cut -d"." -f2)

## Extract 3 tif files from each hdf file
gdal_translate -sds -of GTiff ${file} ${file_code}.tif
rm ${file_code}_4.tif ${file_code}_5.tif
mv ${file_code}_1.tif ${file_code}_burn_date.tif
mv ${file_code}_2.tif ${file_code}_burn_data_uncertainty.tif
mv ${file_code}_3.tif ${file_code}_qa.tif
mv ${file_code}_burn_date.tif ${file_code}_burn_data_uncertainty.tif ${file_code}_qa.tif /home/vk5/icesat_2/MCD64/tifs
done
