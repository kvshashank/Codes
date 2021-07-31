## This code downloads the MODIS data for the period 2001-2020 for the cerrado region (covering 5 MODIS tiles h12v10 h12v11 h13v09 h13v10 h13v11)

dates=$(curl --silent https://e4ftl01.cr.usgs.gov/MOTA/MCD64A1.006/ | grep -oP '(?<=<a href=").*?(?=/">)' | awk 'NR>1' | sed '/2000./d' | sed '/2021./d')


for date in ${dates}; do

link=https://e4ftl01.cr.usgs.gov/MOTA/MCD64A1.006/${date}/

for tile in h12v10 h12v11 h13v09 h13v10 h13v11
do
file_code=$(curl --silent ${link} | grep -oP '(?<=href="MCD64A1.).*?(?=.hdf">)' | grep ${tile})
file_pattern=MCD64A1.${file_code}.hdf

wget --user=konduri.v_20 --password=#Shanks20 https://e4ftl01.cr.usgs.gov/MOTA/MCD64A1.006/${date}/${file_pattern}

done
done
