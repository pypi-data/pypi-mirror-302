
    
    

select
    event_id || '-' || driver_id as unique_field,
    count(*) as n_records

from "f1"."mart"."fct_standings__drivers"
where event_id || '-' || driver_id is not null
group by event_id || '-' || driver_id
having count(*) > 1


