with
raw_driver_race_info as (
    

        select *
        from "f1"."ingress"."live_timing__driver_race_info"

    
),

formatted as (
    select
        race_info.driver as driver_number,
        race_info.position as track_position,
        race_info.gap as gap_to_leader,
        race_info.interval,
        race_info.pitstops as pitstop_count,
        race_info.catching as is_catching,
        race_info.overtakestate as overtake_count,
        race_info.isout as is_out,
        race_info._streamtimestamp as _stream_ts,
        
    season_round as season_round,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_driver_race_info as race_info
)

select *
from formatted