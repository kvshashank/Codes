for year in `seq 2008 2012`; do
for band in `seq 1 9`; do
g.rename raster=MCD13.A${year}.band${band},MCD13.A${year}.band0${band} 
done
done
