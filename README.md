# tigerstats
Scripts for creating a PostGIS-enabled PostgreSQL database for the purposes of loading United States Census shapefiles, calculating spatial statistics based on geographical characteristics, and outputting joined results tables. 

_This is currently a work in progress! Run at your own peril!_

## Purpose

This repository is a practice project meant to provide a Python automated method for users to perform several GIS analyses on shapefiles from within a PostGIS-enabled database. The goal is to have Shapefiles loaded from the "/data" folder into a new database where scripts can run based on identical filenames, resulting in a series of tables organized by unique identifiers.

The statistics calculated here are meant to examine particularities in the shapes of United States COUNTY and PLACE shapefiles to aid in tracking geographic changes between census periods.

## Variables

gid = Unique GID for feature

name = Feature name

state = State id #

county = County id #

place = Place id #

lsad = Legal classification for place or county

area = The total area of the feature as reported

aland = The area of land as reported

awater = The area of water as reported

total\_area = The sum of aland and awater

calc\_area = The area as calculated using PostGIS (st_area())

boundbox\_area = The product of the maximum width and length of the feature (rectangular area fraction)

rect\_area\_fraction = The ratio of the area of the feature to the product of the maximum width and length of the feature (RAF)

boundcircle\_area =The area of the smallest circle that can enclose the feature

boundcircle\_ratio = The ratio of the area of the feature to the area of the smallest circle that can enclose the feature

perimeter = calculated perimeter of the feature

perimcircle\_area = The area of a circle with the same perimeter as the feature

perimcircle\_area\_ratio = The ratio of the area of a feature to the area of a circle with the same perimeter as the feature

areacircle\_perim = The perimeter of a circle with the same area as the feature

areacircle\_perim\_ratio = The ratio of a feature's perimeter to the perimeter of a circle with the same area as the feature

convexhull\_area = the area of a feature's convex hull

convexhull\_ratio = The ratio of the area of a feature to the area of its convex hull (convex ratio)

## Requirements

PostgreSQL
PostGIS
Python 2/3
psycopg2
