with
raw_session_data as (
        

        select * from "f1"."ingress"."live_timing__session_data"

    
),

formatted as (
    select
        key as serie_key,
        utc as utc_ts,
        metricname as metric_name,
        metricvalue as metric_value,
        
    season_round as season_round,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_session_data
)

select *
from formatted