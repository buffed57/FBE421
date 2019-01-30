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
    content_match = re.search(content_pattern, pdf_content, re.DOTALL)

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


def create_df_2(pdf_content, content_pattern, line_pattern, column_headings):
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
    content_match = re.search(content_pattern, pdf_content, re.DOTALL)

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
        values_string = line_match.group(2).strip(). \
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
expenditures_pattern = r'Totals\n+(Legislative, Judicial, Executive.*?)\nGeneral Government:'
out_pattern = r'CONSOLIDATED STATEMENT OF INCOME'
out_pattern2 = r'([a-z, ]+)([$,0-9 -]+)'
out_column = r'Source', '2015', '2016', '2017'

# In the Revenues table, grab all of the lines between 2015-16 and either Subtotal or Total
revenues_pattern = r'\d{4}-\d{2}\n(Personal Income Tax.*?)\n +[Subtotal|Total]'

# For the expenditures, grab the agency name in the first set of parentheses
# and grab the dollar values in the second set of parentheses
expense_pattern = r'(K-12 Education|[a-z,& -]+)([$,0-9 -]+)'

# For the revenues, grab the revenue source in the first set of parentheses
# and grab the dollar values in the second set of parentheses
revenue_pattern = r'([a-z, ]+)([$,0-9 -]+)'

# Column headings for the Expenditures DataFrames
expense_columns = ['Agency', 'General', 'Special', 'Bond', 'Totals']

# Column headings for the Revenues DataFrames
revenue_columns = ['Source', 'General', 'Special', 'Total', 'Change']

# Iterate over all PDF files in the folder and process each one in turn
#for input_file in glob.glob(os.path.join('SummaryCharts', '*.pdf')):
    # Grab the PDF's file name
filename = 'SummaryCharts.pdf'
filename2 = 'out.pdf'
parsedPDF2 = parser.from_file(filename2)
pdf2 = parsedPDF2["content"]
pdf2 = pdf2.replace('\n\n', '\n')
#print(pdf2)
    #print(filename)
    # Remove .pdf from the filename so we can use it as the name of the plot and PNG


    # Use Tika to parse the PDF
parsedPDF = parser.from_file('SummaryCharts.pdf')
#print(parsedPDF)
    # Extract the text content from the parsed PDF
pdf = parsedPDF["content"]
#print(pdf)
    # Convert double newlines into single newlines
pdf = pdf.replace('\n\n', '\n')
#print(pdf)

    # Create a Pandas DataFrame from the lines of text in the Expenditures table in the PDF
#expense_df = create_df(pdf, expenditures_pattern, expense_pattern, expense_columns)
    # Create a Pandas DataFrame from the lines of text in the Revenues table in the PDF
#revenue_df = create_df(pdf, revenues_pattern, revenue_pattern, revenue_columns)
#print(revenue_df)
#revenue_df2 = create_df_2(pdf2, out_pattern, out_pattern2, out_column)
#print(expense_df)
#print(revenue_df)
#print(revenue_df2)
#print(pdf2)
pdf2 = pdf2.splitlines()

print(pdf2)
new_pdf = []
fin_data = []
"""for spot in range(len(pdf2)):
    temp_list = re.findall(r'[A-Za-z]+|(\d+,\d+|\d+)+| \("(.*?)"\)', pdf2[spot])
    new_pdf.append(temp_list)
    list_builder = []
    string_builder = ''
    for unit in range(len(temp_list)):
        print(temp_list[unit])
        if temp_list[unit].isalpha():
            print("yes")
            string_builder += " " + temp_list[unit]
            if unit == len(temp_list)-1:
                list_builder.append(string_builder)
        else:

            if not string_builder:
                print("adding " + temp_list[unit])
                list_builder.append(temp_list[unit])

            else:
                print("adding "+string_builder)
                list_builder.append(string_builder)
                list_builder.append(temp_list[unit])
    print(list_builder)
    fin_data.append(list_builder)
print(fin_data)"""


char_list = [',','.','/',"'",'"','(',')','[',']','|']
for spot in pdf2:
    print(spot)
    spot = re.sub(' +', ' ', spot)
    #print(spot)
    stringer = ''
    count = 0
    temp_list = []
    stringer_num = ''
    if spot:
        for unit in range(len(spot)):

            #print(spot[unit])

            if (unit+1) < (len(spot)) and spot[unit+1].isdigit() and spot[unit] == '(':
                running = True
                neg_num = '-'
                while running:
                    if spot[unit+1].isdigit() or spot[unit+1] == ',' and (unit+1) < len(spot):
                        neg_num += spot[unit+1]
                        unit += 1
                    else:
                        if spot[unit+1] != ')':
                            neg_num += spot[unit+1]
                        unit += 1
                        temp_list.append(neg_num)
                        running = False
            elif spot[unit].isalpha() or spot[unit] in char_list:
                if stringer_num:
                    temp_list.append(stringer_num)
                    stringer_num = ''
                stringer += spot[unit]
            elif spot[unit].isdigit():
                if stringer:
                    temp_list.append(stringer)
                    stringer = ''
                if (unit+1) < (len(spot)):

                    while spot[unit].isdigit() or spot[unit] == ',' and (unit) < (len(spot)):
                        stringer_num += spot[unit]
                        print(stringer_num + ' ' + str(unit) + '/' + str(len(spot)-1))
                        if (unit+1) < len(spot):
                            unit += 1
                        else:
                            print(stringer_num)
                            #stringer_num += spot[unit]
                            temp_list.append(stringer_num)
                            stringer_num = ''
                            unit += 1
                            break
                else:
                    temp_list.append(stringer_num)
                    stringer_num = ''
            else:
                if stringer_num:
                    temp_list.append(stringer_num)
                    stringer_num = ''
                stringer += spot[unit]
        if stringer:
            temp_list.append(stringer)
        if stringer_num:
            temp_list.append((stringer_num))

    if temp_list:
        new_pdf.append(temp_list)
print(new_pdf)

        #print(unit)
#print(new_pdf)
    # Print the total expenditures and total revenues in the budget to the screen
#print("Total Expenditures: {}".format(expense_df["Totals"].sum()))
#print("Total Revenues: {}\n".format(revenue_df["Total"].sum()))

"""writer = pd.ExcelWriter('PythonExport.xlsx', engine='xlsxwriter')
expense_df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()"""



