#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import glob
import os
import re
import sys
import pandas as pd
from pandas import ExcelWriter
# import xlsxwriter

import matplotlib

matplotlib.use('AGG')
import matplotlib.pyplot as plt
# pd.options.display.mpl_style = 'default'

from tika import parser


# input_path = sys.argv[1]

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
# for input_file in glob.glob(os.path.join('SummaryCharts', '*.pdf')):
# Grab the PDF's file name
filename = 'SummaryCharts.pdf'
filename2 = 'out.pdf'
parsedPDF2 = parser.from_file(filename2)
pdf2 = parsedPDF2["content"]
pdf2 = pdf2.replace('\n\n', '\n')
# print(pdf2)
# print(filename)
# Remove .pdf from the filename so we can use it as the name of the plot and PNG


# Use Tika to parse the PDF
parsedPDF = parser.from_file('SummaryCharts.pdf')
# print(parsedPDF)
# Extract the text content from the parsed PDF
pdf = parsedPDF["content"]
# print(pdf)
# Convert double newlines into single newlines
pdf = pdf.replace('\n\n', '\n')
# print(pdf)

# Create a Pandas DataFrame from the lines of text in the Expenditures table in the PDF
# expense_df = create_df(pdf, expenditures_pattern, expense_pattern, expense_columns)
# Create a Pandas DataFrame from the lines of text in the Revenues table in the PDF
# revenue_df = create_df(pdf, revenues_pattern, revenue_pattern, revenue_columns)
# print(revenue_df)
# revenue_df2 = create_df_2(pdf2, out_pattern, out_pattern2, out_column)
# print(expense_df)
# print(revenue_df)
# print(revenue_df2)
# print(pdf2)


pdf2 = pdf2.splitlines()
"""
pdf2 = [['27'], ['Table of Contents Alphabet Inc.'], ['Revenues'],\
 ['The following table presents our revenues, by segment and revenue source (in millions):'], \
 [' Year Ended December ', '31', ','], [' ', '2015', '  ', '2016', '  ', '2017'], ['Google segment      '],\
  ['Google properties revenues  ', '52,357', '   ', '63,785', '   ', '77,788'],\
   ["Google Network Members' properties revenues ", '15,033', '  ', '15,598', '  ', '17,587'],\
    ['Google advertising revenues ', '67,390', '  ', '79,383', '  ', '95,375'],\
     ['Google other revenues ', '7,154', '  ', '10,080', '  ', '14,277'],\
      ['Google segment revenues  ', '74,544', '   ', '89,463', '   ', '109,652'], ['      '], ['Other Bets      '], \
      ['Other Bets revenues  ', '445', '   ', '809', '   ', '1,203'], ['      '], \
      ['Revenues  ', '74,989', '   ', '90,272', '   ', '110,855'], ['Google segment'], \
      ['The following table presents our Google segment revenues (in millions), and changes in our aggregate paid\
       clicks and cost-per-click (expressed as']]
"""
# print(pdf2)
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
fin_info_list = []
date_words = ["Year Ended", "As of", "Three Months Ended", "Twelve Months Ended", "Quarter Ended", \
              "Payments Due By Period", "January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", \
              "November", "December", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
              "Dec"]
char_list = [',', '.', '/', "'", '"', '(', ')', '[', ']', '|', '-', 'a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', \
             'e', 'E', 'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', \
             'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y',
             'Y', 'z', 'Z']
