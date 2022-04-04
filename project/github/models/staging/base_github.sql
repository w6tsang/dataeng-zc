WITH source AS (
  SELECT * FROM {{ source('staging','github_all')}}
  limit 100
),

flattened AS (
  SELECT
    REPLACE(json_extract(json_value, '$.id'), '"', '') AS event_id,
    REPLACE(json_extract(json_value, '$.actor.id'), '"', '') AS user_id,
    REPLACE(json_extract(json_value, '$.type'), '"', '') AS event_type,
    REPLACE(json_extract(json_value, '$.public'), '"', '') AS is_public,
    REPLACE(json_extract(json_value, '$.payload'), '"', '') AS payload,
    REPLACE(json_extract(json_value, '$.created_at'), '"', '') AS event_ts,
  FROM source
)

SELECT * FROM flattened
