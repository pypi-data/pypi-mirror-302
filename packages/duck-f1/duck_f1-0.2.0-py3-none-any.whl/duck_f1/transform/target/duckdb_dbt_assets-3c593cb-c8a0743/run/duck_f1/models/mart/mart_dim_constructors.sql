
  
  create view "f1"."mart"."mart_dim_constructors__dbt_tmp" as (
    select
    "constructor_id",
  "constructor_reference",
  "constructor_name",
  "nationality",
  "wikipedia_url"
from "f1"."staging"."stg_ergast__constructors"
  );
