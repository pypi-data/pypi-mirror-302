
  
  create view "f1"."mart"."mart_dim_circuits__dbt_tmp" as (
    select
    "circuit_id",
  "circuit_ref",
  "circuit_name",
  "circuit_location",
  "circuit_country",
  "latitude",
  "longitude",
  "altitude",
  "wikipedia_url"
from "f1"."staging"."stg_ergast__circuits"
  );
