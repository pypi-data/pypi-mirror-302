
  
  create view "f1"."mart"."fct_standings__constructors__dbt_tmp" as (
    select *
from "f1"."intermediate"."int_standings__constructors"
  );
