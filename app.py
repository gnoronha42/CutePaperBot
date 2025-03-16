from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests
import json
import random

# Selenium Configuration
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Function to save cookies
def save_cookies(driver, path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    pickle.dump(driver.get_cookies(), open(path, "wb"))
    print("Cookies saved successfully!")

# Function to load cookies
def load_cookies(driver, path):
    if os.path.exists(path):
        try:
            cookies = pickle.load(open(path, "rb"))
            if cookies is None:
                print("Cookie file exists but is empty or invalid.")
                return False
                
            for cookie in cookies:
                # Some cookies might have the 'expiry' attribute as float
                if 'expiry' in cookie:
                    cookie['expiry'] = int(cookie['expiry'])
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Error adding cookie: {e}")
            print("Cookies loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading cookies: {e}")
            return False
    return False

# Path to store cookies
cookies_path = "cookies/bagy_session.pkl"

# Bagy website URL
driver.get("https://contas.bagypro.com/admin/login?utm_source=institucional&utm_medium=perpetuo&utm_campaign={institucional}{home}&utm_content=tof&_gl=1*o89vde*_gcl_aw*R0NMLjE3NDE4MTAwMjUuRUFJYUlRb2JDaE1JdFlINV9LdUZqQU1WOHBYdUFSMWVQd1FyRUFBWUFTQUFFZ0x2a2ZEX0J3RQ..*_gcl_au*Njk0NTg5MzU4LjE3NDE4MTAwMDc.*_ga*MTk1MjgzMTEwNi4xNzQxODEwMDA3*_ga_Z403XZM91F*MTc0MTgxMDAwNy4xLjEuMTc0MTgxMDAyNS4wLjAuMTg1Mjk0MjQyNQ..*_fplc*bmdnd2VIQU9FaENVZzRPVU95dWhvblNVY2Z2N3VGcDJOSmMwQ3FiJTJCakFEcExITTFLS2c0c1NkOGVRczA0WHRGZTdUd1ZMNE4yOGFhSVMlMkZRbHR5elBIUEYzUiUyRm4lMkIyQ3Q5QjVpM3JUOEdQYVRjbyUyRmQ5VkxBaiUyRkslMkZITXZVN3clM0QlM0Q.*_ga_DSP36C3EJ6*MTc0MTgxMDAxMC4xLjAuMTc0MTgxMDAxMC4wLjAuMTU1MzIxNDUw")
time.sleep(3)

# Check if there are saved cookies
login_required = True
if os.path.exists(cookies_path):
    # First access the main domain
    driver.get("https://contas.bagypro.com")
    time.sleep(1)
    
    # Try to load cookies
    load_cookies(driver, cookies_path)
    time.sleep(2)
    
    # Redirect to post-login page to verify if session is active
    driver.get("https://flor-de-maria-papelaria.bagypro.com/admin/produtos")
    time.sleep(5)
    
    # Check if login was successful (checking if we're not on login page)
    if "login" not in driver.current_url:
        login_required = False
        print("Session restored successfully!")

# If login is needed
if login_required:
    print("Performing new login...")
    driver.get("https://contas.bagypro.com/admin/login?utm_source=institucional&utm_medium=perpetuo&utm_campaign={institucional}{home}&utm_content=tof&_gl=1*o89vde*_gcl_aw*R0NMLjE3NDE4MTAwMjUuRUFJYUlRb2JDaE1JdFlINV9LdUZqQU1WOHBYdUFSMWVQd1FyRUFBWUFTQUFFZ0x2a2ZEX0J3RQ..*_gcl_au*Njk0NTg5MzU4LjE3NDE4MTAwMDc.*_ga*MTk1MjgzMTEwNi4xNzQxODEwMDA3*_ga_Z403XZM91F*MTc0MTgxMDAwNy4xLjEuMTc0MTgxMDAyNS4wLjAuMTg1Mjk0MjQyNQ..*_fplc*bmdnd2VIQU9FaENVZzRPVU95dWhvblNVY2Z2N3VGcDJOSmMwQ3FiJTJCakFEcExITTFLS2c0c1NkOGVRczA0WHRGZTdUd1ZMNE4yOGFhSVMlMkZRbHR5elBIUEYzUiUyRm4lMkIyQ3Q5QjVpM3JUOEdQYVRjbyUyRmQ5VkxBaiUyRkslMkZITXZVN3clM0QlM0Q.*_ga_DSP36C3EJ6*MTc0MTgxMDAxMC4xLjAuMTc0MTgxMDAxMC4wLjAuMTU1MzIxNDUw")
    time.sleep(3)
    
    # Login
    email = driver.find_element(By.NAME, "email")
    email.send_keys("flordemariapapelaria@gmail.com")
    email.send_keys(Keys.RETURN)
    time.sleep(5)
    
    # Security code field
    security_code = driver.find_element(By.NAME, "pincode")
    security_code.send_keys("353900")
    security_code.send_keys(Keys.RETURN)
    time.sleep(5)
    
    # Save cookies after successful login
    save_cookies(driver, cookies_path)

# Read products from CSV file
products = pd.read_csv("estoque.csv")

# Function to click on "Stock and variations" tab
def click_stock_tab(driver):
    try:
        print("Trying to click on stock tab...")
        
        # Wait until "Stock and variations" tab is present and clickable
        stock_tab = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "ui-tab-item") and contains(., "Estoque e variações")]'))
        )
        
        # Scroll to element to ensure it's visible
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", stock_tab)
        time.sleep(1)  # Small pause to ensure scrolling is complete
        
        # Click the element
        driver.execute_script("arguments[0].click();", stock_tab)
        print("Stock tab clicked successfully.")
        
        # Wait for tab to load
        time.sleep(3)  # Adjust time as needed
        
    except TimeoutException:
        print("Error: 'Stock and variations' tab not found or not clickable.")
        driver.save_screenshot("error_stock_tab.png")
        raise Exception("Could not access stock tab after multiple attempts")

