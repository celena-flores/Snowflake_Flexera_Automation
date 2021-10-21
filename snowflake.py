import csv
import json
import datetime
import fileinput

# fields I will pick from the csv. CBI_FIELD: CSV_FIELD
field_hash = {
  "CloudVendorAccountID": "Warehouse Id",
  "CloudVendorAccountName": "Warehouse Name",
  "Cost": "Bill Amount",
  "UsageStartTime": "Start Time",
#  "InvoiceID": "Order Number",
}

# Static Fields for each line
static_fields = {
  "Category": "SnowFlake",
  "UsageUnit": "Credits",
  "CurrencyCode": "USD",
  "LineItemType": "Usage",
  "ManufacturerName": "Snowflake",
}

tag_fields = {
#   "GL_Account": "GL Account",
#   "Profit_Center": "Profit Center",
# "Division_Name": "Division Name",
 "Department_Name": "Department Name",
 "Quarter": "Quarter",
 "Account_Type": "Account Type",
 "div": "Division Name"
}

deleteable_fields = [
  'CREDITS_USED_CLOUD_SERVICES',
  'Year',
  'Month',
  'CREDITS_USED_COMPUTE',
  'Date Range',
  'Number of Records',
  'End Time',
  "\u00ef\u00bb\u00bfCredits Used",
  "Order Number",
  "GL Account",
  "Profit Center"
]

jsonArray = []
with open('WAREHOUSE_METERING_HISTORY.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',',)
    for row in csv_reader:
        # Appending static fields
        for key, value in static_fields.items():
            row[key] = value
        # Updating row headers to CBI Generic
        for key, value in field_hash.items():
            row[key] = row.pop(str(value))
        # Adding in InvoiceYearMonth
        datetime_object = datetime.datetime.strptime(row['Month'], '%b')
        row["InvoiceYearMonth"] = ''.join([row['Year'],
                                          datetime_object.strftime('%m')])
        # add tags
        row["Tags"] = {}
        for key, value in tag_fields.items():
            row["Tags"][key] = row.pop(value, None)
        # remove dollar symbol from cost
        row['UsageAmount'] = float(
            float(row['CREDITS_USED_CLOUD_SERVICES']) +
            float(row['CREDITS_USED_COMPUTE'])
        )
        row['UsageStartTime'] = datetime.datetime.strptime(
            row['UsageStartTime'],
            '%m/%d/%Y %H:%M').strftime('%Y-%m-%dT%H:%M:%SZ')
        row['Cost'] = row['Cost'].replace('$', '').strip()
        # Cleaning up unused rows
        for item in deleteable_fields:
            del row[item]
        jsonArray.append(row)

with open('export.json', 'w', encoding='utf-8') as json_file:
    jsonString = json.dumps(jsonArray, indent=4)
    json_file.write(jsonString)

data_file = open('export.csv', 'w', newline='')
csv_writer = csv.writer(data_file)

count = 0
for data in jsonArray:
    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(data.values())

data_file.close()

for line in fileinput.input('export.csv', inplace=1):
    line = line.replace("'", "\"\"").rstrip()
    print(line)
