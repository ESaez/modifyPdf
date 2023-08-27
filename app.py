from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from modify_pdf import modify_pdf
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        pdf_file = request.files['pdf']
        xlsx_file = request.files['xlsx']
        pdf_filename = secure_filename(pdf_file.filename)
        xlsx_filename = secure_filename(xlsx_file.filename)
        pdf_file.save(os.path.join(app.root_path, pdf_filename))
        xlsx_file.save(os.path.join(app.root_path, xlsx_filename))
        modify_pdf(pdf_filename, xlsx_filename, app)
        return redirect(url_for('upload_file'))
    return '''
    <!doctype html>
    <title>Upload PDF and XLSX</title>
    <h1>Upload PDF and XLSX</h1>
    <form method=post enctype=multipart/form-data>
      <h4>Seleccionar PDF</h4>
      <input type=file name=pdf>
      <br>
      <h4>Seleccionar Excel</h4>
      <input type=file name=xlsx>
      <br>
      <br>
      <input type=submit value='Generar PDF'>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
