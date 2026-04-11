SELECT
    CAST(raw:c AS FLOAT) AS current_price,
    CAST(raw:d AS FLOAT) AS change_amount,
    CAST(raw:dp AS FLOAT) AS change_percent,
    CAST(raw:h AS FLOAT) AS day_high,
    CAST(raw:l AS FLOAT) AS day_low,
    CAST(raw:o AS FLOAT) AS day_open,
    CAST(raw:pc AS FLOAT) AS prev_close,
    CAST(raw:symbol AS STRING) AS symbol,
    CAST(raw:t AS timestamp) AS market_timestamp,
    CAST(raw:fetched_at AS timestamp) AS fetched_at
FROM
    {{ source("raw_data", "bronze_stock_quotes_raw") }}


