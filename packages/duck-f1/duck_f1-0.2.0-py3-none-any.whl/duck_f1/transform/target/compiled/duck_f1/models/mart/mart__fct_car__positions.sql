with
formatted as (
    select
        car_position.session_id,
        _session.driver_id,
        md5(cast(coalesce(cast(car_position.session_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(_session.driver_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(car_position.lap_number as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as lap_id,
        car_position.lap_number,
        car_position.session_ts,
        car_position.car_status,
        car_position.x_position,
        car_position.y_position,
        car_position.z_position
    from "f1"."intermediate"."int_live_timing__car__positions" as car_position
    left join "f1"."mart"."mart__fct_session__drivers" as _session
        on
            car_position.session_id = _session.session_id
            and car_position.car_number = _session.car_number
)

select *
from formatted