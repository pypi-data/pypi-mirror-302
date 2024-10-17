with
raw_drivers as (select * from "f1"."ingress"."ergast__drivers"),

formatted as (
    select
        md5(cast(coalesce(cast(forename as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(surname as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(dob as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT))
            as driver_id,
        driverid as _ergast_driver_id,
        driverref as driver_reference,
        if(number = '\N', null, number)::integer as driver_number,
        forename as first_name,
        surname as last_name,
        concat_ws(' ', forename, surname) as full_name,
        upper(
            concat(
                replace(strip_accents(first_name), ' ', '')[0:3],
                replace(strip_accents(last_name), ' ', '')[0:3]
            )
        ) as _live_timing_driver,
        if(code = '\N', upper(replace(strip_accents(last_name), ' ', ''))[0:3], code) as driver_code,
        if(code = '\N', true, false) as is_driver_code_generated,
        dob::date as date_of_birth,
        row_number() over (partition by _live_timing_driver order by date_of_birth) as _driver_id_rank,
        format('{:s}{:02d}', _live_timing_driver, _driver_id_rank) as _live_timing_driver_id,
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