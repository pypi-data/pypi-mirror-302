
  
  create view "f1"."intermediate"."int_live_timing__tyre__stints__dbt_tmp" as (
    with driver_stints as (
    select
        tyre_stint.session_id,
        tyre_stint.car_number,
        tyre_stint.stint_sequence,
        min(tyre_stint.session_ts) as stint_start_ts,
        min(lap_series.lap_number) as stint_start_lap_number,
        max(tyre_stint.session_ts) as stint_end_ts,
        max(lap_series.lap_number) as stint_end_lap_number,
        any_value(tyre_stint.tyre_compound) filter (tyre_stint.tyre_compound is not null and tyre_stint.tyre_compound not like 'UNKNOWN') as tyre_compound,
        min(tyre_stint.start_laps) as tyre_age_start,
        max(tyre_stint.total_laps) as tyre_age_end,
    from "f1"."staging"."stg_live_timing__tyre_stint_series" tyre_stint
    left join "f1"."staging"."stg_live_timing__lap_series" as lap_series
        on
            tyre_stint.session_id = lap_series.session_id
            and tyre_stint.car_number = lap_series.car_number
            and (
                tyre_stint.session_ts > lap_series.lap_start_ts
                and tyre_stint.session_ts <= lap_series.lap_end_ts
            )
    where lap_series.lap_number > 0
    group by tyre_stint.session_id, tyre_stint.car_number,tyre_stint.stint_sequence,
),

computed as (
    select
        *,
        if(tyre_age_start = 0, true, false) as is_new,
        tyre_age_end - tyre_age_start as lap_count
    from driver_stints
)

select *
from computed

-- stint lap count
-- stint lap start
-- sting lap end
  );
