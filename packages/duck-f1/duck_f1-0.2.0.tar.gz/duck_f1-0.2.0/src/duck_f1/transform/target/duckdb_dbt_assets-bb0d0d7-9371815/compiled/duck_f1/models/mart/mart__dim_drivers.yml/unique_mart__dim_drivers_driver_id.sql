
    
    

select
    driver_id as unique_field,
    count(*) as n_records

from "f1"."mart"."dim_drivers"
where driver_id is not null
group by driver_id
having count(*) > 1


