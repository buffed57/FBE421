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


from tika import parser




filename2 = 'out.pdf'
parsedPDF2 = parser.from_file(filename2)
pdf2 = parsedPDF2["content"]
pdf2 = pdf2.replace('\n\n', '\n')



pdf2 = pdf2.splitlines()

# print(pdf2)
new_pdf = []
fin_data = []

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
pdf2 = [['shall be expressly set forth by specific reference in such filing.'], ['24'], ['Table of Contents Alphabet Inc.'], ['ITEM ', '6.', ' SELECTED FINANCIAL DATA'], ['The following selected consolidated financial data should be read in conjunction with Item ', '7', ' “Management’s Discussion and Analysis of Financial'], ['Condition and Results of Operations” and our consolidated financial statements and the related notes appearing in Item ', '8', ' “Financial Statements and'], ['Supplementary Data” of this Annual Report on Form ', '10', '-K. The historical results are not necessarily indicative of the results to be expected in any future'], ['period.'], [' Year Ended December ', '31', ','], [' ', '2013', '  ', '2014', '  ', '2015', '  ', '2016', '  ', '2017'], [' (in millions, except per share amounts)'], ['Consolidated Statements of Income Data:'], ['Revenues  ', '55,519', '   ', '66,001', '   ', '74,989', '   ', '90,272', '   ', '110,855'], ['Income from operations ', '15,403', '  ', '16,496', '  ', '19,360', '  ', '23,716', '  ', '26,146'], ['Net income from continuing operations ', '13,160', '  ', '13,620', '  ', '16,348', '  ', '19,478', '  ', '12,662'], ['Net income (loss) from discontinued operations ', '-427', '  ', '516', '  ', '0', '  ', '0', '  ', '0'], ['Net income ', '12,733', '  ', '14,136', '  ', '16,348', '  ', '19,478', '  ', '12,662'], ['          '], ['Basic net income (loss) per share of Class A and B common stock:'], ['Continuing operations  ', '19.77', '   ', '20.15', '   ', '23.11', '   ', '28.32', '   ', '18.27'], ['Discontinued operations ', '-0.64', '  ', '0.76', '  ', '0.00', '  ', '0.00', '  ', '0.00'], ['Basic net income per share of Class A and B'], ['common stock  ', '19.13', '   ', '20.91', '   ', '23.11', '   ', '28.32', '   ', '18.27'], ['          '], ['Basic net income (loss) per share of Class C capital stock:'], ['Continuing operations  ', '19.77', '   ', '20.15', '   ', '24.63', '   ', '28.32', '   ', '18.27'], ['Discontinued operations ', '-0.64', '  ', '0.76', '  ', '0.00', '  ', '0.00', '  ', '0.00'], ['Basic net income per share of Class C capital stock  ', '19.13', '   ', '20.91', '   ', '24.63', '   ', '28.32', '   ', '18.27'], ['          '], ['Diluted net income (loss) per share of Class A and B common stock:'], ['Continuing operations  ', '19.42', '   ', '19.82', '   ', '22.84', '   ', '27.85', '   ', '18.00'], ['Discontinued operations ', '-0.63', '  ', '0.75', '  ', '0.00', '  ', '0.00', '  ', '0.00'], ['Diluted net income per share of Class A and B'], ['common stock  ', '18.79', '   ', '20.57', '   ', '22.84', '   ', '27.85', '   ', '18.00'], ['          '], ['Diluted net income (loss) per share of Class C capital stock:'], ['Continuing operations  ', '19.42', '   ', '19.82', '   ', '24.34', '   ', '27.85', '   ', '18.00'], ['Discontinued operations ', '-0.63', '  ', '0.75', '  ', '0.00', '  ', '0.00', '  ', '0.00'], ['Diluted net income per share of Class C capital stock  ', '18.79', '   ', '20.57', '   ', '24.34', '   ', '27.85', '   ', '18.00'], [' As of December ', '31', ','], [' ', '2013', '  ', '2014', '  ', '2015', '  ', '2016', '  ', '2017'], [' (in millions)'], ['Consolidated Balance Sheet Data:'], ['Cash, cash equivalents, and marketable securities  ', '58,717', '   ', '64,395', '   ', '73,066', '   ', '86,333', '   ', '101,871'], ['Total assets  ', '109,050', '   ', '129,187', '   ', '147,461', '   ', '167,497', '   ', '197,295'], ['Total long-term liabilities  ', '6,165', '   ', '8,548', '   ', '7,820', '   ', '11,705', '   ', '20,610'], ['Total stockholders’ equity  ', '86,977', '   ', '103,860', '   ', '120,331', '   ', '139,036', '   ', '152,502'], ['25'], ['Table of Contents Alphabet Inc.']]
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
        while unit < (len(pdf2[spot])):
            if (unit + 1) < (len(pdf2[spot])) and pdf2[spot][unit + 1].isdigit() and pdf2[spot][unit] == '(':
                if stringer:
                    temp_list.append(stringer)
                    stringer = ''
                running = True
                neg_num = '-'
                while running:
                    if (pdf2[spot][unit + 1].isdigit() or pdf2[spot][unit + 1] == ',') and (unit + 1) < len(pdf2[spot]):
                        neg_num += pdf2[spot][unit + 1]
                        unit += 1
                    elif pdf2[spot][unit + 1] == '.':
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
                    if pdf2[spot][unit + 1].isdigit() or pdf2[spot][unit + 1] == ',' or pdf2[spot][unit+1] == '.':
                        while (unit + 1) < len(pdf2[spot]) and (pdf2[spot][unit].isdigit() or pdf2[spot][unit] == ','or
                                                                pdf2[spot][unit] == '.'):
                            stringer_num += pdf2[spot][unit]
                            unit += 1
                            if (unit + 1) == len(pdf2[spot]):
                                break
                        if pdf2[spot][unit].isdigit():
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
            temp_list.append(stringer_num)
    # print(temp_list)
    if temp_list:
        new_pdf.append(temp_list)
    spot += 1

    # print(new_pdf)


