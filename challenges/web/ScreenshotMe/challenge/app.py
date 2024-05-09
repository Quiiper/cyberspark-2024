import io
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, request, send_file, render_template

app = Flask(__name__)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def capture_screenshot(url):
    try:
        driver.get(url)
        screenshot = driver.get_screenshot_as_png()
        return screenshot
    except Exception as e:
        return str(e).encode()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            screenshot = capture_screenshot(url)
            return send_file(io.BytesIO(screenshot), mimetype='image/png', as_attachment=True, download_name='screenshot.png')
        else:
            return "URL is missing in the request"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)
