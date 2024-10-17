
  
  create view "f1"."staging"."stg_live_timing__timing_data_status__dbt_tmp" as (
    with
raw_timing_data_status as (
        

        select *
        from "f1"."ingress"."live_timing__timing_data_status"

    
),

formatted as (
    select
        driver,
        metricname as metric_name,
        metricvalue as metric_value,
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

    from raw_timing_data_status
)

select *
from formatted
  );
