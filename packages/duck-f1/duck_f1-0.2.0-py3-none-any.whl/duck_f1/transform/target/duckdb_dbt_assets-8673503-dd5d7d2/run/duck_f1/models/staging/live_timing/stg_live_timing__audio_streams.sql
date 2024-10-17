
  
  create view "f1"."staging"."stg_live_timing__audio_streams__dbt_tmp" as (
    with
raw_audio_streams as (
        

        select * from "f1"."ingress"."live_timing__audio_streams"

    
),

formatted as (
    select
        name,
        language,
        uri,
        path,
        utc as event_utc_ts,
        _streamtimestamp as _stream_ts,
        
    season_round as season_round,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_audio_streams
)

select *
from formatted
  );
