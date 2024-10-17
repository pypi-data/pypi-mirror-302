
    
    

select
    status_id as unique_field,
    count(*) as n_records

from "f1"."mart"."mart_dim_status"
where status_id is not null
group by status_id
having count(*) > 1


