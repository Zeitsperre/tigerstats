-- For use with TIGER US CENSUS shapefiles loaded in PostgreSQL with PostGIS

-- SPATIAL REFERENCE ID (SRID) MUST BE SET AT LOADING (EPSG:4269)
-- ST_Transformation needed for GCS to Projected CRS (EPSG:5070; More research needed to determine the accuracy of this CRS for Lower 48 States)

-- Query 0: Extract values from Census 2000 counties shapefile 

DROP TABLE IF EXISTS analysis;
SELECT name, gid, state, county, lsad_trans lsad, area, perimeter, st_transform(geom, 5070) geom 
INTO analysis
FROM counties_2000
WHERE state < '60';

DROP TABLE IF EXISTS raf;
DROP TABLE IF EXISTS circle_boundary;
DROP TABLE IF EXISTS circle_perim_eq;
DROP TABLE IF EXISTS circle_area_eq;
DROP TABLE IF EXISTS hulls;

-- Query 1: The ratio of the area to the product of the maximum width and length of the area, which we will refer to as the rectangular area fraction (RAF);

SELECT 
	name,
	gid,
	state,
	county,
	lsad,
	area,
	perimeter,
	st_Envelope(geom) AS geom,
	st_Area(geom) AS calc_area,	
	st_Area(st_Envelope(geom)) AS boundbox_area,
	st_Area(geom) / st_Area(st_Envelope(geom)) AS rect_area_fraction
INTO raf
FROM analysis
--To remove Alaska Aleutians West
WHERE st_XMax(geom) < 4000000;

-- Query 2: The ratio of the area to the area of the smallest circle that can enclose the area;

SELECT 
	name,
	gid,
	state,
	county,
	lsad,
	area,
	perimeter,
	st_MinimumBoundingCircle(geom) AS geom,
	st_Area(geom) AS calc_area,
	st_Area(st_MinimumBoundingCircle(geom)) AS boundcircle_area, 
	st_Area(geom)/st_Area(st_MinimumBoundingCircle(geom)) AS area_boundcircle_ratio 
INTO circle_boundary
FROM analysis
--To remove Alaska Aleutians West
WHERE st_XMax(geom) < 4000000;

-- Query 3: The ratio of the area to the area of a circle with the same perimeter;

SELECT 
	name,
	gid,
	state,
	county,
	lsad,
	area,
	perimeter,
	st_Buffer(st_Centroid(geom),(st_Perimeter(geom)/(2*PI()))) AS geom,	
	st_Area(geom) AS calc_area,
	st_Perimeter(geom) AS calc_perimeter,	
	st_Area(st_Buffer(st_Centroid(geom),(st_Perimeter(geom)/(2*PI())))) AS perimcircle_area,
	st_Area(geom)/st_Area(st_Buffer(st_Centroid(geom),(st_Perimeter(geom)/(2*PI())))) AS perimcircle_ratio
INTO circle_perim_eq
FROM analysis
--To remove Alaska Aleutians West
WHERE st_XMax(geom) < 4000000;

-- Query 4: The ratio of the area's perimeter to that of a circle with the same area as the area;

SELECT 
	name,
	gid,
	state,
	county,
	lsad,
	area,
	perimeter,
	st_Buffer(st_Centroid(geom),(sqrt(st_Area(geom)/PI()))) AS geom,	
	st_Area(geom) AS calc_area,
	st_Perimeter(geom) AS calc_perimeter,	
	st_Perimeter(st_Buffer(st_Centroid(geom),(sqrt(st_Area(geom)/PI())))) AS areacircle_perimeter,
	st_Area(geom)/st_Area(st_Buffer(st_Centroid(geom),(sqrt(st_Area(geom)/PI())))) AS areacircle_ratio,
	st_Perimeter(geom)/st_Perimeter(st_Buffer(st_Centroid(geom),(sqrt(st_Area(geom)/PI())))) AS areacircle_perim_ratio
INTO circle_area_eq
FROM analysis
--To remove Alaska Aleutians West
WHERE st_XMax(geom) < 4000000;

-- Query 5: The ratio of the area to the area of its convex hull, the convex ratio;

SELECT 
	name,
	gid,
	state,
	county,
	lsad,
	area,
	perimeter,
	st_ConvexHull(geom) AS geom,
	st_Area(geom) AS calc_area,
	st_Area(st_ConvexHull(geom)) AS convexhull_area,
	st_Area(geom)/st_Area(st_ConvexHull(geom)) AS convexhull_area_ratio
INTO hulls
FROM analysis
--To remove Alaska Aleutians West
WHERE st_XMax(geom) < 4000000;

-- ALL QUERIES REQUIRE OPTIMIZATION/REVISION FOR RESOURCE USE

--Query 6: Append all metrics to a new geometry table with standard counties geometries

DROP TABLE IF EXISTS county_metrics;

SELECT 
	analysis.name AS name,
	analysis.gid AS gid,
	analysis.state AS state,
	analysis.county AS county,
	analysis.lsad AS lsad, 
	analysis.area AS area,
	analysis.perimeter AS perimeter,
	raf.calc_area AS calc_area,
	raf.boundbox_area AS boundbox_area,
	raf.rect_area_fraction AS rect_area_fraction,
	circle_boundary.boundcircle_area AS boundcircle_area,
	circle_boundary.area_boundcircle_ratio AS boundcircle_ratio,
	circle_perim_eq.calc_perimeter AS calc_perimeter,
	circle_perim_eq.perimcircle_area AS perimcircle_area,
	circle_perim_eq.perimcircle_ratio AS perimcircle_area_ratio,
	circle_area_eq.areacircle_perimeter AS areacircle_perim,
	circle_area_eq.areacircle_perim_ratio AS areacircle_perim_ratio,
	hulls.convexhull_area AS convexhull_area,
	hulls.convexhull_area_ratio AS convexhull_ratio,
	analysis.geom AS geom
INTO counties_2000_metrics
FROM (((((
	analysis INNER JOIN raf ON analysis.gid=raf.gid)
	INNER JOIN circle_boundary ON analysis.gid=circle_boundary.gid) 
	INNER JOIN circle_perim_eq ON analysis.gid=circle_perim_eq.gid)
	INNER JOIN circle_area_eq ON analysis.gid=circle_area_eq.gid)
	INNER JOIN hulls ON analysis.gid=hulls.gid)
WHERE st_XMax(analysis.geom) < 4000000;