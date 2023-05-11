#!/bin/bash

for _ in $(seq 10) ; do
  # IWLIST_OUTPUT="$(iwlist wlan0 scan)"
  IWLIST_OUTPUT="$(iwlist wlan1 scan)"
  # iwlist wlan0 scan | grep -e "level" -e "Address" | sed 'N;s/\n//' | grep "00:11:32:" | cut -d " " -f 15- | sort | cut -d "-" -f 2 | cut -d " " -f 1 | paste -sd ' '
  /usr/bin/python3 formattor.py "${IWLIST_OUTPUT}"

  echo -en "===\n"
  sleep 1s
done
