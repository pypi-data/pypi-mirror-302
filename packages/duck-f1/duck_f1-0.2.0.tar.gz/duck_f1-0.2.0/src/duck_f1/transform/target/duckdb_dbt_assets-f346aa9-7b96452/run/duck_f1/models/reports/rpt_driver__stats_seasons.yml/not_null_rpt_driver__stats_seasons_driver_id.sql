select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select driver_id
from "f1"."reports"."driver__stats_seasons"
where driver_id is null



      
    ) dbt_internal_test