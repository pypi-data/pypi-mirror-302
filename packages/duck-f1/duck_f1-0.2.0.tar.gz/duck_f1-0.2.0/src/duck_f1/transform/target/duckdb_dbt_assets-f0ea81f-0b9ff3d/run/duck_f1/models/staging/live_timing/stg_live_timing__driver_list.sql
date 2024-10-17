
  
  create view "f1"."staging"."stg_live_timing__driver_list__dbt_tmp" as (
    with
raw_driver_list as (
        

        select 
            *,
            
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

        from "f1"."ingress"."live_timing__driver_list"

    
),

formatted as (
    select
        session_id,
        driver_id,
        racingnumber as racing_number,
        broadcastname as broadcast_name,
        fullname as full_name,
        tla as driver_code,
        line as starting_position,
        teamname as team_name,
        teamcolour as team_color,
        firstname as first_name,
        lastname as last_name,
        reference as _live_timing_driver_id,
        headshoturl as headshort_url,
        _streamtimestamp as _stream_ts
    from raw_driver_list as driver_list
    left join "f1"."staging"."stg_ergast__drivers" as driver
        on driver_list.tla = driver.driver_code
)

select *
from formatted
  );
