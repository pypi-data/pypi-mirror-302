select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select race_id
from "f1"."mart"."dim_races"
where race_id is null



      
    ) dbt_internal_test