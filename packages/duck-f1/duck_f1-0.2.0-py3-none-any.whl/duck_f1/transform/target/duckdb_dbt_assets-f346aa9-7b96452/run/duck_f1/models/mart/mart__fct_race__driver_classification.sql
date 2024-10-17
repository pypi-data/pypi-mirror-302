
  
  create view "f1"."mart"."fct_race__driver_classification__dbt_tmp" as (
    select *
from "f1"."staging"."stg_ergast__race__driver_classification"
  );
