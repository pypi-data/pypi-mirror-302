
    
    

select
    race_id || '-' || driver_id as unique_field,
    count(*) as n_records

from "f1"."mart"."fct_standings__drivers"
where race_id || '-' || driver_id is not null
group by race_id || '-' || driver_id
having count(*) > 1


