
  
  create view "f1"."mart"."dim_drivers__dbt_tmp" as (
    select
    "driver_id",
  "driver_number",
  "driver_code",
  "first_name",
  "last_name",
  "full_name",
  "date_of_birth",
  "age_years",
  "age_days",
  "age_label",
  "nationality",
  "wikipedia_url"
from "f1"."staging"."stg_ergast__drivers"
  );
