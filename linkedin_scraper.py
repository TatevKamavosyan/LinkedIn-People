import random 
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 1. Կարգավորումներ
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Կարդում ենք ընկերությունները
    with open('companies.txt', 'r', encoding='utf-8') as f:
        companies = [line.strip() for line in f if line.strip()]

    # Ստեղծում ենք CSV ֆայլը
    with open('ceos_with_links.csv', mode='w', newline='', encoding='utf-8-sig') as file:
        file.write("sep=,\n")
        writer = csv.writer(file)
        writer.writerow(['Company', 'CEO Full Name', 'Job Title', 'LinkedIn URL'])

        for company in companies:
            print(f"\n🔎 Որոնում եմ {company}-ի CEO-ին...")
            
            query = f"https://www.google.com/search?q=site:linkedin.com/in/+%22{company.replace(' ', '+')}%22+CEO"
            
            # --- ՍԱ ՈՒՂՂՎԱԾ ՄԱՍՆ Է ---
            driver.get(query)
            
            # Սկրիպտը աշխատեցնում ենք ՄԻԱՅՆ էջը բացելուց հետո
            try:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            except:
                pass 
            # -------------------------

            wait_time = random.randint(25, 50) # Ավելի ապահով ժամանակ
            print(f"Սպասում ենք {wait_time} վայրկյան...")
            time.sleep(wait_time)

            try:
                results = driver.find_elements(By.XPATH, "//a[contains(@href, 'linkedin.com/in/')]")
                found = False
                for link in results:
                    try:
                        h3_tag = link.find_elements(By.TAG_NAME, "h3")
                        if not h3_tag: continue
                        
                        full_text = h3_tag[0].text
                        url = link.get_attribute("href")
                        
                        if full_text and url:
                            clean_name = full_text.split('-')[0].split('|')[0].split('·')[0].strip()
                            job_title = "CEO / Executive"
                            if '-' in full_text:
                                parts = full_text.split('-')
                                if len(parts) > 1:
                                    job_title = parts[1].split('|')[0].strip()

                            if "/in/" in url and "google.com" not in url:
                                writer.writerow([company, clean_name, job_title, url])
                                print(f"✅ Գտնվեց: {clean_name}")
                                found = True
                                break 
                    except:
                        continue
                
                if not found:
                    writer.writerow([company, "Not Found", "N/A", "N/A"])
                    print(f"❌ {company} - Արդյունք չկա")

            except Exception as e:
                print(f"⚠️ Սխալ {company}-ի հետ")
                writer.writerow([company, "Error", "N/A", "N/A"])

    print("\n🎉 ԱՇԽԱՏԱՆՔՆ ԱՎԱՐՏՎԵՑ:")

finally:
    driver.quit()