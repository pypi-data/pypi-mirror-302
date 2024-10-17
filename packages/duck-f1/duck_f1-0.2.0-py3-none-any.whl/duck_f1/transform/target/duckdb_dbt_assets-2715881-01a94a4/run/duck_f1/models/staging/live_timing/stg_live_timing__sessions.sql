
  
  create view "f1"."staging"."stg_live_timing__sessions__dbt_tmp" as (
    with
raw_sessions as (
    select * from "f1"."ingress"."live_timing__sessions"
),

formatted as (
    select
        md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as event_id,
        md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(session_type as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as session_id,
        session_sha as _live_timing_session_sha,
        session_type,
        session_name,
        session_date as session_timestamp_local
    from raw_sessions
    where event_round_number > 0
)

select *
from formatted
  );
