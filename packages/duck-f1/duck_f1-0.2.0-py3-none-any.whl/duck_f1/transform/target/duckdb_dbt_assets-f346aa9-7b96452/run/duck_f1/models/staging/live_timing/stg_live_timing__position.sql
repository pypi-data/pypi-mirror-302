
  
  create view "f1"."staging"."stg_live_timing__position__dbt_tmp" as (
    with
raw_position as (
        

        select * from "f1"."ingress"."live_timing__position"

    
),

car_positions as (
    select
        timestamp::timestamp as event_utc_ts,
        driver::integer as car_number,
        status as car_status,
        x::integer as x_position,
        y::integer as y_position,
        z::integer as z_position,
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

    from raw_position
),

stream_segments as (
    select
        session_id,
        car_number,
        session_ts,
        count(*) as _count
    from car_positions
    group by session_id, car_number, session_ts
),

stream_corrections as (
    select
        *,
        lead(session_ts) over (
            partition by session_id, car_number
            order by session_ts
        ) as _next_value,
        if(
            _next_value is null,
            to_milliseconds(200),
            (_next_value - session_ts) / _count
        ) as _correction_step
    from stream_segments
),

computed as (
    select
        car_position.session_id,
        car_position.car_number,
        car_position.car_status,
        car_position.x_position,
        car_position.y_position,
        car_position.z_position,
        car_position.event_utc_ts,
        car_position.session_ts,
        -1 + row_number() over (
            partition by car_position.session_id, car_position.car_number, car_position.session_ts
            order by car_position.event_utc_ts
        ) as _correction_factor,
        car_position.session_ts
        + date_trunc('millisecond', _correction_factor * stream_correction._correction_step)
            as _correctedsession_ts
    from car_positions as car_position
    left join stream_corrections as stream_correction
        on
            car_position.session_id = stream_correction.session_id
            and car_position.car_number = stream_correction.car_number
            and car_position.session_ts = stream_correction.session_ts
),

formatted as (
    select
        session_id,
        car_number,
        car_status,
        x_position,
        y_position,
        z_position,
        event_utc_ts,
        session_ts,
        _correctedsession_ts
    from computed
)

select *
from formatted
  );
