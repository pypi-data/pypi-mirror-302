
  
  create view "f1"."mart"."mart_dim_events__dbt_tmp" as (
    select
    "event_id",
  "circuit_id",
  "season",
  "round",
  "event_country",
  "event_location",
  "event_name",
  "event_official_name",
  "wikipedia_url"
from "f1"."staging"."stg_events"
  );
