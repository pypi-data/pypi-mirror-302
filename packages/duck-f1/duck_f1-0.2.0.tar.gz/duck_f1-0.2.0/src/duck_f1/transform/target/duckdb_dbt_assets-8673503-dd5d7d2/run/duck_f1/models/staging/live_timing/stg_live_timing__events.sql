
  
  create view "f1"."staging"."stg_live_timing__events__dbt_tmp" as (
    with
raw_sessions as (
    select * from "f1"."ingress"."live_timing__sessions"
),

formatted as (
    select
        md5(cast(coalesce(cast(date_part('year', event_date) as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_round_number as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as event_id,
        event_sha as _live_timing_event_sha,
        date_part('year', event_date) as season,
        event_round_number as round,
        event_name as name,
        event_official_event_name as official_name,
        event_country as country,
        event_location as location,
    from raw_sessions
    qualify 
        row_number() over (partition by event_id order by event_id) = 1
)

select *
from formatted
  );
