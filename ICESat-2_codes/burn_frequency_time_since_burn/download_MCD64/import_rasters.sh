g.mapset mapset=map1 location=MCD64
g.region rast=test@PERMANENT -p

files=$(ls A*.tif)

for file in ${files}; do
name=$(echo ${file} | cut -d"." -f1)
r.in.gdal input=${file} output=${name} 
done
