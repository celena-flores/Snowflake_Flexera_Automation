# Snowflake_Flexera_Automation

## Requirements

- File named WAREHOUSE_METERING_HISTORY.csv
- python, requests
- Your refresh token

## Instructions

- open WAREHOUSE_METERING_HISTORY.csv with excel and save it again to update timestamps
- run `python snowflake.py`
- run `python bill_upload.py $REFRESH_TOKEN 27915 cbi-oi-optima-snowflake-1 2021-10 export.csv`
