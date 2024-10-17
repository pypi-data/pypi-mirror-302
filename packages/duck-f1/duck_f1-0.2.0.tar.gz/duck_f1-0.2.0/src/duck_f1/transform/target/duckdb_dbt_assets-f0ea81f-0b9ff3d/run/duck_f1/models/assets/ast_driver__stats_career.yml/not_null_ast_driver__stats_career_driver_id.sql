select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select driver_id
from "f1"."assets"."ast_driver__stats_career"
where driver_id is null



      
    ) dbt_internal_test