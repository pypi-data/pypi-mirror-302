
  
  create view "f1"."mart"."mart_fct_sprint__driver_classification__dbt_tmp" as (
    select *
from "f1"."staging"."stg_ergast__sprint__driver_classification"
  );
