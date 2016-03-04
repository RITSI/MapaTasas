#!/bin/bash
# Clean maps

if [ -f ../esp.json ]
then
mv ../esp.json ../esp.json.bak
fi

if [ -f subunits.json ]
then
mv subunits.json subunits.json.bak
fi

ogr2ogr -f GeoJSON -where "iso_a2 = 'ES'" subunits.json ne_10m_admin_1_states_provinces.shp 
topojson -o ../esp.json subunits.json -p name,name_alt --id-property name_alt
