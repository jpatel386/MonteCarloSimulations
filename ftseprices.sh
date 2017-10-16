#!/bin/bash

wget --no-check-certificate https://www.advfn.com/stock-market/FTSE/UKX/historical/more-historical-data

cat  more-historical-data | head -379 | tail -1 > dates.file


sed 's/<tr class="odd"><td>/\
> /g' dates.file | sed 's/,//g' | sed -e 's/<[^>]*>/,/g' > hope.txt

sed -e '1d;' hope.txt > hope1.txt

awk -F',' '{print $1, $3, $5, $11, $13}' hope1.txt > final.file
