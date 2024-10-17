
  
  create view "f1"."staging"."stg_live_timing__timing_data_last_lap__dbt_tmp" as (
    with
raw_timing_data_last_lap as (
        

        select *
        from "f1"."ingress"."live_timing__timing_data_last_lap"

    
),

computed as (
    select
        driver as car_number,
        
    to_milliseconds(
        (split_part(value, ':', 1)::integer * 60 * 1000)
        + (floor(split_part(value, ':', 2)::double)::integer * 1000)
        + (split_part(value, '.', 2)::integer)
    )
 as lap_time,
        status as lap_time_status,
        overallfastest as is_overall_fastest,
        personalfastest as is_personal_fastest,
        _streamtimestamp::interval as session_ts,
        
    md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as event_id,
    event_round_number,
    event_sha,
    event_country,
    event_date as event_start_local,
    event_name,
    md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(session_type as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as session_id,
    session_sha,
    session_type,
    session_date as session_start_local

    from raw_timing_data_last_lap
    where
        value is not null
        and len(value) > 0
),

formatted as (
    select
        session_id,
        car_number,
        lap_time,
        lap_time_status,
        is_personal_fastest,
        session_ts
    from computed
)

select *
from formatted
  );
