drop table if exists phidgets.spatial_points;

create table phidgets.spatial_points (
rcvts timestamp,
points double precision[]);

insert into phidgets.spatial_points 
select accel.rcvts, array [accel.x, accel.y, accel.z, ang.x, ang.y, ang.z, mag.x, mag.y, mag.z]
from phidgets.spatial_acceleration accel,phidgets.spatial_angular ang, phidgets.spatial_magnetic mag
where abs(EXTRACT(EPOCH FROM accel.rcvts) - EXTRACT(EPOCH FROM ang.rcvts)) < 1
and abs(EXTRACT(EPOCH FROM accel.rcvts) - EXTRACT(EPOCH FROM mag.rcvts)) < 1;

SELECT * FROM madlib.kmeanspp( 'phidgets.spatial_points',
                               'points',
                               5,
                               'madlib.squared_dist_norm2',
                               'madlib.avg',
                               20,
                               0.001
                             );
                             
                             SELECT data.*, (madlib.closest_column(centroids, points)).column_id as cluster_id
FROM public.km_sample as data,
     (SELECT centroids
      FROM madlib.kmeanspp('km_sample', 'points', 2,
                           'madlib.squared_dist_norm2',
                           'madlib.avg', 20, 0.001)) as centroids
ORDER BY data.pid;

select count(*) from phidgets.spatial_acceleration accel,phidgets.spatial_angular ang, phidgets.spatial_magnetic mag
where abs(EXTRACT(EPOCH FROM accel.rcvts) - EXTRACT(EPOCH FROM ang.rcvts)) < 1
and abs(EXTRACT(EPOCH FROM accel.rcvts) - EXTRACT(EPOCH FROM mag.rcvts)) < 1

select EXTRACT(EPOCH FROM TIMESTAMP WITH TIME ZONE accel.rcvts)
from phidgets.spatial_acceleration accel limit 100;