spot = 0
income_statement = {}
for spot in range(len(pdf2) - 1):
    # print(spot)
    # spot = re.sub(' +', ' ', spot)
    # print(spot)
    stringer = ''
    count = 0
    temp_list = []
    stringer_num = ''
    if spot:
        unit = 0
        # print(str(len(spot)))
        while unit < (len(pdf2[spot])):
            #   print(str(unit))
            #  print(str(spot[unit]))

            # print(spot[unit])

            if (unit + 1) < (len(pdf2[spot])) and pdf2[spot][unit + 1].isdigit() and pdf2[spot][unit] == '(':
                if stringer:
                    temp_list.append(stringer)
                    stringer = ''
                running = True
                neg_num = '-'
                while running:
                    if pdf2[spot][unit + 1].isdigit() or pdf2[spot][unit + 1] == ',' and (unit + 1) < len(pdf2[spot]):
                        neg_num += pdf2[spot][unit + 1]
                        unit += 1
                    else:
                        if pdf2[spot][unit + 1] != ')':
                            neg_num += pdf2[spot][unit + 1]
                        unit += 2
                        temp_list.append(neg_num)
                        running = False
            elif pdf2[spot][unit].isalpha() or pdf2[spot][unit] in char_list:
                if stringer_num:
                    temp_list.append(stringer_num)
                    stringer_num = ''
                stringer += pdf2[spot][unit]
                unit += 1
            elif pdf2[spot][unit].isdigit():
                if stringer:
                    temp_list.append(stringer)
                    stringer = ''
                if (unit + 1) < len(pdf2[spot]):
                    if pdf2[spot][unit + 1].isdigit() or pdf2[spot][unit + 1] == ',':
                        while (unit + 1) < len(pdf2[spot]) and pdf2[spot][unit].isdigit() or pdf2[spot][unit] == ',':
                            if (unit + 1) == len(pdf2[spot]) and pdf2[spot][unit].isdigit():
                                stringer_num += spot[unit]
                                unit += 1
                            if (unit + 1) == len(pdf2[spot]) and pdf2[spot][unit] == ',':
                                temp_list.append(stringer_num)
                                stringer_num = ''
                                stringer += spot[unit]
                                unit += 1
                            else:
                                stringer_num += pdf2[spot][unit]
                                unit += 1
                            if (unit + 1) == len(pdf2[spot]):
                                break
                        if (pdf2[spot][unit].isdigit()):
                            stringer_num += pdf2[spot][unit]
                            temp_list.append(stringer_num)
                            stringer_num = ''
                            unit += 1
                        else:
                            temp_list.append(stringer_num)
                            stringer_num = ''
                            stringer += pdf2[spot][unit]
                            unit += 1
                    else:
                        stringer_num += pdf2[spot][unit]
                        temp_list.append(stringer_num)
                        stringer_num = ''
                        unit += 1
                else:
                    stringer_num += pdf2[spot][unit]
                    temp_list.append(stringer_num)
                    stringer_num = ''
                    unit += 1
            else:
                if stringer_num:
                    temp_list.append(stringer_num)
                    stringer_num = ''
                if pdf2[spot][unit] != '$':
                    stringer += pdf2[spot][unit]
                    unit += 1
                else:
                    unit += 1
        if stringer:
            temp_list.append(stringer)
        if stringer_num:
            temp_list.append((stringer_num))
    #print(temp_list)
    if temp_list:

        if any(char in temp_list[count] for char in date_words):
            print(pdf2[spot + 1])
            if pdf2[spot+1] and len(pdf2[spot + 1]) > 1 and pdf2[spot + 1][1].isdigit():
                spot += 1
                year_list = []
                for year in pdf2[spot]:
                    #print(year)
                    if year.isdigit():
                        year_list.append(year)

                income_statement['Years'] = year_list
                spot += 1
                temp_num_list = []
                temp_info_name = ''
                going = True
                while going and spot <= (len(pdf2)-1):
                    end_num = (len(pdf2[spot]) - 1)
                    print(pdf2[spot])
                    if pdf2[spot][end_num][0].isdigit() or pdf2[spot][end_num][0] == '-':
                        running = True
                        info_count = (len(pdf2[spot]) - 1)
                        #print(pdf2[spot])
                        while running:
                            print(pdf2[spot])
                            if pdf2[spot][info_count][0].isdigit() or pdf2[spot][info_count][0] == '-':
                                temp_num_list.append(pdf2[spot][info_count])
                                info_count -= 1
                            elif pdf2[spot][info_count][0].isalpha():
                                #print(pdf2[spot])
                                if temp_num_list:
                                    temp_num_list = list(reversed(temp_num_list))
                                    nameBuild = True
                                    while nameBuild:
                                        if info_count > 0:
                                            temp_info_name += pdf2[spot][info_count]
                                            info_count -= 1
                                        else:
                                            temp_info_name += pdf2[spot][info_count]
                                            income_statement[temp_info_name] = temp_num_list.copy()
                                            #print(income_statement)
                                            temp_info_name = ''
                                            del temp_num_list[:]
                                            nameBuild = False
                                            spot += 1
                                            if spot < len(pdf2)-1:
                                                info_count = len(pdf2[spot]) - 1
                                            else:
                                                #print(pdf2[spot])
                                                running = False
                                else:
                                    nameBuilder = True
                                    while nameBuilder:
                                        if info_count > 0:
                                            temp_info_name += pdf2[spot][info_count]
                                            info_count -= 1
                                        else:
                                            temp_info_name += pdf2[spot][info_count]
                                            income_statement[temp_info_name] = temp_num_list.copy()
                                            temp_info_name = ''
                                            nameBuilder = False
                                            spot += 1
                                            if spot < len(pdf2)-1:
                                                info_count = len(pdf2[spot]) - 1
                                            else:
                                                #print(pdf2[spot])
                                                running = False

                            else:
                                if info_count > 0:
                                    info_count -= 1
                                else:
                                    spot += 1
                                    running = False
                    else:
                        if spot < (len(pdf2) - 1):
                            last_num = len(pdf2[spot + 1]) - 1
                            if pdf2[spot + 1][last_num][0].isdigit() or pdf2[spot + 1][last_num][0] == '-':
                                title_name = str(pdf2[spot])
                                income_statement[title_name] = []
                                spot += 1
                        else:
                            going = False
            else:
                spot += 1
        new_pdf.append(temp_list)

    spot += 1

    # print(new_pdf)
