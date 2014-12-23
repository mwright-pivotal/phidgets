DROP EXTERNAL TABLE IF EXISTS phidgets.ext_csv_phidget_spatial;
CREATE EXTERNAL TABLE phidgets.ext_csv_phidget_spatial (
	type varchar(10),
	serialnum varchar(8),
	rcvts timestamp ,
	x double precision ,
	y double precision ,
	z double precision
	)
	LOCATION ('pxf://hdm:8020/xd/phidget-stream/*.txt?PROFILE=HdfsTextSimple')
	-- LOCATION ('gpfdist://uc1epivphdmst01.local:8000/hierarchies/SL/local_hier_prod1.csv')
	FORMAT 'CSV' ( HEADER DELIMITER ',' NULL AS '' escape '"' quote '"' FILL MISSING FIELDS)
	ENCODING 'WIN1252';

DROP TABLE IF EXISTS phidgets.spatial_acceleration;

CREATE TABLE phidgets.spatial_acceleration (
	serialnum varchar(8),
	rcvts	timestamp,
	x double precision ,
	y double precision ,
	z double precision,
	tilt double precision
	)
WITH (APPENDONLY=true, ORIENTATION=Parquet, 
  OIDS=FALSE
)
DISTRIBUTED RANDOMLY;

INSERT INTO phidgets.spatial_acceleration
SELECT serialnum,rcvts,x,y,z,180/3.14 * (asin(x) + asin(y)) FROM phidgets.ext_csv_phidget_spatial
WHERE type = 'accel';

DROP TABLE IF EXISTS phidgets.spatial_angular;

CREATE TABLE phidgets.spatial_angular (
	serialnum varchar(8),
	rcvts	timestamp,
	x double precision ,
	y double precision ,
	z double precision
	)
WITH (APPENDONLY=true, ORIENTATION=Parquet, 
  OIDS=FALSE
)
DISTRIBUTED RANDOMLY;

INSERT INTO phidgets.spatial_angular
SELECT serialnum,rcvts,x,y,z FROM phidgets.ext_csv_phidget_spatial
WHERE type = 'angular';

DROP TABLE IF EXISTS phidgets.spatial_magnetic;

CREATE TABLE phidgets.spatial_magnetic (
	serialnum varchar(8),
	rcvts	timestamp,
	x double precision ,
	y double precision ,
	z double precision
	)
WITH (APPENDONLY=true, ORIENTATION=Parquet, 
  OIDS=FALSE
)
DISTRIBUTED RANDOMLY;

INSERT INTO phidgets.spatial_magnetic
SELECT serialnum,rcvts,x,y,z FROM phidgets.ext_csv_phidget_spatial
WHERE type = 'magnetic';

DROP TABLE IF EXISTS phidgets.spatial_gps;

CREATE TABLE phidgets.spatial_gps (
	serialnum varchar(8),
	rcvts	timestamp,
	lat double precision ,
	long double precision ,
	altitude double precision
	)
WITH (APPENDONLY=true, ORIENTATION=Parquet, 
  OIDS=FALSE
)
DISTRIBUTED RANDOMLY;

INSERT INTO phidgets.spatial_gps
SELECT serialnum,rcvts,x,y,z FROM phidgets.ext_csv_phidget_spatial
WHERE type = 'gps';