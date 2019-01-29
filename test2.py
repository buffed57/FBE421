import pdfkit

path_wkthmltopdf = r'C:\Users\goetz\Anaconda3\envs\test\Lib\site-packages\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
#pdfkit.from_url("https://www.sec.gov/Archives/edgar/data/1652044/000165204418000007/goog10-kq42017.htm#sED35F0F0C5D48853983C78DBC5220BE3", "out.pdf", configuration=config)

fp = open('out.pdf', 'rb')
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
parser = PDFParser(fp)
doc = PDFDocument()
parser.set_document(doc)
doc.set_parser(parser)
doc.initialize('')
rsrcmgr = PDFResourceManager()
laparams = LAParams()
laparams.char_margin = 1.0
laparams.word_margin = 1.0
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
extracted_text = ''
for page in doc.get_pages():
    interpreter.process_page(page)
    layout = device.get_result()
    for lt_obj in layout:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            extracted_text += lt_obj.get_text()
print(extracted_text)

