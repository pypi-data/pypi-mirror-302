
  
  create view "f1"."staging"."stg_ergast__status__dbt_tmp" as (
    with
raw_status as (select * from "f1"."ingress"."ergast__status"),

formatted as (
    select
        md5(cast(coalesce(cast(status as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as status_id,
        statusid as _ergast_status_id,
        status
    from raw_status
)

select *
from formatted
  );
