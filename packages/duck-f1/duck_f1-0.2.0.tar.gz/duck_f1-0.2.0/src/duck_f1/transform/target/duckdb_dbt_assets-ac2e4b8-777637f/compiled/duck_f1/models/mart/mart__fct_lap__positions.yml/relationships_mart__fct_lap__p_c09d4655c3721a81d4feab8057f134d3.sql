
    
    

with child as (
    select driver_id as from_field
    from "f1"."mart"."fct_lap__positions"
    where driver_id is not null
),

parent as (
    select driver_id as to_field
    from "f1"."mart"."dim_drivers"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


