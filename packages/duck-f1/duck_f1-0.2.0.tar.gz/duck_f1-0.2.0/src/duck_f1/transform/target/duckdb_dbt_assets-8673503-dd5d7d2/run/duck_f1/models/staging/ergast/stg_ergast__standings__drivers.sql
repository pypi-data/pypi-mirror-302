
  
  create view "f1"."staging"."stg_ergast__standings__drivers__dbt_tmp" as (
    with
raw_driver_standings as (
    select * from "f1"."ingress"."ergast__driver_standings"
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

formatted as (
    select
        driver.driver_id,
        _session.session_id,
        driver_standing.points,
        driver_standing.position,
        driver_standing.positiontext as position_label,
        driver_standing.wins as win_count
    from raw_driver_standings as driver_standing
    inner join driver_ids as driver on driver_standing.driverid = driver.ergast_driver_id
    inner join event_ids as _session on driver_standing.raceid = _session.ergast_race_id
)

select *
from formatted
  );
