select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select session_sha
from "f1"."staging"."stg_live_timing__events"
where session_sha is null



      
    ) dbt_internal_test