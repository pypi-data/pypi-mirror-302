
  
  create view "f1"."staging"."stg_live_timing__heartbeat__dbt_tmp" as (
    with
raw_heartbeat as (
        

        select * from "f1"."ingress"."live_timing__heartbeat"

    
),

formatted as (
    select
        utc::timestamp as utc_ts,
        _streamtimestamp::interval as _stream_ts,
        utc_ts - _stream_ts as start_utc,
        
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_heartbeat
)

select *
from formatted
  );
