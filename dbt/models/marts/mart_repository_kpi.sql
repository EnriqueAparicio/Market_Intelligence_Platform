with base as (
    select
        cast(ingested_at as date) as metric_date,
        repository_name,
        stars,
        forks,
        open_issues
    from {{ ref('stg_github_repository_snapshot') }}
),
daily as (
    select
        metric_date,
        repository_name,
        max(stars) as stars,
        max(forks) as forks,
        max(open_issues) as open_issues
    from base
    group by 1, 2
)
select
    metric_date,
    repository_name,
    (stars * 1.0 + forks * 2.0 - open_issues * 0.5) as popularity_score,
    (stars - lag(stars) over (partition by repository_name order by metric_date)) as change_vs_prev_day
from daily
