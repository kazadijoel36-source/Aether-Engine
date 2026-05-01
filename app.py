import os
from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfWriter
from PIL import Image
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'temp_uploads'

# Ensure the temp folder exists for processing
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

# ================= MAIN TRANSMUTATION ENGINE =================
@app.route('/convert', methods=['POST'])
def convert():
    # 1. Check for files
    if 'file' not in request.files:
        return "No file matter detected.", 400
    
    file = request.files.get('file')
    # Use getlist if you are supporting the Merge feature specifically
    files = request.files.getlist('file') 
    
    conversion_type = request.form.get('conversion_type')

    if not file or file.filename == '':
        return "Matter is empty. Please load a file.", 400

    try:
        # --- PDF TO IMAGE (.png) ---
        if conversion_type == "pdf_to_img":
            # Note: This requires 'pdf2image' library
            return "PDF to Image engine coming soon!", 501

        # --- MERGE PDF ---
        elif conversion_type == "merge_pdf":
            merger = PdfWriter()
            for f in files:
                if f.filename.endswith('.pdf'):
                    merger.append(f)
            
            output = io.BytesIO()
            merger.write(output)
            merger.close()
            output.seek(0)
            return send_file(output, as_attachment=True, download_name="merged_tactical.pdf")

        # --- PNG TO JPG ---
        elif conversion_type == "png_to_jpg":
            img = Image.open(file)
            rgb_img = img.convert('RGB')
            output = io.BytesIO()
            rgb_img.save(output, format='JPEG', quality=90)
            output.seek(0)
            return send_file(output, as_attachment=True, download_name="converted.jpg")

        # --- JPG TO PNG ---
        elif conversion_type == "jpg_to_png":
            img = Image.open(file)
            output = io.BytesIO()
            img.save(output, format='PNG')
            output.seek(0)
            return send_file(output, as_attachment=True, download_name="converted.png")

        # --- COMPRESS IMAGE ---
        elif conversion_type == "compress_img":
            img = Image.open(file)
            output = io.BytesIO()
            img.save(output, format=img.format, quality=30)
            output.seek(0)
            return send_file(output, as_attachment=True, download_name="compressed_file" + os.path.splitext(file.filename)[1])

        else:
            return "Target state unknown. Re-align transmutation parameters.", 400

    except Exception as e:
        return f"Transmutation Error: {str(e)}", 500

# =============================================================

if __name__ == '__main__':
    # Set to False when deploying to Railway
    app.run(debug=True, port=5000)