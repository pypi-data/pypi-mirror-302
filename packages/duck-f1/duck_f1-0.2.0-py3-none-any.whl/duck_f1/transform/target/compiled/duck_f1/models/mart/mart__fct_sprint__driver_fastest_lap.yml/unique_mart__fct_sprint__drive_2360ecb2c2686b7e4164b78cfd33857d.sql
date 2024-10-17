
    
    

select
    race_id || '-' || constructor_id || '-' || driver_id as unique_field,
    count(*) as n_records

from "f1"."mart"."fct_sprint__driver_fastest_lap"
where race_id || '-' || constructor_id || '-' || driver_id is not null
group by race_id || '-' || constructor_id || '-' || driver_id
having count(*) > 1


