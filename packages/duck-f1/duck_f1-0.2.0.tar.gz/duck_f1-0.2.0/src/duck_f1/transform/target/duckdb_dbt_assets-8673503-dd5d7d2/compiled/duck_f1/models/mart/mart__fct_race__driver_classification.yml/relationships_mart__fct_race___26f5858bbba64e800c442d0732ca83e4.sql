
    
    

with child as (
    select constructor_id as from_field
    from "f1"."mart"."fct_race__driver_classification"
    where constructor_id is not null
),

parent as (
    select constructor_id as to_field
    from "f1"."mart"."dim_constructors"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


