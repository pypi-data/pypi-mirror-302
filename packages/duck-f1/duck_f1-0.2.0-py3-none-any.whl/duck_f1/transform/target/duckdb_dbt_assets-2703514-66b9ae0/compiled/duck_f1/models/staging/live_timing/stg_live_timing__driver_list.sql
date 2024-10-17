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

computed as (
    select
        session_id,
        reference as _live_timing_driver_id,
        racingnumber::integer as car_number,
        tla as driver_code,
        line as starting_position,
        teamname as team_name,
        teamcolour as team_color,
        headshoturl as head_shot_url,
        _streamtimestamp::interval as _stream_ts,
        trim(broadcastname) as broadcast_name,
        trim(fullname) as full_name,
        trim(broadcast_name[3:]) as _last_name,
        trim(string_split(full_name, _last_name)[1]) as first_name
    from raw_driver_list
),

formatted as (
    select
        session_id,
        _live_timing_driver_id,
        car_number,
        broadcast_name,
        first_name,
        driver_code,
        starting_position,
        team_name,
        team_color,
        head_shot_url,
        _stream_ts,
        _last_name[1] || lower(_last_name[2:]) as last_name,
        concat(first_name, ' ', last_name) as full_name,
        lower(strip_accents(concat(first_name, last_name))) as _full_name_key
    from computed
)

select *
from formatted