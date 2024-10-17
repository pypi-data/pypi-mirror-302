
    
    

with child as (
    select session_id as from_field
    from "f1"."mart"."mart_fct_session__drivers"
    where session_id is not null
),

parent as (
    select session_id as to_field
    from "f1"."mart"."mart_dim_sessions"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