print(new_pdf)
print(fin_info_list)
print(income_statement)
# print(new_pdf)
# Print the total expenditures and total revenues in the budget to the screen
# print("Total Expenditures: {}".format(expense_df["Totals"].sum()))
# print("Total Revenues: {}\n".format(revenue_df["Total"].sum()))

"""writer = pd.ExcelWriter('PythonExport.xlsx', engine='xlsxwriter')
expense_df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()"""

""" if len(temp_list) > 2:
            temp_line = ''
            temp_line2 = ''
            count = 1
            print(str(count))
            running = True
            print(temp_list)
            print('In loop')
            while running:
                    print(str(count))
                    if temp_list[count] == ' ' or temp_list[count] == '':
                        del temp_list[count]
                        if len(temp_list) <= 2:
                            running = False
                        temp_list[count - 1] += ' ' + temp_line + ' ' + temp_line2
                    elif any(char in temp_list[count-1] for char in char_list) and \
                            temp_list[count][0].isdigit() and \
                            any(char in temp_list[count+1] for char in char_list):
                        temp_line = temp_list[count]
                        temp_line2 = temp_list[count+1]
                        del temp_list[count]
                        del temp_list[count]
                        temp_list[count-1] += ' ' + temp_line + ' ' + temp_line2
                        #print(temp_list[count])
                        print('1')
                        if len(temp_list) <= 2:
                            running = False
                    elif temp_list[count-1].isdigit() and any(char in temp_list[count] for char in char_list):
                        temp_line = temp_list[count]
                        temp_line2 = temp_list[count + 1]
                        del temp_list[count]
                        del temp_list[count]
                        temp_list[count - 1] += ' ' + temp_line + ' ' + temp_line2
                        print('2')
                        if len(temp_list) <= 2:
                            running = False
                    elif len(temp_list) == 3:
                        print(' 3')
                        running = False
                    else:
                        print('4')
                        if (count+1) >= len(temp_list):
                            running = False
                        else:
                            count += 1"""