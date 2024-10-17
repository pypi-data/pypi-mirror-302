
    
    

select
    session_id as unique_field,
    count(*) as n_records

from "f1"."mart"."mart_dim_races"
where session_id is not null
group by session_id
having count(*) > 1


