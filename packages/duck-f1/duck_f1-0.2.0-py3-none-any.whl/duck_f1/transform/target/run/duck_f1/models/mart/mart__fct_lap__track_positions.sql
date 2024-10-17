
  
  create view "f1"."mart"."mart__fct_lap__track_positions__dbt_tmp" as (
    select *
from "f1"."staging"."stg_ergast__lap__positions"
  );
