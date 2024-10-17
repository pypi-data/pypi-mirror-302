with
raw_timing_data_speeds as (
        

        select *
        from "f1"."ingress"."live_timing__timing_data_speeds"

    
),

computed as (
    select
        driver as car_number,
        speedkey as speed_key,
        if(len(value) > 0, value::integer, null) as speed_value,
        status as speed_status,
        coalesce(overallfastest::boolean, false) as is_overall_fastest,
        coalesce(personalfastest::boolean, false) as is_personal_fastest,
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

    from raw_timing_data_speeds
    where speed_value is not null
),

formatted as (
    select
        session_id,
        car_number,
        speed_key,
        speed_value,
        is_overall_fastest
            as is_personal_fastest,
        speed_status,
        session_ts
    from computed
)

select *
from formatted