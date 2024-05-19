from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Indiquer le chemin vers chromedriver
driver_path = "/opt/homebrew/bin/chromedriver"
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Ouvrir une page web pour tester
driver.get("https://www.google.com")

# Vérifier que le titre de la page est bien "Google"
print(driver.title)

# Fermer le navigateur
driver.quit()
