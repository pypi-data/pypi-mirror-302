
    
    

with child as (
    select constructor_id as from_field
    from "f1"."mart"."mart_fct_race__constructor_classification"
    where constructor_id is not null
),

parent as (
    select constructor_id as to_field
    from "f1"."mart"."mart_dim_constructors"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


