from tika import  parser

file = "WalmartIncome2.pdf"
file_data = parser.from_file(file)
# Get files text content
text = file_data['content']
print(text)