""" from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuración del WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Navegar a la página de inicio de sesión de Netflix
    driver.get("https://sso.crunchyroll.com/es/login")

    # Rellenar el formulario de inicio de sesión
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys("neudyselene08@gmail.com")
    
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("1q2w3e4r5t")
    
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Esperar a que la navegación se complete
    time.sleep(50)  # Espera explícita

    # Navegar a un contenido específico
    # driver.get("https://www.crunchyroll.com/es/watch/G67521GNR/naruto-enters-the-battle")

    # Esperar a que el video cargue
    time.sleep(5)

    # Obtener el enlace de video
    # video_element = driver.find_element(By.TAG_NAME, "iframe")
    # video_url = video_element.get_attribute("src")

    # print(video_url)
    # time.sleep(235)
finally:
    driver.quit() """


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuración de opciones de Chrome
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
options.add_argument("accept-encoding=gzip, deflate, br")
options.add_argument("accept-language=en-US,en;q=0.9")
options.add_argument("upgrade-insecure-requests=1")
# options.add_argument("user-data-dir=path_to_your_chrome_profile")
# options.add_argument('--proxy-server=http://your_residential_proxy:your_port') # Si usas un proxy

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Navegar a la página de inicio de sesión
    driver.get("https://sso.crunchyroll.com/es/login")

    # Rellenar el formulario de inicio de sesión
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys("neudyselene08@gmail.com")
    
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("1q2w3e4r5t")
    
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Esperar a que la navegación se complete
    time.sleep(5)  # Pausa de 5 segundos entre acciones

    # Navegar a un contenido específico
    driver.get("https://www.crunchyroll.com/es/watch/G67521GNR/naruto-enters-the-battle")

    # Esperar a que el video cargue
    time.sleep(5)

    # Obtener el enlace de video
    video_element = driver.find_element(By.TAG_NAME, "video")
    video_url = video_element.get_attribute("src")

    print(video_url)

finally:
    driver.quit()
