import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

#print( os.getcwd() )

driver = webdriver.Chrome()
driver.get("http://freesis.kofia.or.kr/")
#driver.get("https://www.naver.com/")

print(driver.title)								# Title
print(driver.current_url)						# URL

time.sleep(5)

#driver.find_element_by_xpath("//*[@id='NM_FAVORITE']/div[1]/ul[1]/li[3]/a").click()

#try:
#	driver.switchTo().frame("main");
#except:
#       print("cannot switchTo(main)")

# 주식탭 클릭
try:
	#driver.find_element(By.XPATH, '//*[@id="rank"]/tbody/tr[2]/td[1]').text
	#driver.find_element(By.XPATH, '//*[@id="skipnavigation"]/ul/li[1]/a').text
	driver.find_element(By.XPATH, "//frameset//frame[@name='main']//#document//[@id='skipnavigation']/ul/li[1]/a").text
	#driver.find_element_by_xpath("//*[@id='gnb']/div[1]/ul[1]/li[1]/a").click()
	#driver.find_element_by_xpath("//*[@id='TopMenuSub']/ul/li[1]/a").click()
	#driver.find_element_by_xpath("//*[@id='wrap']/[@id='header']/[@id='gnb']/[@id='TopMenuSub']/ul[1]/li[1]/a").click()
	#driver.find_element_by_xpath("//*[@id='header']/h1[1]/a").click()

	time.sleep(5)
except:
        print("not searched find_element(주식탭)")

#time.sleep(60)

# 현재의 브라우저만 닫기
driver.close()

# 모든 브라우저 닫기
#driver.quit()

print("end")
