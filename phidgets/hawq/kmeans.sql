drop table if exists phidgets.spatial_points;

create table phidgets.spatial_points (
rcvts timestamp,
points double precision[]);

insert into phidgets.spatial_points 
select accel.rcvts, array [accel.x, accel.y, accel.z]
from phidgets.spatial_acceleration accel;

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