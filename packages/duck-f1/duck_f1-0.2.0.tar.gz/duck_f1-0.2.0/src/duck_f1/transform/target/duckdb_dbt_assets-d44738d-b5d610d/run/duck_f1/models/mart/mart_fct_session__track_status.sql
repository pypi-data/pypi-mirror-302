
  
  create view "f1"."mart"."mart_fct_session__track_status__dbt_tmp" as (
    select *
from "f1"."staging"."stg_live_timing__weather_data"
  );
