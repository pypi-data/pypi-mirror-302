
  
  create view "f1"."staging"."stg_live_timing__extrapolated_clock__dbt_tmp" as (
    with
raw_extrapolated_clock as (
        

        select *
        from "f1"."ingress"."live_timing__extrapolated_clock"

    
),

formatted as (
    select
        utc as utc_ts,
        remaining as remaining_session_time,
        extrapolating as is_extrapolated,
        _streamtimestamp as _stream_ts,
        
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_extrapolated_clock
)

select *
from formatted
  );