# Function to generate description using Ollama
def generate_description_with_ollama(product_name):
    try:
        # Emojis relacionados a papelaria fofa e flores
        emojis = ["🌸", "🌷", "🌹", "🌺", "🌻", "🌼", "🍃", "✨", "📝", "📚", "🖌️", "🎨", "📒", "✏️", "🖋️", "📏", "📐", "🖇️", "📎", "🌈"]
        
        # Prompt mais específico para o modelo de IA
        prompt = f"""
        Crie uma descrição específica e detalhada em português do Brasil para o produto: "{product_name}"

        Regras obrigatórias:
        1. A descrição DEVE ser específica para este produto, mencionando seu nome e características únicas
        2. NUNCA use descrições genéricas
        3. Foque nas características específicas deste tipo de produto

        Por exemplo:
        - Se for um caderno: fale sobre número de folhas, tipo de papel, pauta, capa, encadernação
        - Se for uma caneta: destaque tipo de ponta, cor da tinta, espessura do traço
        - Se for um adesivo: mencione o tema, tamanho, se é à prova d'água
        - Se for um planner: descreva as seções, formato de organização, período
        - Se for um marca-texto: fale sobre a cor, ponta, características especiais
        - Se for um washi tape: destaque o padrão, largura, comprimento
        
        Estrutura obrigatória:
        Parágrafo 1: Apresente o produto específico e sua principal característica
        Parágrafo 2: Detalhe técnico do produto (medidas, materiais, cores, etc)
        Parágrafo 3: Sugestões de uso específicas para este produto

        Exemplo para um marca-texto pastel:
        <p>✨ Marca-texto Pastel Verde Menta - Com ponta dupla chanfrada para traços precisos de 1mm a 4mm!</p>
        <p>🌸 Tinta suave em tom verde menta, perfeita para destacar seus textos sem agredir o papel. Ponta dupla face que permite diferentes espessuras de marcação.</p>
        <p>📝 Ideal para suas anotações de estudo, bullet journal, ou para destacar trechos importantes em seus livros de forma delicada e elegante.</p>

        IMPORTANTE: Adapte a descrição mantendo sempre o foco nas características específicas do produto {product_name}.
        """
        
        # Chamada para a API do Ollama
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            description = result.get("response", "")
            
            # Limpar a descrição
            description = description.replace("```html", "").replace("```", "").strip()
            
            # Se a descrição não tiver emojis, adicionar alguns aleatoriamente
            if not any(emoji in description for emoji in emojis):
                selected_emojis = random.sample(emojis, 3)
                description = f"""
                <p>{selected_emojis[0]} {product_name} - Um produto especial para você!</p>
                <p>{selected_emojis[1]} Feito com todo carinho e qualidade que você merece. Perfeito para tornar seus momentos ainda mais especiais.</p>
                <p>{selected_emojis[2]} Produto exclusivo da Flor de Maria Papelaria - Encantando seu dia!</p>
                """
            
            # Garantir que a descrição esteja em formato HTML
            if "<p>" not in description:
                paragraphs = description.split("\n\n")
                html_description = ""
                for paragraph in paragraphs:
                    if paragraph.strip():
                        html_description += f"<p>{paragraph.strip()}</p>\n"
                description = html_description
            
            print("Descrição gerada com sucesso usando Ollama!")
            return description
        else:
            print(f"Erro na chamada à API do Ollama: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Erro ao gerar descrição com Ollama: {e}")
        # Descrição de fallback em português
        random_emojis = random.sample(emojis, 3)
        return f"""
        <p>{random_emojis[0]} {product_name} - Um produto especial da nossa coleção!</p>
        <p>{random_emojis[1]} Criado com materiais selecionados e acabamento impecável, este item vai encantar você.</p>
        <p>{random_emojis[2]} Ideal para presentear alguém especial ou para deixar seu dia a dia mais organizado e cheio de estilo!</p>
        """

