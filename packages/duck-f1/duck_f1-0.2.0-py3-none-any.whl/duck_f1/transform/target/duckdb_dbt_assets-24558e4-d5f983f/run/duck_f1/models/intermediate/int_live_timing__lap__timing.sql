
  
  create view "f1"."intermediate"."int_live_timing__lap__timing__dbt_tmp" as (
    with
formatted as (
    select
        lap_series.session_id,
        lap_series.car_number,
        lap_series.lap_number,
        lap_series.lap_time as estimated_lap_time,
        lap_time.lap_time,
        lap_time.lap_time_status,
        lap_time.is_personal_fastest,
        lap_time.session_ts
    from "f1"."staging"."stg_live_timing__lap_series" as lap_series
    left join "f1"."staging"."stg_live_timing__timing_data_last_lap" as lap_time
        on
            lap_series.session_id = lap_time.session_id
            and lap_series.car_number = lap_time.car_number
            and (
                lap_time.session_ts > (lap_series.lap_end_ts - to_milliseconds(125))
                and lap_time.session_ts < (lap_series.lap_end_ts + to_milliseconds(125))
            )
    where lap_series.lap_number > 0
)

select *
from formatted
  );
