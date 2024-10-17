
    
    

select
    constructor_id as unique_field,
    count(*) as n_records

from "f1"."mart"."mart_dim_constructors"
where constructor_id is not null
group by constructor_id
having count(*) > 1


