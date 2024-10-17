
    
    

select
    session_id || '-' || constructor_id || '-' || driver_id as unique_field,
    count(*) as n_records

from "f1"."mart"."mart_fct_sprint__driver_classification"
where session_id || '-' || constructor_id || '-' || driver_id is not null
group by session_id || '-' || constructor_id || '-' || driver_id
having count(*) > 1


