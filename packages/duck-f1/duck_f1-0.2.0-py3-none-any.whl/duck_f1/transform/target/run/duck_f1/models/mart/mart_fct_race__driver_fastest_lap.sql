
  
  create view "f1"."mart"."mart_fct_race__driver_fastest_lap__dbt_tmp" as (
    select *
from "f1"."staging"."stg_ergast__race__driver_fastest_lap"
  );
