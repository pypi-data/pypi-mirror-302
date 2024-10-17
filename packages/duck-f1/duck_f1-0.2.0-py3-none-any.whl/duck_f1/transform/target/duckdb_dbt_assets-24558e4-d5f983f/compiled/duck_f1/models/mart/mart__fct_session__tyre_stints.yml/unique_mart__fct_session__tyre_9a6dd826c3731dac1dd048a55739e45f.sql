
    
    

select
    session_id || '-' || driver_id || '-' || stint_id as unique_field,
    count(*) as n_records

from "f1"."mart"."fct_session__tyre_stints"
where session_id || '-' || driver_id || '-' || stint_id is not null
group by session_id || '-' || driver_id || '-' || stint_id
having count(*) > 1


