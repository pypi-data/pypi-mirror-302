
  
  create view "f1"."intermediate"."int_lap__times__dbt_tmp" as (
    with
raw_timing_data_sectors as (
    select *
    from "f1"."staging"."stg_live_timing__timing_data_last_lap"
),

formatted as (
    select
        lap_time.session_id,
        lap_time.car_number,
        lap_series.lap_number,
        lap_time.lap_time,
        lap_time.lap_time_status,
        lap_time.is_personal_fastest,
        lap_time._stream_ts
    from raw_timing_data_sectors as lap_time
    left join "f1"."staging"."stg_live_timing__lap_series" as lap_series
        on lap_time.session_id = lap_series.session_id
        and lap_time.car_number = lap_series.car_number
        and (
            lap_time._stream_ts > lap_series.lap_start_ts
            and lap_time._stream_ts <= lap_series.lap_end_ts
        )
)

select *
from formatted
  );
