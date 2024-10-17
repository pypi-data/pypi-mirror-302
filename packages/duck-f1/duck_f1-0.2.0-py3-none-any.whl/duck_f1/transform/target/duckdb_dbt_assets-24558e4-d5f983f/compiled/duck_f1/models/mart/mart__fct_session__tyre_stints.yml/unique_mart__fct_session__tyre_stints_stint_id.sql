
    
    

select
    stint_id as unique_field,
    count(*) as n_records

from "f1"."mart"."fct_session__tyre_stints"
where stint_id is not null
group by stint_id
having count(*) > 1


