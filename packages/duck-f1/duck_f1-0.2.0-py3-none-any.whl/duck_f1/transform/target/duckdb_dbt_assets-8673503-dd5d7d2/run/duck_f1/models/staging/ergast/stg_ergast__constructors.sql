
  
  create view "f1"."staging"."stg_ergast__constructors__dbt_tmp" as (
    with
raw_constructors as (
    select * from "f1"."ingress"."ergast__constructors"
),

formatted as (
    select
        md5(cast(coalesce(cast(name as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(nationality as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT))
            as constructor_id,
        constructorid as ergast_constructor_id,
        constructorref as constructor_reference,
        name as constructor_name,
        nationality,
        url as wikipedia_url
    from raw_constructors
)

select *
from formatted
  );
