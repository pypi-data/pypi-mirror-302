select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select status_id
from "f1"."mart"."dim_status"
where status_id is null



      
    ) dbt_internal_test