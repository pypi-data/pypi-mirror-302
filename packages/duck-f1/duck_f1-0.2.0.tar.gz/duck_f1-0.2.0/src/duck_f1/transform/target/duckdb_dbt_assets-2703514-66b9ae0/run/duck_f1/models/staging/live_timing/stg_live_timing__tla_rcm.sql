
  
  create view "f1"."staging"."stg_live_timing__tla_rcm__dbt_tmp" as (
    with
raw_tla_rcm as (
        

        select * from "f1"."ingress"."live_timing__tla_rcm"

    
),

formatted as (
    select
        timestamp as event_local_ts,
        message as race_control_message,
        _streamtimestamp::interval as _stream_ts,
        
    md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as event_id,
    event_round_number,
    event_sha,
    event_country,
    event_date,
    event_name,
    md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(session_type as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as session_id,
    session_sha,
    session_type,
    session_date

    from raw_tla_rcm
)

select *
from formatted
  );
