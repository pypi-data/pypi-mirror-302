select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select status_id
from "f1"."mart"."fct_sprint__driver_classification"
where status_id is null



      
    ) dbt_internal_test