with
raw_seasons as (select * from "f1"."ingress"."ergast__seasons"),

formatted as (
    select
        year,
        url as wikipedia_url,
        md5(year::varchar) as season_id
    from raw_seasons
)

select *
from formatted