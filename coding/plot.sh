# filename: plot.sh
curl https://www.macrotrends.net/stocks/charts/NVDA/nvidia/stock-price-history \
    | grep -oP '(?<=<td class="dt">(.*?)</td>).*?(?<=<td class="num right">)(.*?)</td>' \
    | sed 's/&nbsp;//g' \
    | awk -F ',' '{printf "%s %s\n", $1, $2}' > ./nvda.csv

curl https://www.macrotrends.net/stocks/charts/TSLA/tesla/stock-price-history \
    | grep -oP '(?<=<td class="dt">(.*?)</td>).*?(?<=<td class="num right">)(.*?)</td>' \
    | sed 's/&nbsp;//g' \
    | awk -F ',' '{printf "%s %s\n", $1, $2}' > ./tsla.csv

gnuplot -p -e '
set term png size 1920,1200
set output "TSLA and NVDA  stock chart.png"
set xdata time
set timefmt "%b %e"
set ylabel "Daily Closing Price (USD)"
set style data lines
set grid
set key right
plot "nvda.csv" using 1:2 with lines title "NVIDIA", \
     "tsla.csv" using 1:2 with lines title "Tesla"
'