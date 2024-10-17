select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    event_id || '-' || constructor_id || '-' || driver_id as unique_field,
    count(*) as n_records

from "f1"."mart"."fct_sprint__driver_fastest_lap"
where event_id || '-' || constructor_id || '-' || driver_id is not null
group by event_id || '-' || constructor_id || '-' || driver_id
having count(*) > 1



      
    ) dbt_internal_test