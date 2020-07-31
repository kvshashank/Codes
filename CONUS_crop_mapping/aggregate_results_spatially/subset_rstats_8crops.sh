for file in $(ls r.stats_2018_county_cdl_count*); do
awk '$2==1 || $2==5 || $2==24 || $2==61 || $2==37 || $2==36 || $2==4 || $2==3' ${file} > ${file}_8crops
done