# Process all products from CSV
for index, row in products.iterrows():
    try:
        print(f"\nProcessing product {index+1}/{len(products)}: {row['name']}")
        
        # Navigate to product addition page
        driver.get("https://flor-de-maria-papelaria.bagypro.com/admin/produtos/new")
        time.sleep(5)  # Increased time to ensure page loads completely
        
        # Fill in "Product name" field
        product_name = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[3]/div/div/form/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/input'))
        )
        product_name.send_keys(row["name"])
        time.sleep(2)
        
        # Fill in product description using Ollama
        try:
            print("Generating custom description with Ollama...")
            
            # Generate custom description
            custom_description = generate_description_with_ollama(row["name"])
            
            # Locate rich text editor
            try:
                # Locate rich text editor by provided XPath
                description_editor = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="ui-card-3705"]/div[2]/div[2]/div/div/div[2]'))
                )
                print("Description editor found by specific XPath.")
            except TimeoutException:
                # If specific XPath fails, try locating by class selector
                try:
                    description_editor = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".redactor-styles.redactor-in"))
                    )
                    print("Description editor found by CSS class.")
                except TimeoutException:
                    # Last attempt: look for any editable element within the card
                    description_editor = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "[contenteditable='true']"))
                    )
                    print("Description editor found by contenteditable attribute.")
            
            # Scroll to element to ensure it's visible
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", description_editor)
            time.sleep(1)
            
            # Click editor to activate it
            driver.execute_script("arguments[0].click();", description_editor)
            time.sleep(1)
            
            # Insert description into editor
            driver.execute_script("arguments[0].innerHTML = arguments[1];", description_editor, custom_description)
            print("Custom product description filled successfully.")
            
            # Small pause to ensure content is saved by editor
            time.sleep(2)
            
        except Exception as e:
            print(f"Error filling product description: {e}")
            driver.save_screenshot(f"error_description_product_{index}.png")
            # Continue even if unable to fill description
        
        # Fill in product price field
        try:
            print("Trying to fill in product price...")
            
            # First attempt: using specific XPath provided
            try:
                price_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="__VID__3780"]'))
                )
                print("Price field found by specific XPath.")
            except TimeoutException:
                # Second attempt: look for placeholder or common price field attributes
                try:
                    price_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="0.00" or @inputmode="numeric"]'))
                    )
                    print("Price field found by placeholder or inputmode.")
                except TimeoutException:
                    # Third attempt: look for any field with label containing "Price"
                    price_field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//label[contains(text(), "Preço")]/following::input[1]'))
                    )
                    print("Price field found by label.")
            
            # Scroll to element to ensure it's visible
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", price_field)
            time.sleep(1)
            
            # Clear field and fill with price from spreadsheet
            price_field.click()
            price_field.clear()
            
            # Format price correctly (ensure it's a string with proper format)
            price = str(row["price"]).replace(",", ".")
            price_field.send_keys(price)
            print(f"Product price filled with: {price}")
            
            # Small pause to ensure value is registered
            time.sleep(1)
            
        except Exception as e:
            print(f"Error filling product price: {e}")
            driver.save_screenshot(f"error_price_product_{index}.png")
            # Continue even if unable to fill price
        
        # Navigate to stock and variations tab using function
        try:
            click_stock_tab(driver)
            
            # Now try to locate stock field
            try:
                # First attempt: using specific stock field ID
                stock_field = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.ID, "__VID__1067"))
                )
                print("Stock field found by specific ID.")
            except TimeoutException:
                try:
                    # Second attempt: using XPath
                    stock_field = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="__VID__1067"]'))
                    )
                    print("Stock field found by XPath.")
                except TimeoutException:
                    # Third attempt: using placeholder
                    try:
                        stock_field = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="0" and @type="number"]'))
                        )
                        print("Stock field found by placeholder and type.")
                    except TimeoutException:
                        driver.save_screenshot(f"stock_field_not_found_product_{index}.png")
                        with open(f"html_stock_tab_product_{index}.txt", "w", encoding="utf-8") as f:
                            f.write(driver.page_source)
                        raise Exception("Stock field not found after multiple attempts")
            
            # Fill in stock field
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", stock_field)
            time.sleep(1)
            stock_field.click()
            stock_field.clear()
            stock_field.send_keys(str(row["stock"]))
            print(f"Stock field filled with: {row['stock']}")
            
        except Exception as e:
            print(f"Error interacting with stock tab: {e}")
            driver.save_screenshot(f"error_stock_tab_product_{index}.png")
            with open(f"error_html_product_{index}.txt", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Screenshot and HTML saved for debug")
            continue  # Skip to next product in case of error
        
        # Continue with product saving
        try:
            save_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="form-register"]/div[1]/div/div[2]/button[2]'))
            )
            save_button.click()
            print(f"Product {index+1}/{len(products)}: {row['name']} saved successfully!")
            
            # Wait for save confirmation (could be a toast or redirect)
            time.sleep(5)
            
            # Check if we're still in session (every 5 products, to ensure)
            if index % 5 == 0:
                # Save cookies again to keep session updated
                save_cookies(driver, cookies_path)
                print("Session cookies updated.")
                
        except Exception as e:
            print(f"Error saving product {index+1}/{len(products)}: {row['name']} - {e}")
            driver.save_screenshot(f"error_saving_product_{index}.png")
            continue  # Skip to next product in case of error
            
    except Exception as e:
        print(f"General error processing product {index+1}/{len(products)}: {row['name']} - {e}")
        continue  # Skip to next product in case of error

# Save cookies again at the end of processing
save_cookies(driver, cookies_path)
print("Final session cookies saved.")

print("Product registration completed!")
driver.quit()