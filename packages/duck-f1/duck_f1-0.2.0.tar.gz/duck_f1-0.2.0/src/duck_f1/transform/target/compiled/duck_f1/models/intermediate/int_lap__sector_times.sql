with
raw_timing_data_sectors as (
    select *
    from "f1"."staging"."stg_live_timing__timing_data_sectors"
),

pivoted as (
    select
        sector.session_id,
        sector.car_number,
        lap_series.lap_number,
        any_value(if(sector.sector_key = 0, sector.sector_time, null) order by sector._stream_ts) as sector_1_time,
        any_value(if(sector.sector_key = 1, sector.sector_time, null) order by sector._stream_ts) as sector_2_time,
        any_value(if(sector.sector_key = 2, sector.sector_time, null) order by sector._stream_ts) as sector_3_time
    from raw_timing_data_sectors as sector
    left join "f1"."staging"."stg_live_timing__lap_series" as lap_series
        on sector.session_id = lap_series.session_id
        and sector.car_number = lap_series.car_number
        and (
            sector._stream_ts > lap_series.lap_start_ts
            and sector._stream_ts <= lap_series.lap_end_ts
        )
    group by sector.session_id, sector.car_number, lap_series.lap_number
)

select *
from pivoted