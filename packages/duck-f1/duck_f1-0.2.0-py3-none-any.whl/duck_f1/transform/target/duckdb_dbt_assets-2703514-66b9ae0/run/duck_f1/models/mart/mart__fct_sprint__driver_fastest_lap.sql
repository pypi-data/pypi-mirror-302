
  
  create view "f1"."mart"."fct_sprint__driver_fastest_lap__dbt_tmp" as (
    select *
from "f1"."staging"."stg_ergast__sprint__driver_fastest_lap"
  );
