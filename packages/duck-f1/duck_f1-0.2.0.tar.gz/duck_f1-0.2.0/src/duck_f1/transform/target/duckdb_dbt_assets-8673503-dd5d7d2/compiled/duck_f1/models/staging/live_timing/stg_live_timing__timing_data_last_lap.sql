with
raw_timing_data_last_lap as (
        

        select *
        from "f1"."ingress"."live_timing__timing_data_last_lap"

    
),

formatted as (
    select
        value as lap_time,
        status as lap_time_status,
        overallfastest as is_overall_fastest,
        personalfastest as is_personal_fastest,
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

    from raw_timing_data_last_lap
)

select *
from formatted