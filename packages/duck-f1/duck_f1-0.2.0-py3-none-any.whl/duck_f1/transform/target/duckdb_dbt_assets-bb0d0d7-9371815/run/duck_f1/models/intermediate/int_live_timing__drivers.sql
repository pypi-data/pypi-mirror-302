
  
  create view "f1"."intermediate"."int_live_timing__drivers__dbt_tmp" as (
    with
driver_list as (
    select * from "f1"."staging"."stg_live_timing__driver_list"
),

formatted as (
    select *
    from driver_list
)

select *
from formatted
  );