print(new_pdf)
company_data = {}
def get_title_info(beg_index, end_index,pdf):
    first_half_running = True
    beg_count = beg_index
    while first_half_running and beg_count < end_index:
        end_num = (len(pdf[beg_count]) - 1)




def check_if_valid_data(pdf,pdf_section):
    # checks if data has valid data in it
    # Find begning of page and end and notes all indexs between the two
    first_running = True
    start_index = pdf_section
    beg_index = 0
    end_index = 0
    pdf_section -= 1
    while first_running:
        if len(pdf[pdf_section]) == 1:
            if len(pdf[pdf_section][0]) == 2 or len(pdf[pdf_section][0]) == 3:
                #print(pdf[pdf_section])
                first_running = False
                last_running = True
                beg_index = pdf_section + 1
                pdf_section = start_index
                while last_running:
                    if len(pdf[pdf_section]) == 1:
                        if len(pdf[pdf_section][0]) == 2 or len(pdf[pdf_section][0]) == 3:
                            #print(pdf[pdf_section])
                            last_running = False
                            end_index = pdf_section - 1
                            #return(beg_index,end_index)
                            break
                        else:
                            pdf_section += 1
                    else:
                        pdf_section += 1
            else:
                pdf_section -= 1
        else:
            pdf_section -= 1
    get_title_info(beg_index,end_index,pdf)

def extract_data_from_pdf(pdf):
    # pulls financial data from pdf list
    pdf_section = 0
    while pdf_section < len(pdf):
        if any(char in section for char in date_words for section in pdf[pdf_section]):
            print(check_if_valid_data(pdf,pdf_section))
            print(pdf[pdf_section])
            break
        else:
            pdf_section += 1

extract_data_from_pdf(new_pdf)