
  
  create view "f1"."intermediate"."int_qualifying__dbt_tmp" as (
    with
qualifying_results as (select * from "f1"."staging"."stg_ergast__qualifying"),

qualifying_windows as (
    select *,
        row_number() over (partition by race_id order by q1_time nulls last) as q1_position
    from qualifying_results
    where q1_time is not null
),

formatted as (
    select qualifying_result.*
    from qualifying_windows qualifying_result
)

select *
from formatted
  );
