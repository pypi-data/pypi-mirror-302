
  
  create view "f1"."mart"."dim_sessions__dbt_tmp" as (
    select
    "event_id",
  "session_id",
  "session_type",
  "session_name",
  "session_start_utc",
  "session_start_local"
from "f1"."staging"."stg_sessions"
  );
