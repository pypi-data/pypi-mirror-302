
    
    

select
    session_id || '-' || constructor_id as unique_field,
    count(*) as n_records

from "f1"."mart"."mart_fct_race__constructor_classification"
where session_id || '-' || constructor_id is not null
group by session_id || '-' || constructor_id
having count(*) > 1


