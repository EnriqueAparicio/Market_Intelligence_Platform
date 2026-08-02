select
    cast(ingested_at as timestamp_ntz) as ingested_at,
    trim(repository_name) as repository_name,
    trim(default_branch) as default_branch,
    trim(visibility) as visibility,
    cast(stars as number) as stars,
    cast(forks as number) as forks,
    cast(open_issues as number) as open_issues,
    raw_payload
from {{ source('raw', 'GITHUB_REPOSITORY_SNAPSHOT') }}
