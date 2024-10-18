Using python, I want to take a pandas df and format it to a excel file using xlsxwriter.

Here's my code at the moment:

```python
import pandas as pd
import xlsxwriter

from sqlalchemy import create_engine

engine = create_engine("postgresql://fastapi:fastapi@localhost:5432/barbatus-db")

df = pd.read_sql_table("csrd", engine)
df = df.sort_values(by=["standard_id", "section_id", "subsection_id", "indicator_id"], ascending=False)
df = df[::-1].reset_index(drop=True)

cols = ["standard_id", "section_id", "subsection_id", "indicator_id", "top_down"]
df[cols].to_dict(orient="records")


# Create a new Excel file and add a worksheet
workbook = xlsxwriter.Workbook("esrs.xlsx")
worksheet = workbook.add_worksheet()

# Define formats
title_format = workbook.add_format({"bold": True, "align": "center", "valign": "vcenter", "border": 2})
summary_format = workbook.add_format({"align": "center", "valign": "vcenter"})


# Start writing data
row = 0

for index, record in df.iterrows():
    # Determine the last non-null element
    last_non_null = record["indicator_id"] or record["subsection_id"] or record["section_id"] or record["standard_id"]

    # Determine the hierarchy level
    hierarchy_level = (
        "Indicator"
        if record["indicator_id"]
        else "Subsection"
        if record["subsection_id"]
        else "Section"
        if record["section_id"]
        else "Standard"
    )

    # Write the last non-null element in column B
    worksheet.merge_range(row, 1, row + 4, 1, last_non_null, title_format)

    # Write the title in columns C to L
    worksheet.merge_range(row, 2, row, 11, f"{hierarchy_level} Title: {last_non_null}", title_format)

    # If a summary is provided, write it in the next 4 rows
    # Here, we assume a summary is provided if the 'summary' column exists and is not null
    if "summary" in record and pd.notnull(record["summary"]):
        worksheet.merge_range(row + 1, 2, row + 4, 11, record["summary"], summary_format)
        row += 5  # Move to the next block, leaving a space
    else:
        row += 1  # Move to the next block, leaving a space

    # Leave a space between blocks
    row += 1

# Close the workbook
workbook.close()

```

Things I want to improve:

- have border around each big block, and not individually, for the title and the id
- improve the display of the summary text. at the moment, it is on one line, and is not readable at all. Especially since it is a text formatted in markdown, and excel don't take into account `\n` etc...
