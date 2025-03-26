from flask import Flask, request, jsonify
import PyPDF2
import io

app = Flask(__name__)

@app.route('/split', methods=['POST'])
def split_pdf():
    # Ensure a file is provided
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    
    try:
        # Read the PDF file
        pdf_reader = PyPDF2.PdfFileReader(file)
        num_pages = pdf_reader.getNumPages()
        split_pages = []

        for i in range(num_pages):
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.addPage(pdf_reader.getPage(i))
            output = io.BytesIO()
            pdf_writer.write(output)
            output.seek(0)
            # You might save the page to disk or cloud storage here,
            # then return a URL or identifier instead of the raw bytes.
            split_pages.append(f"Page {i+1} processed.")

        return jsonify({
            "message": f"PDF successfully split into {num_pages} pages.",
            "pages": split_pages
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
