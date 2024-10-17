with
raw_track_status as (
        

        select * from "f1"."ingress"."live_timing__track_status"

    
),

renamed as (
    select
        status as _track_status_id,
        message as status_message,
        _streamtimestamp::interval as session_ts,
        
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

    from raw_track_status
),

computed as (
    select
        *,
        session_ts as status_start_ts,
        lead(session_ts) over (partition by session_id order by session_ts) as status_end_ts,
        status_end_ts - status_start_ts as status_duration
        -- TODO: Add session end
    from renamed
),

formatted as (
    select
        session_id,
        _track_status_id,
        status_message,
        session_ts,
        status_start_ts,
        status_end_ts,
        status_duration
    from computed
)

select *
from formatted