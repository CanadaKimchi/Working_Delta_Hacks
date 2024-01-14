from flask import Flask, render_template
app=Flask(__name__, static_url_path='/static')
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import fitz  # PyMuPDF
import boto3
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

key_id = os.getenv("AWS_KEY_ID")
access_key = os.getenv("AWS_ACCESS_KEY")
GPT_API = os.getenv("TEXT_GEN_API")

# Create a Textract client
textract = boto3.client(
    'textract',
    region_name='us-east-2',
    aws_access_key_id=key_id,
    aws_secret_access_key=access_key
)

client = OpenAI(api_key=GPT_API)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    notes = FileField("Notes PDF", validators=[InputRequired()])
    slides = FileField("Slides PDF", validators=[InputRequired()])
    submit = SubmitField("Upload Files")

def upload_to_aws(file_path):
    with open(file_path, 'rb') as file:
        image_bytes = file.read()
    response = textract.detect_document_text(Document={'Bytes': image_bytes})
    lines = [block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE']
    return '\n'.join(lines)

def convert_pdf_to_images(pdf_file_path, output_folder_path):
    output_image_format = 'PNG'
    output_dpi = 300
    os.makedirs(output_folder_path, exist_ok=True)

    pdf_document = fitz.open(pdf_file_path)
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        image = page.get_pixmap(matrix=fitz.Matrix(output_dpi / 72, output_dpi / 72))
        image_path = os.path.join(output_folder_path, f'page_{page_number + 1}.{output_image_format.lower()}')
        image.save(image_path)
    pdf_document.close()

    print(f'Conversion complete. Images saved in: {output_folder_path}')

def gpt(text_notes, text_slides):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "These are my notes: " + str(text_notes) + "Rewrite and format the notes like html code without <html>: " + str(text_slides)}
        ]
    )

    return completion.choices[0].message.content

def main():
    # Notes PDF
    notes_pdf_file_path = './static/files/notes/notes.pdf'
    notes_image_folder_path = './static/files/notespng'
    convert_pdf_to_images(notes_pdf_file_path, notes_image_folder_path)
    text_notes = upload_to_aws(os.path.join(notes_image_folder_path, 'page_1.png'))

    # Slides PDF
    slides_pdf_file_path = './static/files/slides/slides.pdf'
    slides_image_folder_path = './static/files/slidespng'
    convert_pdf_to_images(slides_pdf_file_path, slides_image_folder_path)
    text_slides = upload_to_aws(os.path.join(slides_image_folder_path, 'page_1.png'))

    # GPT-3 Text Generation
    gpt_result = gpt(text_notes, text_slides)

    print(gpt_result)

    return gpt_result

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()

    if form.validate_on_submit():
        notes_file = form.notes.data
        slides_file = form.slides.data

        if notes_file:
            save_path_notes = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], 'notes','notes.pdf')
            notes_file.save(save_path_notes)
            print(f"Notes PDF has been uploaded to: {save_path_notes}")

        if slides_file:
            save_path_slides = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], 'slides', 'slides.pdf')
            slides_file.save(save_path_slides)
            print(f"Slides PDF has been uploaded to: {save_path_slides}")

        # Run additional code after files have been uploaded
        gpt_result = main()

        return render_template('result.html', gpt_result=gpt_result)

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
