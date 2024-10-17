
  
  create view "f1"."staging"."stg_live_timing__tyre_stint_series__dbt_tmp" as (
    with
raw_tyre_stint_series as (
        

        select *
        from "f1"."ingress"."live_timing__tyre_stint_series"

    
),

formatted as (
    select
        driver as car_number,
        stint as stint_id,
        compound as tyre_compound,
        new as is_new,
        tyresnotchanged as tyres_not_changed,
        totallaps as total_laps,
        startlaps as start_laps,
        _streamtimestamp::interval as _stream_ts,
        
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

    from raw_tyre_stint_series
)

select *
from formatted
  );
