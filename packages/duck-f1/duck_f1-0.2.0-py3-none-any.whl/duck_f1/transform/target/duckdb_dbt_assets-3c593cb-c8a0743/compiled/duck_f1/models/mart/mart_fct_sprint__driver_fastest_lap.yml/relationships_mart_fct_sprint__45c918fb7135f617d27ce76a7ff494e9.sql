
    
    

with child as (
    select driver_id as from_field
    from "f1"."mart"."mart_fct_sprint__driver_fastest_lap"
    where driver_id is not null
),

parent as (
    select driver_id as to_field
    from "f1"."mart"."mart_dim_drivers"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


