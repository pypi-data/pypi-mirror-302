select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select race_id
from "f1"."mart"."fct_race__driver_fastest_lap"
where race_id is null



      
    ) dbt_internal_test