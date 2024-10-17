
  
  create view "f1"."mart"."mart__fct_race__constructor_classification__dbt_tmp" as (
    select *
from "f1"."staging"."stg_ergast__race__constructor_classification"
  );
