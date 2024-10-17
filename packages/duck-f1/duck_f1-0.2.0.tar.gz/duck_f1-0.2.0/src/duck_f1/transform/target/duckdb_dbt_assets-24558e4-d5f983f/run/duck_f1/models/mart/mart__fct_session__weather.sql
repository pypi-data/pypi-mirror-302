
  
  create view "f1"."mart"."fct_session__weather__dbt_tmp" as (
    select *
from "f1"."staging"."stg_live_timing__weather_data"
  );
