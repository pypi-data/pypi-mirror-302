with
raw_events as (select * from "f1"."ingress"."ergast__races"),

circuit_ids as (
    select
        circuit_id,
        _ergast_circuit_id
    from "f1"."staging"."stg_ergast__circuits"
),

formatted as (
    select
        md5(cast(coalesce(cast(_event.year as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(_event.round as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as event_id,
        circuit.circuit_id,
        _event.raceid as _ergast_race_id,
        _event.year as season,
        _event.round,
        _event.name as event_name,
        _event.url as wikipedia_url
    from raw_events as _event
    inner join circuit_ids as circuit on _event.circuitid = circuit._ergast_circuit_id
)

select *
from formatted