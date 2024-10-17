select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select session_id
from "f1"."mart"."fct_session__drivers"
where session_id is null



      
    ) dbt_internal_test