
    
    

select
    session_id || '-' || driver_id || '-' || lap_id || '-' || session_ts as unique_field,
    count(*) as n_records

from "f1"."mart"."fct_car__telemetry"
where session_id || '-' || driver_id || '-' || lap_id || '-' || session_ts is not null
group by session_id || '-' || driver_id || '-' || lap_id || '-' || session_ts
having count(*) > 1


