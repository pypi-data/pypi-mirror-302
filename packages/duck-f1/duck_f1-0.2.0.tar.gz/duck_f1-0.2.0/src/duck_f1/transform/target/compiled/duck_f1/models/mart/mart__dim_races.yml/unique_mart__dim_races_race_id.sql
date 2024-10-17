
    
    

select
    race_id as unique_field,
    count(*) as n_records

from "f1"."mart"."dim_races"
where race_id is not null
group by race_id
having count(*) > 1


