
  
  create view "f1"."mart"."mart__dim_status__dbt_tmp" as (
    select
    "status_id",
  "status"
from "f1"."staging"."stg_ergast__status"
  );
