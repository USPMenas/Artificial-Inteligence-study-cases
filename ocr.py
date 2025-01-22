import pytesseract
import pdfplumber
import pandas as pd
from PIL import Image
import os

# Encontra o idioma que estamos analisando
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/tessdata'


# Configure o caminho para o Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Função para extrair texto do PDF usando pdfplumber e OCR
def extract_data_from_pdf(pdf_path):
    data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            # Extração do texto estruturado
            text = page.extract_text()
            
            # Captura das imagens para OCR
            image = page.to_image()
            image_path = f"temp_page_{page_number}.png"
            image.save(image_path)
            
            # Aplicação do OCR para textos manuscritos
            ocr_text = pytesseract.image_to_string(Image.open(image_path), lang='por')
            os.remove(image_path)  # Remova a imagem temporária
            
            # Combine os resultados
            data.append({'page_number': page_number, 'text': text, 'ocr_text': ocr_text})
    
    return data

# Função para salvar os dados em um arquivo Excel
def save_to_excel(data, output_path):
    rows = []
    for item in data:
        rows.append({'Página': item['page_number'], 'Texto': item['text'], 'Texto OCR': item['ocr_text']})
    
    df = pd.DataFrame(rows)
    df.to_excel(output_path, index=False)
    print(f"Dados salvos em {output_path}")

# Caminho do PDF de entrada e saída do Excel
input_pdf = "teste1.pdf"
output_excel = "resultado_formulario.xlsx"

# Extração e salvamento dos dados
data_extracted = extract_data_from_pdf(input_pdf)
save_to_excel(data_extracted, output_excel)
