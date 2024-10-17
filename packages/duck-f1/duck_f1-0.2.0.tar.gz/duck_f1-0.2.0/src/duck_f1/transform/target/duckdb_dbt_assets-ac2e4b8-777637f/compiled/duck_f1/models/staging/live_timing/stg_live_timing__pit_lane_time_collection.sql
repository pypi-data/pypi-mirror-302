with
raw_pit_lane_time_collection as (
        

        select *
        from
                "f1"."ingress"."live_timing__pit_lane_time_collection"

    
),

formatted as (
    select
        driver,
        duration as pit_lane_time_duration,
        lap as lap_number,
        _streamtimestamp as _stream_ts,
        
    season_round as season_round,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_pit_lane_time_collection
)

select *
from formatted