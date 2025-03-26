from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pypdf import PdfReader, PdfWriter
import io
import zipfile

app = FastAPI()

@app.post("/split", summary="Split a PDF into individual pages.", operation_id="splitPdf")
async def split_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are accepted.")

    try:
        # Read the input PDF file
        file_contents = await file.read()
        pdf_reader = PdfReader(io.BytesIO(file_contents))
        num_pages = len(pdf_reader.pages)

        # Create an in-memory ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i in range(num_pages):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(pdf_reader.pages[i])
                pdf_buffer = io.BytesIO()
                pdf_writer.write(pdf_buffer)
                pdf_buffer.seek(0)
                # Define a filename for this PDF page
                filename = f"page_{i+1}.pdf"
                # Add the PDF page to the ZIP file
                zip_file.writestr(filename, pdf_buffer.getvalue())

        zip_buffer.seek(0)
        # Return the ZIP file as a StreamingResponse
        return StreamingResponse(
            zip_buffer,
            media_type="application/x-zip-compressed",
            headers={"Content-Disposition": "attachment; filename=split_pdf.zip"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))