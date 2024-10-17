select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select lap_id
from "f1"."mart"."fct_lap__positions"
where lap_id is null



      
    ) dbt_internal_test