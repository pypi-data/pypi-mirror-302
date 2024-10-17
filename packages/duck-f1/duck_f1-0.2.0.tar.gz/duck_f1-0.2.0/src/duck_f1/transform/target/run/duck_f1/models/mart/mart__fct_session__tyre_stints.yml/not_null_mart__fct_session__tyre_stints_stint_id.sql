select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select stint_id
from "f1"."mart"."fct_session__tyre_stints"
where stint_id is null



      
    ) dbt_internal_test