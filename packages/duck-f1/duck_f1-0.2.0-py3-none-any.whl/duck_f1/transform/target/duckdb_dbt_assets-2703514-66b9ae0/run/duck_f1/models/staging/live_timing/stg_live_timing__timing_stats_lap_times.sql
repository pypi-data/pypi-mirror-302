
  
  create view "f1"."staging"."stg_live_timing__timing_stats_lap_times__dbt_tmp" as (
    with
raw_timing_stats_lap_times as (
        

        select *
        from "f1"."ingress"."live_timing__timing_stats_lap_times"

    
),

computed as (
    select
        
    to_milliseconds(
        (split_part(value, ':', 1)::integer * 60 * 1000)
        + (floor(split_part(value, ':', 2)::double)::integer * 1000)
        + (split_part(value, '.', 2)::integer)
    )
 as lap_time,
        lap as lap_number,
        position,
        driver as car_number,
        _streamtimestamp::interval as _stream_ts,
        
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

    from raw_timing_stats_lap_times
    where len(value) > 0
),

formatted as (
    select
        session_id,
        car_number,
        lap_number,
        lap_time,
        position,
        _stream_ts
    from computed
)

select *
from formatted
  );
