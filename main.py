from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

try:
    option = webdriver.ChromeOptions()
    brave_path = "C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe"
    option.binary_location = brave_path
    driver = webdriver.Chrome(chrome_options=option, executable_path="G:/My Drive/Interno/Projetos/Projeto Busca Capes/chromedriver.exe")
    
    # countries = ['brazil','bolivia', 'china', 'egypt']
    countries = ['brazil']
    result = []

    for country in countries:

        print(f'checking costs for {country}...')
        page = f'https://www.lonelyplanet.com/{country}/essential-information'

        driver.get(page)

        try:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Accept Cookies']"))).click()

        finally:
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Money and costs']"))).click()

            currency = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*/text()[.="Currency"]/following::div[@class="jsx-3059088443 dangerHTML leading-relaxed lg:text-lg"]')))
            string_daily_costs = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*/text()[.="Daily Costs"]/following::div[@class="jsx-3059088443 dangerHTML leading-relaxed lg:text-lg"]')))
            daily_costs = string_daily_costs.text.split('\n')
            daily_costs = [y.split(": ") for y in daily_costs]
            list_costs = [{'name':item[0],'value':item[1]} for item in daily_costs]

            result.append({
                    'country': country,
                    'currency': currency.text,
                    'costs': list_costs[0]
                })

            final_df = pd.DataFrame()

            for item in result:
                df = pd.DataFrame(item['costs'])
                df['country'] = item['country']
                df['currency'] = item['currency']
                final_df = pd.concat([final_df, df])
                # final_df.merge(df, how='inner', on='country')

            # # df.to_csv('costs_country.csv')

            # # df = pd.DataFrame(result)
            # print(final_df.head())

    print(result)
    input()

except Exception as e:
    print(e)

finally:
    driver.close()