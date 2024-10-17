select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    lap_id as unique_field,
    count(*) as n_records

from "f1"."mart"."fct_lap__positions"
where lap_id is not null
group by lap_id
having count(*) > 1



      
    ) dbt_internal_test