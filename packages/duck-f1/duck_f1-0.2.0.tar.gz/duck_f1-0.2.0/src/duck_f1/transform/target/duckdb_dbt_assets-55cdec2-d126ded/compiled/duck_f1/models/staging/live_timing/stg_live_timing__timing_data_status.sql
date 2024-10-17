with
raw_timing_data_status as (
        

        select *
        from "f1"."ingress"."live_timing__timing_data_status"

    
),

formatted as (
    select
        driver,
        metricname as metric_name,
        metricvalue as metric_value,
        _streamtimestamp as _stream_ts,
        
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_timing_data_status
)

select *
from formatted