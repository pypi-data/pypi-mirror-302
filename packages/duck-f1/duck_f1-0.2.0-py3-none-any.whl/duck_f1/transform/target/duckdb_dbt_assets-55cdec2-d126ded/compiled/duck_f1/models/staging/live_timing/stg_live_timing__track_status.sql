with
raw_track_status as (
        

        select * from "f1"."ingress"."live_timing__track_status"

    
),

formatted as (
    select
        status as status_id,
        message as status_message,
        _streamtimestamp as _stream_ts,
        
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_track_status
)

select *
from formatted