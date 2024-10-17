
  
  create view "f1"."mart"."mart__fct_standings__drivers__dbt_tmp" as (
    select *
from "f1"."intermediate"."int_standings__drivers"
  );
