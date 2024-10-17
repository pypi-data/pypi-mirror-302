
  
  create view "f1"."staging"."stg_live_timing__driver_race_info__dbt_tmp" as (
    with
raw_driver_race_info as (
    

        select *
        from "f1"."ingress"."live_timing__driver_race_info"

    
),

formatted as (
    select
        race_info.driver as car_number,
        race_info.position as track_position,
        race_info.gap as gap_to_leader,
        race_info.interval,
        race_info.pitstops as pitstop_count,
        race_info.catching as is_catching,
        race_info.overtakestate as overtake_count,
        race_info.isout as is_out,
        race_info._streamtimestamp as _stream_ts,
        
    md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as event_id,
    event_round_number,
    event_sha,
    event_country,
    event_date,
    event_name,
    md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(session_type as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as session_id,
    session_sha,
    session_type,
    session_date

    from raw_driver_race_info as race_info
)

select *
from formatted
  );
