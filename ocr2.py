import cv2
import pytesseract
import pdfplumber
import pandas as pd
from PIL import Image
import os

# Configure o caminho para o Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/tessdata'

# Função para pré-processar imagens (melhorar a detecção de manuscritos)
def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    return binary

# Função para extrair texto usando OCR
def extract_handwritten_text(image_path):
    preprocessed_image = preprocess_image(image_path)
    # Salve a imagem pré-processada temporariamente
    temp_path = 'temp_preprocessed.png'
    cv2.imwrite(temp_path, preprocessed_image)
    text = pytesseract.image_to_string(temp_path, lang='por', config='--psm 6')
    os.remove(temp_path)
    return text

# Função principal para extrair texto do PDF e aplicar OCR
def extract_data_from_pdf(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            # Extração do texto estruturado
            text = page.extract_text()

            # Salvar a imagem da página e aplicar OCR
            image_path = f'temp_page_{page_number}.png'
            page.to_image().save(image_path)
            ocr_text = extract_handwritten_text(image_path)
            os.remove(image_path)

            # Combine os resultados
            data.append({'page_number': page_number, 'text': text, 'ocr_text': ocr_text})
    return data

# Salvar os resultados em Excel
def save_to_excel(data, output_path):
    rows = []
    for item in data:
        rows.append({'Página': item['page_number'], 'Texto Estruturado': item['text'], 'Texto Manuscrito': item['ocr_text']})
    df = pd.DataFrame(rows)
    df.to_excel(output_path, index=False)
    print(f'Dados salvos em {output_path}')

# Caminho do PDF de entrada e saída do Excel
input_pdf = "teste1.pdf"
output_excel = "resultado_formulario_atualizado.xlsx"

# Extração e salvamento dos dados
data_extracted = extract_data_from_pdf(input_pdf)
save_to_excel(data_extracted, output_excel)
