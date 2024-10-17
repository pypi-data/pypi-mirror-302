
    
    

select
    lap_id || '-' || race_id || '-' || driver_id as unique_field,
    count(*) as n_records

from "f1"."mart"."fct_lap__positions"
where lap_id || '-' || race_id || '-' || driver_id is not null
group by lap_id || '-' || race_id || '-' || driver_id
having count(*) > 1


