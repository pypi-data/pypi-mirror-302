
    
    

with child as (
    select status_id as from_field
    from "f1"."mart"."fct_sprint__driver_classification"
    where status_id is not null
),

parent as (
    select status_id as to_field
    from "f1"."mart"."dim_status"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


