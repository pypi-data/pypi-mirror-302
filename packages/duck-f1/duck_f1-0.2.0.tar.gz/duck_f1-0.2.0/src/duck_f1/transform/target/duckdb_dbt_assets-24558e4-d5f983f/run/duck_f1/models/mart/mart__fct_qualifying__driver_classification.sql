
  
  create view "f1"."mart"."fct_qualifying__driver_classification__dbt_tmp" as (
    select *
from "f1"."staging"."stg_ergast__qualifying__driver_classification"
  );
