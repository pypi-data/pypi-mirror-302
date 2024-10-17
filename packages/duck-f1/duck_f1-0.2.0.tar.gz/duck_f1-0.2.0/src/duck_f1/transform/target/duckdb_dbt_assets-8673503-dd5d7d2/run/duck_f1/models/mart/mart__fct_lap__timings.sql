
  
  create view "f1"."mart"."fct_lap__timings__dbt_tmp" as (
    select *
from "f1"."staging"."stg_ergast__lap__timings"
  );
