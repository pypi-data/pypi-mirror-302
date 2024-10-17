
  
  create view "f1"."staging"."stg_ergast__race__driver_classification__dbt_tmp" as (
    with
raw_results as (select * from "f1"."ingress"."ergast__results"),

constructor_ids as (
    select
        constructor_id,
        ergast_constructor_id
    from "f1"."staging"."stg_ergast__constructors"
),

driver_ids as (
    select
        driver_id,
        ergast_driver_id
    from "f1"."staging"."stg_ergast__drivers"
),

event_ids as (
    select
        session_id,
        ergast_race_id
    from "f1"."staging"."stg_ergast__races"
),

status_ids as (
    select
        status_id,
        ergast_status_id
    from "f1"."staging"."stg_ergast__status"
),

results as (
    select
        _session.session_id,
        driver.driver_id,
        constructor.constructor_id,
        result.positiontext as position_label,
        result.positionorder::integer as position_order,
        driver_status.status_id,
        result.points,
        result.laps as laps_completed,
        result.number::integer as driver_number,
        if(result.grid > 0, result.grid, null) as grid_position,
        if(result.position = '\N', null, result.position::integer) as classification,
        if(result.milliseconds = '\N', null, to_milliseconds(result.milliseconds::integer))
            as race_time,
        if(result.time = '\N', null, result.time) as race_time_label
    from raw_results as result
    inner join
        constructor_ids as constructor
        on result.constructorid = constructor.ergast_constructor_id
    inner join driver_ids as driver on result.driverid = driver.ergast_driver_id
    inner join event_ids as _session on result.raceid = _session.ergast_race_id
    inner join status_ids as driver_status on result.statusid = driver_status.ergast_status_id
),

results_windows as (
    select
        *,
        race_time
        - first(race_time)
            over (partition by session_id order by position_order)
            as race_time_interval,
        race_time
        - lag(race_time) over (partition by session_id order by position_order) as race_time_gap
    from results
),

formatted as (
    select
        result.session_id,
        result.driver_id,
        result.constructor_id,
        result.driver_number,
        result.grid_position,
        result.classification,
        result.position_label,
        result.position_order,
        result.status_id,
        result.points,
        result.laps_completed,
        result.race_time,
        result.race_time_label,
        result.race_time_interval,
        result.race_time_gap
    from results_windows as result
)

select *
from formatted
  );
