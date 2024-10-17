
  
  create view "f1"."staging"."stg_live_timing__heartbeat__dbt_tmp" as (
    with
raw_heartbeat as (
        

        select * from "f1"."ingress"."live_timing__heartbeat"

    
),

formatted as (
    select
        utc::timestamp as utc_ts,
        _streamtimestamp::interval as session_ts,
        utc_ts - session_ts as start_utc,
        
    md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as event_id,
    event_round_number,
    event_sha,
    event_country,
    event_date as event_start_local,
    event_name,
    md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(session_type as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as session_id,
    session_sha,
    session_type,
    session_date as session_start_local

    from raw_heartbeat
)

select *
from formatted
  );
