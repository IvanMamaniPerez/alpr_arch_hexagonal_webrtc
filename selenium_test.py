from selenium import webdriver
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
    driver.get("https://www.netflix.com/login")

    # Rellenar el formulario de inicio de sesión
    email_input = driver.find_element(By.NAME, "userLoginId")
    email_input.send_keys("mamaniperezivan@gmail.com")
    
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("ReG.OnlyF4m1l74")
    
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Esperar a que la navegación se complete
    time.sleep(5)  # Espera explícita

    # Navegar a un contenido específico
    driver.get("https://www.netflix.com/watch/80057281")

    # Esperar a que el video cargue
    time.sleep(5)

    # Obtener el enlace de video
    video_element = driver.find_element(By.TAG_NAME, "video")
    video_url = video_element.get_attribute("src")

    print(video_url)

finally:
    driver.quit()
