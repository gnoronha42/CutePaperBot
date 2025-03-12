from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configuração do Selenium
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# URL do site da Bagy
driver.get("https://contas.bagypro.com/admin/login?utm_source=institucional&utm_medium=perpetuo&utm_campaign={institucional}{home}&utm_content=tof&_gl=1*o89vde*_gcl_aw*R0NMLjE3NDE4MTAwMjUuRUFJYUlRb2JDaE1JdFlINV9LdUZqQU1WOHBYdUFSMWVQd1FyRUFBWUFTQUFFZ0x2a2ZEX0J3RQ..*_gcl_au*Njk0NTg5MzU4LjE3NDE4MTAwMDc.*_ga*MTk1MjgzMTEwNi4xNzQxODEwMDA3*_ga_Z403XZM91F*MTc0MTgxMDAwNy4xLjEuMTc0MTgxMDAyNS4wLjAuMTg1Mjk0MjQyNQ..*_fplc*bmdnd2VIQU9FaENVZzRPVU95dWhvblNVY2Z2N3VGcDJOSmMwQ3FiJTJCakFEcExITTFLS2c0c1NkOGVRczA0WHRGZTdUd1ZMNE4yOGFhSVMlMkZRbHR5elBIUEYzUiUyRm4lMkIyQ3Q5QjVpM3JUOEdQYVRjbyUyRmQ5VkxBaiUyRkslMkZITXZVN3clM0QlM0Q.*_ga_DSP36C3EJ6*MTc0MTgxMDAxMC4xLjAuMTc0MTgxMDAxMC4wLjAuMTU1MzIxNDUw")
time.sleep(3)

# Login
email = driver.find_element(By.NAME, "email")
email.send_keys("flordemariapapelaria@gmail.com")
email.send_keys(Keys.RETURN)
time.sleep(5)

# Campo para código de segurança
codigo_seguranca = driver.find_element(By.NAME, "pincode")
codigo_seguranca.send_keys("160218")
codigo_seguranca.send_keys(Keys.RETURN)
time.sleep(5)

# Leitura do arquivo CSV com os produtos
produtos = pd.read_csv("estoque.csv")

# Teste com apenas um produto
if not produtos.empty:
    row = produtos.iloc[0]   

    # Navegar para a página de adição de produtos
    driver.get("https://flor-de-maria-papelaria.bagypro.com/admin/produtos/new")
    time.sleep(3)
    
    # Preencher o campo "Nome do produto"
    nome_produto = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[3]/div/div/form/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/input'))
    )
    nome_produto.send_keys(row["name"])
    
    
    
    # Navegar para a aba de estoques e variações
    try:
        # Verifique se o elemento está presente e visível
        aba_estoque = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ui-tab-1763"]/button[2]/span'))
        )
        # Role até o elemento
        driver.execute_script("arguments[0].scrollIntoView();", aba_estoque)
        # Clique no elemento
        aba_estoque.click()
        print("Aba de estoque clicada com sucesso.")
    except TimeoutException:
        print("Erro: O elemento 'Aba de estoque' não está clicável.")
    except Exception as e:
        print("Erro inesperado:", e)
    time.sleep(2)
    
    campo_estoque = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[3]/div/div/form/div[2]/div[3]/div/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/input'))
    )
    campo_estoque.click()  
    campo_estoque.send_keys(row["stock"])
    
  
    botao_salvar = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="form-register"]/div[1]/div/div[2]/button[2]'))
    )
    botao_salvar.click()
    time.sleep(5)

print("Cadastro de produtos finalizado!")
driver.quit()
