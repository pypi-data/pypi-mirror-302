
  
  create view "f1"."staging"."stg_live_timing__tyre_stint_series__dbt_tmp" as (
    with
raw_tyre_stint_series as (
        

        select *
        from "f1"."ingress"."live_timing__tyre_stint_series"

    
),

formatted as (
    select
        driver as driver_number,
        stint as stint_id,
        compound as tyre_compound,
        new as is_new,
        tyresnotchanged as tyres_not_changed,
        totallaps as total_laps,
        startlaps as start_laps,
        _streamtimestamp as _stream_ts,
        
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_tyre_stint_series
)

select *
from formatted
  );
