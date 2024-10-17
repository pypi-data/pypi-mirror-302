with
raw_lap_count as (
        

        select * from "f1"."ingress"."live_timing__lap_count"

    
),

formatted as (
    select
        metric as metric_lable,
        value as metric_value,
        _streamtimestamp as _stream_ts,
        
    season_round as season_round,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_lap_count
)

select *
from formatted