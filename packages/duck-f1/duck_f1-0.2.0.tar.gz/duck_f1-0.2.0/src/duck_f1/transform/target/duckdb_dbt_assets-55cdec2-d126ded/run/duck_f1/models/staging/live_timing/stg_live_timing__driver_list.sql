
  
  create view "f1"."staging"."stg_live_timing__driver_list__dbt_tmp" as (
    with
raw_driver_list as (
        

        select * from "f1"."ingress"."live_timing__driver_list"

    
),

formatted as (
    select
        racingnumber as racing_number,
        broadcastname as broadcast_name,
        fullname as full_name,
        tla as driver_abbr,
        line as starting_position,
        teamname as team_name,
        teamcolour as team_color,
        firstname as first_name,
        lastname as last_name,
        reference as driver_id,
        headshoturl as headshort_url,
        _streamtimestamp as _stream_ts,
        
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date

    from raw_driver_list
)

select *
from formatted
  );
