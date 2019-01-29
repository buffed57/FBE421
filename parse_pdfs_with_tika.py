#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import glob
import os
import re
import sys
import pandas as pd
from pandas import ExcelWriter
import xlsxwriter

import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
#pd.options.display.mpl_style = 'default'

from tika import parser

#input_path = sys.argv[1]

def create_df(pdf_content, content_pattern, line_pattern, column_headings):
    """Create a Pandas DataFrame from lines of text in a PDF.

    Arguments:
    pdf_content -- all of the text Tika parses from the PDF
    content_pattern -- a pattern that identifies the set of lines
    that will become rows in the DataFrame
    line_pattern -- a pattern that separates the agency name or revenue source
    from the dollar values in the line
    column_headings -- the list of column headings for the DataFrame
    """
    list_of_line_items = []
    # Grab all of the lines of text that match the pattern in content_pattern
    content_match = re.search('\w', pdf_content, re.DOTALL)
    print(content_match)
    # group(1): only keep the lines between the parentheses in the pattern
    content_match = content_match.group(1)
    # Split on newlines to create a sequence of strings
    content_match = content_match.split('\n')
    # Iterate over each line
    for item in content_match:
        # Create a list to hold the values in the line we want to retain
        line_items = []
        # Use line_pattern to separate the agency name or revenue source
        # from the dollar values in the line
        line_match = re.search(line_pattern, item, re.I)
        # Grab the agency name or revenue source, strip whitespace, and remove commas
        # group(1): the value inside the first set of parentheses in line_pattern
        agency = line_match.group(1).strip().replace(',', '')
        # Grab the dollar values, strip whitespace, replace dashes with 0.0, and remove $s and commas
        # group(2): the value inside the second set of parentheses in line_pattern
        values_string = line_match.group(2).strip().\
        replace('- ', '0.0 ').replace('$', '').replace(',', '')
        # Split on whitespace and convert to float to create a sequence of floating-point numbers
        values = map(float, values_string.split())
        # Append the agency name or revenue source into line_items
        line_items.append(agency)
        # Extend the floating-point numbers into line_items so line_items remains one list
        line_items.extend(values)
        # Append line_item's values into list_of_line_items to generate a list of lists;
        # all of the lines that will become rows in the DataFrame
        list_of_line_items.append(line_items)
    # Convert the list of lists into a Pandas DataFrame and specify the column headings
    df = pd.DataFrame(list_of_line_items, columns=column_headings)
    return df


# In the Expenditures table, grab all of the lines between Totals and General Government
expenditures_pattern = r'Net Income\n+(Revenues.*?)\nCosts and expenses:'
IncomeS = '(Net Sales(Revenues)Revenues)'


# In the Revenues table, grab all of the lines between 2015-16 and either Subtotal or Total
revenues_pattern = r'\d{4}-\d{2}\n(Personal Income Tax.*?)\n +[Subtotal|Total]'

# For the expenditures, grab the agency name in the first set of parentheses
# and grab the dollar values in the second set of parentheses
expense_pattern = r'(Net sales|[a-z,& -]+)([$,0-9 -]+)'

# For the revenues, grab the revenue source in the first set of parentheses
# and grab the dollar values in the second set of parentheses
revenue_pattern = r'([a-z, ]+)([$,0-9 -]+)'

# Column headings for the Expenditures DataFrames
expense_columns = ['2018', '2017', '2016']

# Column headings for the Revenues DataFrames
revenue_columns = ['Source', 'General', 'Special', 'Total', 'Change']

# Iterate over all PDF files in the folder and process each one in turn
#for input_file in glob.glob(os.path.join('SummaryCharts', '*.pdf')):
    # Grab the PDF's file name
filename = 'out.pdf'
    #print(filename)
    # Remove .pdf from the filename so we can use it as the name of the plot and PNG


    # Use Tika to parse the PDF
parsedPDF = parser.from_file('out.pdf')
#print(parsedPDF)
    # Extract the text content from the parsed PDF
pdf = parsedPDF["content"]
#print(pdf)
    # Convert double newlines into single newlines
pdf = pdf.replace('\n\n', '\n')
#print(pdf)

    # Create a Pandas DataFrame from the lines of text in the Expenditures table in the PDF
expense_df = create_df(pdf, IncomeS, expense_pattern, expense_columns)
    # Create a Pandas DataFrame from the lines of text in the Revenues table in the PDF
#revenue_df = create_df(pdf, revenues_pattern, revenue_pattern, revenue_columns)
print(expense_df)
#print(revenue_df)

    # Print the total expenditures and total revenues in the budget to the screen
#print("Total Expenditures: {}".format(expense_df["Totals"].sum()))
#print("Total Revenues: {}\n".format(revenue_df["Total"].sum()))

"""writer = pd.ExcelWriter('PythonExport.xlsx', engine='xlsxwriter')
expense_df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()"""



