
  
  create view "f1"."staging"."stg_live_timing__timing_data_speeds__dbt_tmp" as (
    with
raw_timing_data_speeds as (
        

        select *
        from "f1"."ingress"."live_timing__timing_data_speeds"

    
),

formatted as (
    select
        speedkey as speed_key,
        value as speed_value,
        status as speed_status,
        overallfastest as is_overall_fastest,
        personalfastest as is_personal_fastest,
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

    from raw_timing_data_speeds
)

select *
from formatted
  );
