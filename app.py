from flask import Flask, render_template, request
from PIL import Image, ImageEnhance
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ASCII_CHARS = "@%#*+=-:. "  # Контрастные символы для ASCII
WIDTH_SCALE = 2  # Масштаб для компенсации несоответствия высоты и ширины символов

# Функция для изменения размера изображения
def resize_image(image, new_width=100):
    width, height = image.size
    new_height = int((height / width) * new_width / WIDTH_SCALE)
    return image.resize((new_width, new_height))

# Функция для увеличения контрастности изображения
def enhance_contrast(image, factor=1.5):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

# Функция для конвертации пикселей в ASCII-символы
def pixel_to_ascii(pixel):
    gray_value = int(pixel / 255 * (len(ASCII_CHARS) - 1))  # Масштабируем в допустимый диапазон
    return ASCII_CHARS[gray_value]

# Основная функция преобразования изображения в ASCII
def image_to_ascii(image_path, new_width=100):
    try:
        # Открыть изображение
        image = Image.open(image_path).convert("L")  # Преобразуем в градации серого
    except Exception as e:
        print(f"Ошибка при открытии изображения: {e}")
        return

    # Увеличиваем контрастность изображения
    image = enhance_contrast(image)

    # Изменяем размер изображения
    image = resize_image(image, new_width)

    # Преобразуем пиксели в ASCII
    ascii_str = ""
    for y in range(image.height):
        for x in range(image.width):
            gray = image.getpixel((x, y))
            ascii_str += pixel_to_ascii(gray)
        ascii_str += "\n"

    return ascii_str

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        width = int(request.form.get('width', 100))
        ascii_art = image_to_ascii(file_path, width)
        return render_template('result.html', ascii_art=ascii_art.replace("\n", "<br>"))
#444
if __name__ == "__main__":
    app.run(debug=True)
