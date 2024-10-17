
    
    

select
    lap_id as unique_field,
    count(*) as n_records

from "f1"."mart"."fct_car__positions"
where lap_id is not null
group by lap_id
having count(*) > 1


