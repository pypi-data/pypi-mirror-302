
  
  create view "f1"."staging"."stg_live_timing__race_control_messages__dbt_tmp" as (
    with
raw_race_control_messages as (
        

        select *
        from "f1"."ingress"."live_timing__race_control_messages"

    
),

formatted as (
    select
        messageid as message_id,
        utc as utc_ts,
        lap as lap_number,
        category as message_category,
        messagedata as message_data,
        _streamtimestamp as _stream_ts,
        
    season_round as season_round,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_race_control_messages
)

select *
from formatted
  );
