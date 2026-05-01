import os
import io
import uuid
from flask import Flask, render_template, request, send_file, redirect, url_for, session
from PIL import Image
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "aether_quantum_core_77" # Required for session management

# Security: Protect cheap hosting from crashes[cite: 2]
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 

# In-memory storage for converted files (Production note: use Redis for high traffic)[cite: 2]
temp_storage = {}

SEO_CONFIG = {
    'png-to-jpg': {'title': 'Convert PNG to JPG Online | Aether', 'h1': 'PNG to JPG'},
    'pdf-to-docx': {'title': 'Convert PDF to Word | Aether', 'h1': 'PDF to Word'},
    'txt-to-pdf': {'title': 'Convert Text to PDF | Aether', 'h1': 'Text to PDF'}
}

@app.errorhandler(413)
def file_too_large(error):
    return "File exceeds 10MB limit. Aether core stability requires smaller matter.", 413

@app.route('/')
@app.route('/convert/<tool_id>')
def index(tool_id=None):
    seo_data = SEO_CONFIG.get(tool_id, {
        'title': 'AETHER | Shift Digital State Instantly',
        'h1': 'Shift Digital State Instantly'
    })
    return render_template('index.html', seo=seo_data)

@app.route('/success')
def success():
    # Only allow access if a file was actually converted[cite: 2]
    if 'download_id' not in session:
        return redirect(url_for('index'))
    return render_template('success.html')

@app.route('/transcode', methods=['POST'])
def transcode():
    file = request.files.get('file')
    if not file: return redirect(url_for('index'))

    target_format = request.form.get('format', 'JPEG').upper()
    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    
    out_io = io.BytesIO()
    mime_type = ""
    
    try:
        # --- ENGINE 1: VISUAL (Images)[cite: 2] ---
        if ext in ['jpg', 'jpeg', 'png', 'webp']:
            img = Image.open(file)
            if img.mode in ("RGBA", "P") and target_format == "JPEG":
                img = img.convert("RGB")
            img.save(out_io, format=target_format)
            mime_type = f'image/{target_format.lower()}'

        # --- ENGINE 2: TEXTUAL (Text to PDF)[cite: 2] ---
        elif ext == 'txt' and target_format == 'PDF':
            text_content = file.read().decode('utf-8', errors='ignore')
            p = canvas.Canvas(out_io)
            t = p.beginText(50, 750)
            t.setFont("Helvetica-Bold", 14)
            t.textLine("AETHER TRANSCODING REPORT")
            t.setFont("Helvetica", 10)
            t.moveCursor(0, 20)
            for line in text_content.splitlines()[:100]:
                t.textLine(line)
            p.drawText(t)
            p.showPage()
            p.save()
            mime_type = 'application/pdf'

        else:
            return "Unsupported conversion pair", 400

        # --- STATE MANAGEMENT[cite: 2] ---
        file_id = str(uuid.uuid4())
        out_io.seek(0)
        temp_storage[file_id] = {
            'data': out_io.read(),
            'name': f"aether_export_{file_id[:6]}.{target_format.lower()}",
            'mime': mime_type
        }
        
        session['download_id'] = file_id
        return redirect(url_for('success')) # Redirect to capture Ad revenue

    except Exception as e:
        print(f"Server Error: {e}")
        return "Internal Engine Error", 500

@app.route('/download_file')
def download_file():
    file_id = session.get('download_id')
    if file_id in temp_storage:
        f = temp_storage[file_id]
        return send_file(
            io.BytesIO(f['data']),
            mimetype=f['mime'],
            as_attachment=True,
            download_name=f['name']
        )
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

if __name__ == '__main__':
    app.run(debug=True)