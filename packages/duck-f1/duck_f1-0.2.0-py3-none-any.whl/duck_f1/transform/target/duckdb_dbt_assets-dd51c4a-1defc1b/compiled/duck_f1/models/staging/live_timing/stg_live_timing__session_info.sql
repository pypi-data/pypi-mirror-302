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

    from raw_session_info
)

select *
from formatted