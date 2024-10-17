select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

with child as (
    select constructor_id as from_field
    from "f1"."mart"."fct_qualifying__driver_classification"
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



      
    ) dbt_internal_test