with
raw_current_tyres as (
        

        select * from "f1"."ingress"."live_timing__current_tyres"

    
),

formatted as (
    select
        driver as car_number,
        compound as tyre_compound,
        new as is_new,
        _streamtimestamp::interval as session_ts,
        
    md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as event_id,
    event_round_number,
    event_sha,
    event_country,
    event_date as event_start_local,
    event_name,
    md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(session_type as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as session_id,
    session_sha,
    session_type,
    session_date as session_start_local

    from raw_current_tyres
)

select *
from formatted