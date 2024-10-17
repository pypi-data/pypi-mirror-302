
    
    

select
    event_id as unique_field,
    count(*) as n_records

from "f1"."mart"."mart_dim_events"
where event_id is not null
group by event_id
having count(*) > 1


