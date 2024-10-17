
  
  create view "f1"."staging"."stg_live_timing__lap_series__dbt_tmp" as (
    with
raw_lap_series as (
        

        select * from "f1"."ingress"."live_timing__lap_series"

    
),

formatted as (
    select
        drivernumber as driver_number,
        lapnumber as lap_number,
        lapposition as lap_position,
        _streamtimestamp as _stream_ts,
        
    md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as event_id,
    event_round_number,
    event_sha,
    event_country,
    event_date,
    event_name,
    md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(session_type as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as session_id,
    session_sha,
    session_type,
    session_date

    from raw_lap_series
)

select *
from formatted
  );
