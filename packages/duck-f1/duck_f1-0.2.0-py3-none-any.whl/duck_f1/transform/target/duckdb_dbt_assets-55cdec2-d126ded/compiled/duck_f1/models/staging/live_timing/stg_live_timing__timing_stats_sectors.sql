with
raw_timing_stats_sectors as (
        

        select *
        from "f1"."ingress"."live_timing__timing_stats_sectors"

    
),

formatted as (
    select
        sectorkey as sector_key,
        value as sector_time,
        position,
        driver,
        _streamtimestamp as _stream_ts,
        
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_timing_stats_sectors
)

select *
from formatted