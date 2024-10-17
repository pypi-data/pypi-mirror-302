
    
    

select
    session_id || '-' || driver_id as unique_field,
    count(*) as n_records

from "f1"."mart"."fct_session__drivers"
where session_id || '-' || driver_id is not null
group by session_id || '-' || driver_id
having count(*) > 1


