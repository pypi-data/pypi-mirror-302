with
raw_weather_data as (
        

        select * from "f1"."ingress"."live_timing__weather_data"

    

),

formatted as (
    select
        airtemp as air_temperature,
        humidity as relative_humidity,
        pressure as air_pressure,
        rainfall as rain_accumulation,
        tracktemp as track_temperature,
        winddirection as wind_direction,
        windspeed as wind_speed,
        _streamtimestamp as _stream_ts,
        
    split_part(_stream_ts, ':', 1)::integer * 60 * 60 * 1000
    + split_part(_stream_ts, ':', 2)::integer * 60 * 1000
    + floor(split_part(_stream_ts, ':', 3)::double) * 1000
    + split_part(_stream_ts, '.', 2)::integer as stream_ms,
    to_milliseconds(
        (ceiling(stream_ms / 1000 * 10) / 10 * 1000)::integer
    ) as stream_bucket
,
        
    season_round as season_round,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_weather_data
)

select *
from formatted