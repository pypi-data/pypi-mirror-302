with
raw_current_tyres as (
        

        select * from "f1"."ingress"."live_timing__current_tyres"

    
),

formatted as (
    select
        driver as driver_number,
        compound as tyre_compound,
        new as is_new,
        _streamtimestamp as _stream_ts,
        
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_current_tyres
)

select *
from formatted