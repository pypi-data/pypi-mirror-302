with
raw_circuits as (select * from "f1"."ingress"."ergast__circuits"),

formatted as (
    select
        md5(cast(coalesce(cast(circuitref as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as circuit_id,
        circuitid as _ergast_circuit_id,
        circuitref as circuit_ref,
        name as circuit_name,
        location as circuit_location,
        country as circuit_country,
        lat as latitude,
        lng as longitude,
        alt as altitude,
        url as wikipedia_url
    from raw_circuits
)

select *
from formatted