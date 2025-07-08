#!/bin/bash

MARSPATH="/work/cmcc/jd19424/test-ML/data/ECMWF/mars/"

TYPE="forecast"
# this example will filter the area of Europe (N/W/S/E) and interpolate the final fields to
# a 0.5x0.5 regular lat-lon grid (GRID=0.5/0.5)
AREA="10/-130/-10/110"
GRID="0.5/0.5"
  
# fixed selection from the same block
PARAMS="129.128" # 129: geopotential height
# LEVELIST="1000/850/700/500"
LEVELIST="500"
# STEP="0/to/90/by/1"
STEP="24"
  
# TIMES="0000 1200"
TIMES="0000"
# YEAR="2023"
# MONTH="01"

# DATE=""
YEAR="2023"
MONTH="01 02 03 04 05 06 07 08 09 10 11 12"
 
date loop
for y in ${YEAR}; do
 
  for m in ${MONTH}; do
    #get the number of days for this particular month/year
    days_per_month=$(cal ${m} ${y} | awk 'NF {DAYS = $NF}; END {print DAYS}')
 
    for my_date in $(seq -w 1 ${days_per_month}); do
      my_date=${YEAR}${m}${my_date}
 
      #time loop
      for my_time in ${TIMES}; do
        cat << EOF > ${MARSPATH}my_request_${my_date}_${my_time}.mars
RETRIEVE,
    CLASS      = OD,
    TYPE       = ${TYPE},
    STREAM     = OPER,
    EXPVER     = 0001,
    LEVTYPE    = "pressure level",
    GRID       = ${GRID},
    AREA       = ${AREA},
    LEVELIST   = ${LEVELIST},
    PARAM      = ${PARAMS},
    DATE       = ${my_date},
    TIME       = ${my_time},
    STEP       = ${STEP},
    TARGET     = "oper_ml_${my_date}_${my_time}.grib"
EOF
      mars ${MARSPATH}my_request_${my_date}_${my_time}.mars
      if [ $? -eq 0 ]; then
        rm -f my_request_${my_date}_${my_time}.mars
      fi
      done
    done
  done
done
