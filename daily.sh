#!/bin/bash
datestr=$(date '+%Y-%m-%d')
source /home/jane/anaconda3/bin/activate
cd /home/jane/python/tradeML
python stock_persist.py data/highvol_watchlist.json > dailyoutput/stock_persist_"${datestr}" 2>&1&
for i in Default sp500 dowjones nasdaq100
do 
   filename="data/$i.json"
   echo "getting watch list $filename"
   python optionML.py -w "$filename" -c 2048 -t option_chain -o data >> dailyoutput/$i_"$datestr" 2>&1
done
short_date_str=`echo $(date '+%Y%m%d')  | cut -c3-`
ls -lrt data/*/${short_date_str}_option_chain.csv | wc -l >> dailyoutput/$i_"${datestr}" 

