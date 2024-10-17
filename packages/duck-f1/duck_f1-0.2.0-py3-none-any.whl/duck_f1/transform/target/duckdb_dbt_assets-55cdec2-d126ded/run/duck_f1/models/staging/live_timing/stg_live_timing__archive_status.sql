
  
  create view "f1"."staging"."stg_live_timing__archive_status__dbt_tmp" as (
    with
raw_archive_status as (
        

        select *
        from "f1"."ingress"."live_timing__archive_status"

    
),

formatted as (
    select
        status, 
    event_round_number as event_round_number,
    event_sha as event_sha,
    event_country as event_country,
    event_date as event_date,
    event_name as event_name,
    session_sha as session_sha,
    session_type as session_type,
    session_date as session_date
 from raw_archive_status
)

select *
from formatted
  );
