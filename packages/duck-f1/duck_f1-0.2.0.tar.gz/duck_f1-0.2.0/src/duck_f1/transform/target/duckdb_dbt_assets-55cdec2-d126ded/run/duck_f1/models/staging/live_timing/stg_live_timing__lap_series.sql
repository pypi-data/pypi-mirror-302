
  
  create view "f1"."staging"."stg_live_timing__lap_series__dbt_tmp" as (
    with
raw_lap_series as (
        

        select * from "f1"."ingress"."live_timing__lap_series"

    
),

formatted as (
    select
        drivernumber as driver_number,
        lapnumber as lap_number,
        lapposition as lap_position,
        _streamtimestamp as _stream_ts,
        
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_lap_series
)

select *
from formatted
  );
