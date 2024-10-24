from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ChromeDriverManager를 사용하여 ChromeDriver 설치 및 실행
service = Service('C:/Users/guryo/.wdm/drivers/chromedriver/win64/130.0.6723.69/chromedriver-win32/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# 웹 페이지 접속
driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')

driver.find_element(By.ID, 'srchDvNm01').send_keys('') # 회원번호
driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys("") # 비밀번호

driver.find_element(By.XPATH, '//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()
driver.implicitly_wait(5)

driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
driver.implicitly_wait(5)

# 출발지 입력
dep_stn = driver.find_element(By.ID, 'dptRsStnCdNm')
dep_stn.clear() 
dep_stn.send_keys("오송")

# 도착지 입력
arr_stn = driver.find_element(By.ID, 'arvRsStnCdNm')
arr_stn.clear()
arr_stn.send_keys("수서")

# 출발 날짜
elm_dptDt = driver.find_element(By.ID, "dptDt")
driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptDt)
Select(driver.find_element(By.ID,"dptDt")).select_by_value("20241031")

# 출발 시간
elm_dptTm = driver.find_element(By.ID, "dptTm")
driver.execute_script("arguments[0].setAttribute('style','display: True;')", elm_dptTm)
Select(driver.find_element(By.ID, "dptTm")).select_by_visible_text("12")

# 조회하기 버튼 클릭
driver.find_element(By.XPATH,"//input[@value='조회하기']").click()
driver.implicitly_wait(5)

# 조회 결과 테이블이 나타날 때까지 기다리기 (최대 30초 대기)
wait = WebDriverWait(driver, 30)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child(1)")))

reserved = False

while True:
    for i in range(1, 5):
        standard_seat = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7)").text

        if "예약하기" in standard_seat:
            print("예약 가능")          
            driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div/div[3]/div[1]/form/fieldset/div[6]/table/tbody/tr[{i}]/td[7]/a/span").click()
            reserved = True
            break

    if not reserved:
        # 5초 기다리기
        time.sleep(5)
        
        # 다시 조회하기
        submit = driver.find_element(By.XPATH, "//input[@value='조회하기']")
        driver.execute_script("arguments[0].click();", submit)
        print("새로고침")

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child(1)")))

    else:
        break

input("브라우저를 닫으려면 엔터를 누르세요...")
