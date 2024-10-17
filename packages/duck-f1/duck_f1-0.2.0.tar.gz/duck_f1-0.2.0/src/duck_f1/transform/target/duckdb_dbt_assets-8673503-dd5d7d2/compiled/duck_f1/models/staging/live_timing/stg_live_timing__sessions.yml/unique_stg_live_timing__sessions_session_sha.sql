
    
    

select
    session_sha as unique_field,
    count(*) as n_records

from "f1"."staging"."stg_live_timing__sessions"
where session_sha is not null
group by session_sha
having count(*) > 1


