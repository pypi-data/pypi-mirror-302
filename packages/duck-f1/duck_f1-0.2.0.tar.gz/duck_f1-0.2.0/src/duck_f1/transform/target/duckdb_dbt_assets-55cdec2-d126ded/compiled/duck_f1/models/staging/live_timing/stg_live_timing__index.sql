with
raw_index as (
        

        select * from "f1"."ingress"."live_timing__index"

    
),

formatted as (
    select
        keyframepath as key_frame_path,
        streampath as stream_path,
        
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_index
)

select *
from formatted