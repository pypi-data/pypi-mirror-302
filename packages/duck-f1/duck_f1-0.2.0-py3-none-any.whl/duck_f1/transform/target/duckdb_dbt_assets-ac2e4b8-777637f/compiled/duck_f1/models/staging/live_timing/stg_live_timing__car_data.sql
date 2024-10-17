with
raw_car_data as (
        

        select * from "f1"."ingress"."live_timing__car_data"

    
),

formatted as (
    select
        capturetimestamp::timestamp as capture_ts,
        carnumber as car_number,
        enginerpm as engine_rpm,
        carspeed as car_speed,
        enginegear as engine_gear,
        throttleposition as throttle_position,
        brakeposition as brake_position,
        drsstatus as drs_status,
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

    from raw_car_data
)

select *
from formatted