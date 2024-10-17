
  
  create view "f1"."mart"."dim_seasons__dbt_tmp" as (
    select
    "year",
  "url",
  "season_id"
from "f1"."staging"."stg_ergast__seasons"
  );
