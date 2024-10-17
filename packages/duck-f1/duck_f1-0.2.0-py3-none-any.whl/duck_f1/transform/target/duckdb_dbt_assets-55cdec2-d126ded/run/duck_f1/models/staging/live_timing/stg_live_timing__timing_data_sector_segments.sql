
  
  create view "f1"."staging"."stg_live_timing__timing_data_sector_segments__dbt_tmp" as (
    with
raw_timing_data_sector_segments as (
        

        select *
        from
                "f1"."ingress"."live_timing__timing_data_sector_segments"

    
),

formatted as (
    select
        sectorkey as sector_key,
        segmentkey as segment_key,
        status as sector_status,
        driver,
        _streamtimestamp as _stream_ts,
        
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_timing_data_sector_segments
)

select *
from formatted
  );
