select
    tyre_stint.session_id,
    _session.driver_id,
    md5(cast(coalesce(cast(tyre_stint.session_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(_session.driver_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(tyre_stint.stint_sequence as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as stint_id,
    tyre_stint.stint_sequence,
    tyre_stint.stint_start_ts,
    tyre_stint.stint_start_lap_number,
    tyre_stint.tyre_age_start,
    tyre_stint.tyre_compound,
    tyre_stint.is_new,
    tyre_stint.stint_end_ts,
    tyre_stint.stint_end_lap_number,
    tyre_stint.tyre_age_end,
    tyre_stint.lap_count
from "f1"."intermediate"."int_live_timing__tyre_stints" as tyre_stint
left join "f1"."mart"."mart_fct_session__drivers" as _session
    on
        tyre_stint.session_id = _session.session_id
        and tyre_stint.car_number = _session.car_number