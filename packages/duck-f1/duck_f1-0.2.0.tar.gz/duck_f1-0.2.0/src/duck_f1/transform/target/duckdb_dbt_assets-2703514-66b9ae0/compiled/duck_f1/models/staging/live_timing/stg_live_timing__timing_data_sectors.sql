with
raw_timing_data_sectors as (
        

        select *
        from "f1"."ingress"."live_timing__timing_data_sectors"

    
),

computed as (
    select
        driver as car_number,
        sectorkey::integer as sector_key,
        stopped::boolean as is_stopped,
        to_milliseconds(if(len(value) > 0, value::numeric * 1000, null)) as sector_time,
        to_milliseconds(if(len(previousvalue) > 0, value::numeric * 1000, null)) as previous_value,
        status as sector_status,
        overallfastest::boolean as is_overall_fastest,
        personalfastest::boolean as is_personal_fastest,
        _streamtimestamp::interval as _stream_ts,
        
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

    from raw_timing_data_sectors
    where sector_time is not null
),

formatted as (
    select
        session_id,
        car_number,
        sector_key,
        sector_time,
        previous_value,
        is_overall_fastest,
        is_personal_fastest,
        sector_status,
        is_stopped,
        _stream_ts
    from computed
)

select *
from formatted