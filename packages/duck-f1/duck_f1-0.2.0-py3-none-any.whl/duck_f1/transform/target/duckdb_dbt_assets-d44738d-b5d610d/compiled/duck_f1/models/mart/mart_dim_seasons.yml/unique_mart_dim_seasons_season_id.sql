
    
    

select
    season_id as unique_field,
    count(*) as n_records

from "f1"."mart"."mart_dim_seasons"
where season_id is not null
group by season_id
having count(*) > 1


