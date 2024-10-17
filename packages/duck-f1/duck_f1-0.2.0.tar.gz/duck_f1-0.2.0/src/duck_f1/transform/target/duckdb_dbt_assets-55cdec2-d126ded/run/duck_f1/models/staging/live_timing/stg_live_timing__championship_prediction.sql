
  
  create view "f1"."staging"."stg_live_timing__championship_prediction__dbt_tmp" as (
    with
raw_championship_prediction as (
        

        select *
        from
            "f1"."ingress"."live_timing__championship_prediction"

    
),

formatted as (
    select
        entity,
        identifier,
        metric as metric_name,
        value as metric_value,
        _streamtimestamp as _stream_ts,
        
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_championship_prediction
)

select *
from formatted
  );
