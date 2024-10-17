with
raw_timing_data_sectors as (
        

        select *
        from "f1"."ingress"."live_timing__timing_data_sectors"

    
),

formatted as (
    select
        sectorkey as sector_key,
        stopped as is_stopped,
        value as sector_time,
        previousvalue as previous_value,
        status as sector_status,
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

    from raw_timing_data_sectors
)

select *
from formatted