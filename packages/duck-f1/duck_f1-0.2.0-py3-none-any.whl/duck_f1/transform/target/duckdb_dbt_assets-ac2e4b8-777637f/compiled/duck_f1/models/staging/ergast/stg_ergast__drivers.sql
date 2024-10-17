with
raw_drivers as (select * from "f1"."ingress"."ergast__drivers"),

formatted as (
    select
        md5(cast(coalesce(cast(forename as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(surname as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(dob as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT))
            as driver_id,
        driverid as _ergast_driver_id,
        driverref as driver_reference,
        if(number = '\N', null, number) as driver_number,
        if(code = '\N', null, code) as driver_code,
        forename as first_name,
        surname as last_name,
        concat_ws(' ', forename, surname) as full_name,
        dob as date_of_birth,
        datesub('y', date_of_birth, today())::integer as age_years,
        datesub('d', date_of_birth, today())::integer as age_days,
        concat(
            age_years,
            ' years, ',
            datesub('d', date_of_birth + to_years(age_years), today()),
            ' days'
        ) as age_label,
        nationality,
        url as wikipedia_url
    from raw_drivers
)

select
    *
from formatted