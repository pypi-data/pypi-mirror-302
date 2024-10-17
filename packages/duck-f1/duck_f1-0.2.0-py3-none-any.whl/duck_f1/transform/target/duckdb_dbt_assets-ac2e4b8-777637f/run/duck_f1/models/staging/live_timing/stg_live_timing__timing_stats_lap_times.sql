
  
  create view "f1"."staging"."stg_live_timing__timing_stats_lap_times__dbt_tmp" as (
    with
raw_timing_stats_lap_times as (
        

        select *
        from "f1"."ingress"."live_timing__timing_stats_lap_times"

    
),

formatted as (
    select
        value as lap_time,
        lap,
        position,
        driver as driver_number,
        _streamtimestamp as _stream_ts,
        
    season_round as season_round,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_timing_stats_lap_times
)

select *
from formatted
  );
