
  
  create view "f1"."staging"."stg_live_timing__timing_data_best_lap__dbt_tmp" as (
    with
raw_timing_data_best_lap as (
        

        select *
        from "f1"."ingress"."live_timing__timing_data_best_lap"

    
),

formatted as (
    select
        value as lap_time,
        lap as lap_key,
        driver,
        _streamtimestamp as _stream_ts,
        
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_timing_data_best_lap
)

select *
from formatted
  );
