from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pypdf import PdfReader, PdfWriter
import io

app = FastAPI()

@app.post("/split", summary="Split a PDF into individual pages.", operation_id="splitPdf")
async def split_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are accepted.")

    try:
        file_contents = await file.read()
        pdf_reader = PyPDF2.PdfFileReader(io.BytesIO(file_contents))
        num_pages = pdf_reader.getNumPages()
        pages = []

        for i in range(num_pages):
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.addPage(pdf_reader.getPage(i))
            output = io.BytesIO()
            pdf_writer.write(output)
            output.seek(0)
            # For now, we're just returning a confirmation message per page.
            pages.append(f"Page {i+1} processed.")

        return JSONResponse(content={
            "message": f"PDF successfully split into {num_pages} pages.",
            "pages": pages
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))