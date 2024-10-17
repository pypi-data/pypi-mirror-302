
  
  create view "f1"."staging"."stg_live_timing__weather_data__dbt_tmp" as (
    with
raw_weather_data as (
        

        select * from "f1"."ingress"."live_timing__weather_data"

    

),

computed as (
    select
        airtemp as air_temperature,
        humidity as relative_humidity,
        pressure as air_pressure,
        rainfall as rain_accumulation,
        tracktemp as track_temperature,
        winddirection as wind_direction,
        windspeed as wind_speed,
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

    from raw_weather_data
),

formatted as (
    select
        session_id,
        session_ts,
        air_temperature,
        air_pressure,
        relative_humidity,
        rain_accumulation,
        track_temperature,
        wind_direction,
        wind_speed
    from computed
)

select *
from formatted
  );
