
    
    

select
    event_id || '-' || constructor_id || '-' || driver_id as unique_field,
    count(*) as n_records

from "f1"."mart"."fct_qualifying__driver_classification"
where event_id || '-' || constructor_id || '-' || driver_id is not null
group by event_id || '-' || constructor_id || '-' || driver_id
having count(*) > 1


