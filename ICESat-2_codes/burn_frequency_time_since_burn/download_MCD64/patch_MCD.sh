### Copy rasters from other mapsets and run r.patch on each of the maps


####### Copy rasters from other mapsets #########
#for tile in h12v10 h12v11 h13v09 h13v10 h13v11
#do
#g.mapset mapset=mapset_${tile}
#maps=$(g.list type=raster pattern=${tile}_*burn_date_wo_uncertain_qa)
#
#g.mapset mapset=combined_tiles_cerrado location=MCD64
#g.region n=-0.000005 e=-4447802.078659 w=-6671703.117994 s=-3335851.559006 nsres=463.31271653 ewres=463.31271653 -p
#
#for map in ${maps}; do
#
#g.copy ${map}@mapset_${tile},${map}
#
#done
#done

####### Patch rasters #########
g.mapset mapset=combined_tiles_cerrado location=MCD64
g.region n=-0.000005 e=-4447802.078659 w=-6671703.117994 s=-3335851.559006 nsres=463.31271653 ewres=463.31271653 -p
maps=$(g.list type=raster pattern=h12v10_A*)
for map in ${maps}; do
code=$(echo ${map} | cut -d"_" -f2)

r.patch input=`g.list type=raster pattern=*${code}* separator=comma` output=${code}_burn_date_patched_map

done

