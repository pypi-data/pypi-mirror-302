
  
  create view "f1"."mart"."fct_session__drivers__dbt_tmp" as (
    select *
from "f1"."staging"."stg_ergast__lap__positions"
  );
