with
raw_timing_stats_speeds as (
        

        select *
        from "f1"."ingress"."live_timing__timing_stats_speeds"

    
),

formatted as (
    select
        speedtrapkey as speed_trap_key,
        value as speed,
        position,
        driver,
        _streamtimestamp as _stream_ts,
        
    season_round as season_round,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_timing_stats_speeds
)

select *
from formatted