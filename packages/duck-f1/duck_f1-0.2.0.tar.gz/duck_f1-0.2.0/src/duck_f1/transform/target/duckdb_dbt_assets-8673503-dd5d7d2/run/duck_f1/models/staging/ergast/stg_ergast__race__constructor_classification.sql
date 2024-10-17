
  
  create view "f1"."staging"."stg_ergast__race__constructor_classification__dbt_tmp" as (
    with
raw_constructor_results as (
    select * from "f1"."ingress"."ergast__constructor_results"
),

constructor_ids as (
    select
        constructor_id,
        ergast_constructor_id
    from "f1"."staging"."stg_ergast__constructors"
),

event_ids as (
    select
        session_id,
        ergast_race_id
    from "f1"."staging"."stg_ergast__races"
),

formatted as (
    select
        constructor.constructor_id,
        _session.session_id,
        constructor_result.points,
        if(constructor_result.status = '\N', null, constructor_result.status) as status
    from raw_constructor_results as constructor_result
    inner join
        constructor_ids as constructor
        on constructor_result.constructorid = constructor.ergast_constructor_id
    inner join event_ids as _session on constructor_result.raceid = _session.ergast_race_id
)

select *
from formatted
  );
