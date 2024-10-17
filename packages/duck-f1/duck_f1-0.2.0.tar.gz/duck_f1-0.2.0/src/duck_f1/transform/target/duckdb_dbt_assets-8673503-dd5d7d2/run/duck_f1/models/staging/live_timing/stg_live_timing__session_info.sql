
  
  create view "f1"."staging"."stg_live_timing__session_info__dbt_tmp" as (
    with
raw_session_info as (
        

        select * from "f1"."ingress"."live_timing__session_info"

    
),

formatted as (
    select
        meetingkey as meeting_key,
        meetingname as meeting_name,
        meetinglocation as meeting_locatio,
        meetingcountrykey as country_key,
        meetingcountrycode as country_code,
        meetingcountryname as country_name,
        meetingcircuitkey as circuit_key,
        meetingcircuitshortname as circuit_short_name,
        archivestatusstatus as archive_status,
        key as session_key,
        type as session_type,
        name as session_name,
        startdate as session_start_date,
        enddate as session_end_data,
        gmtoffset as gmt_offset,
        path as session_path,
        
    season_round as season_round,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_session_info
)

select *
from formatted
  );
