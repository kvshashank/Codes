## Data for this is available at /home/vk5/create_confusion_matrix
awk '$1==1 || $1==5 || $1==24 || $1==61 || $1==37 || $1==36 || $1==4 || $1==3' r.stats_phenoreclassed_cdl_2015_24 > r.stats_sub1_24
awk '$2==1 || $2==5 || $2==24 || $2==61 || $2==37 || $2==36 || $2==4 || $2==3' r.stats_sub1_24 > r.stats_sub2_24
