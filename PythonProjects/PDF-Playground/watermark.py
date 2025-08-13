import PyPDF2 
import sys

waterMark = sys.argv[1]
file = sys.argv[2:]

def WaterMarkFiles(waterMark, files):

    weiter = PyPDF2.PdfFileWriter()
    for file in files:
        reader = PyPDF2.PdfFileReader(file)

        page_indexes = list(range(0,len(reader.pages)))
        for index in page_indexes:
            reader_stamp = PyPDF2.PdfFileReader(waterMark)
            image_page = reader_stamp.pages[0]
            page =  reader.getPage(index)
            media_box = page.mediaBox
            image_page.mergePage(page)
            image_page.mediaBox = media_box
            weiter.addPage(image_page)
        with open(f"./WaterMarks/{file}","wb") as pf:
            weiter.write(pf)

WaterMarkFiles(waterMark=waterMark, files=file)