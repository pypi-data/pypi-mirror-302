
    
    

select
    event_id || '-' || constructor_id as unique_field,
    count(*) as n_records

from "f1"."mart"."fct_standings__constructors"
where event_id || '-' || constructor_id is not null
group by event_id || '-' || constructor_id
having count(*) > 1


