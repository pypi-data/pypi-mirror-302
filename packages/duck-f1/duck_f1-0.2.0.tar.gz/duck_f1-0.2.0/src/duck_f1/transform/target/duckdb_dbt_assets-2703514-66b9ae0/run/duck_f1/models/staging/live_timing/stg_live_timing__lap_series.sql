
  
  create view "f1"."staging"."stg_live_timing__lap_series__dbt_tmp" as (
    with
raw_lap_series as (
        

        select * from "f1"."ingress"."live_timing__lap_series"

    
),

renamed as (
    select
        drivernumber as car_number,
        lapnumber as lap_number,
        lapposition as lap_position,
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

    from raw_lap_series
),

formatted as (
    select
        session_id,
        session_type,
        car_number,
        lap_number,
        lap_position,
        _stream_ts as lap_end_ts,
        lag(_stream_ts)
            over (partition by session_id, car_number order by _stream_ts)
            as lap_start_ts,
        lap_end_ts - lap_start_ts as lap_time
    from renamed
)

select *
from formatted
  );
