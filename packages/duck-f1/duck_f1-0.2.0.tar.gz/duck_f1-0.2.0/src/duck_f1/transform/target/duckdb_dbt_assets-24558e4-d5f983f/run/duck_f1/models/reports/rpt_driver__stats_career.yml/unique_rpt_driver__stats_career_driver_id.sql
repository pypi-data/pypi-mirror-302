select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    driver_id as unique_field,
    count(*) as n_records

from "f1"."reports"."driver__stats_career"
where driver_id is not null
group by driver_id
having count(*) > 1



      
    ) dbt_internal_test