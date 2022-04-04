WITH github as (
  SELECT * from {{ ref('base_github') }}
),

final AS(
  SELECT
    DATE(event_ts) as event_date,
    event_id,
    user_id,
    event_type,
    is_public
  FROM github
)

SELECT * from final