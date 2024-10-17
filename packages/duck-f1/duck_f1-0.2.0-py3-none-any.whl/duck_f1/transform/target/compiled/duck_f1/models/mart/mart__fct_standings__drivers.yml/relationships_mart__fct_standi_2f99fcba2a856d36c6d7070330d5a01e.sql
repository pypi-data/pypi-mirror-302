
    
    

with child as (
    select event_id as from_field
    from "f1"."mart"."fct_standings__drivers"
    where event_id is not null
),

parent as (
    select event_id as to_field
    from "f1"."mart"."dim_races"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


