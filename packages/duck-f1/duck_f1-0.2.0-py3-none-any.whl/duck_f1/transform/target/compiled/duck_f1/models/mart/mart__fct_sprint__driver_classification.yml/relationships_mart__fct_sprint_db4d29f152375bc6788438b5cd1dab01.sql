
    
    

with child as (
    select session_id as from_field
    from "f1"."mart"."fct_sprint__driver_classification"
    where session_id is not null
),

parent as (
    select session_id as to_field
    from "f1"."mart"."dim_races"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


