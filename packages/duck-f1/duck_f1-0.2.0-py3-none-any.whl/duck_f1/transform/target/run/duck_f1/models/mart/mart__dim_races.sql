
  
  create view "f1"."mart"."mart__dim_races__dbt_tmp" as (
    select
    "session_type",
  "event_id",
  "session_id",
  "circuit_id",
  "year",
  "round",
  "name",
  "date",
  "event_time",
  "race_time_utc",
  "wikipedia_url",
  "fp1_date",
  "fp1_time",
  "fp2_date",
  "fp2_time",
  "fp3_date",
  "fp3_time",
  "quali_date",
  "quali_time",
  "sprint_date",
  "sprint_time"
from "f1"."staging"."stg_ergast__races"
  );
