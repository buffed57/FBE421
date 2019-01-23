import pdfkit


path_wkthmltopdf = r'C:\Users\goetz\PDF_Reader\Lib\site-packages\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
pdfkit.from_url("https://www.sec.gov/Archives/edgar/data/1652044/000165204418000007/goog10-kq42017.htm", "out.pdf", configuration=config)

