
  
  create view "f1"."staging"."stg_ergast__race__driver_fastest_lap__dbt_tmp" as (
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

results as (
    select
        _session.session_id,
        driver.driver_id,
        constructor.constructor_id,
        if(result.fastestlap = '\N', null, result.fastestlap::integer) as fastest_lap,
        if(result.rank = '\N', null, result.rank::integer) as fastest_lap_rank,
        if(
            result.fastestlaptime = '\N',
            null,
            
    to_milliseconds(
        (split_part(result.fastestlaptime, ':', 1)::integer * 60 * 1000)
        + (floor(split_part(result.fastestlaptime, ':', 2)::double)::integer * 1000)
        + (split_part(result.fastestlaptime, '.', 2)::integer)
    )

        ) as fastest_lap_time,
        if(result.fastestlapspeed = '\N', null, result.fastestlapspeed::numeric)
            as fastest_lap_speed
    from raw_results as result
    inner join
        constructor_ids as constructor
        on result.constructorid = constructor.ergast_constructor_id
    inner join driver_ids as driver on result.driverid = driver.ergast_driver_id
    inner join event_ids as _session on result.raceid = _session.ergast_race_id
    where fastest_lap_rank > 0
),

results_stats as (
    select
        *,
        fastest_lap_time
        - first(fastest_lap_time)
            over (partition by session_id order by fastest_lap_rank)
            as fastest_lap_time_interval,
        fastest_lap_time
        - lag(fastest_lap_time)
            over (partition by session_id order by fastest_lap_rank)
            as fastest_lap_time_gap
    from results
),

formatted as (
    select
        result.session_id,
        result.driver_id,
        result.constructor_id,
        result.fastest_lap,
        result.fastest_lap_rank,
        result.fastest_lap_time,
        result.fastest_lap_time_gap,
        result.fastest_lap_speed,
        if(
            result.fastest_lap_time_interval = to_milliseconds(0),
            null,
            result.fastest_lap_time_interval
        ) as fastest_lap_time_interval
    from results_stats as result
)

select *
from formatted
  );
