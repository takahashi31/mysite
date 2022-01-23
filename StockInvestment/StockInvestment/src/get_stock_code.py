import time
import json
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
import requests
from bs4 import BeautifulSoup as bs4
from html_table_parser import parser_functions as parser
#import pandas as pd
#import urllib.request
#import os

PATH_DATA = '..\\Data\\KOSPI\\'
TODAY = time.strftime("%Y%m%d")

def load_json_from_file(file_name) :
	try :
		#with open(file_name,'r',encoding="cp949") as make_file: 
		with open(file_name,'r',encoding="UTF8") as make_file: 
		   data=json.load(make_file) 
		make_file.close()
	except  Exception as e :
		data = {}
		print(e, file_name)
	return data

def save_to_file_json(file_name, data) :
	filename = file_name + '_' + TODAY + '.txt'
	with open(filename,'w',encoding="UTF8") as make_file: 
	   json.dump(data, make_file, ensure_ascii=False, indent="\t") 
	make_file.close()

def save_to_file_csv(file_name, data) :
	filename = file_name + '_' + TODAY + '.csv'
	#with open(file_name,'w',encoding="cp949") as make_file: 
	with open(filename,'w',encoding="UTF8") as make_file: 
		# title 저장
		vals = data[0].keys()
		ss = ''
		for val in vals:
			val = val.replace(',','')
			ss += (val + ',')
		ss += '\n'
		make_file.write(ss)

		for dt in data:
			vals = dt.values()
			ss = ''
			for val in vals:
				val = val.replace(',','')
				ss += (val + ',')
			ss += '\n'
			make_file.write(ss)
	make_file.close()

#print( os.getcwd() )

driver = webdriver.Chrome()
driver.get("http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101")
#driver.get("http://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd")

print(driver.title)								# Title
print(driver.current_url)						# URL

time.sleep(5)

try:
	# 종목정보 클릭
	driver.find_element(By.XPATH, '//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[2]/a').click()
	#driver.implicitly_wait(15)
	time.sleep(3)
except  Exception as e :
	print(e, "not searched find_element(종목정보)")

try:
	# 전종목 기본정보 클릭
	driver.find_element(By.XPATH, '//*[@id="jsMdiMenu"]/div[4]/ul/li[1]/ul/li[2]/div/div[1]/ul/li[2]/ul/li[2]/ul/li[1]/a').click()
	#driver.implicitly_wait(15)
	time.sleep(10)
	#driver.find_element(By.XPATH, '//*[@id="mktId_1_1"]').click()
	#driver.find_element(By.XPATH, '//*[@id="jsSearchButton"]').click()
	#time.sleep(5)
except  Exception as e :
	print(e, "not searched find_element(전종목 기본정보)")

#fname = 'trading_halt'
#url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101'
#warning_stocks(fname, url)

# テーブル内容取得
try:
	#해당 연도 항공통계 데이터 불러오기
	#html = driver.find_element_by_xpath('//*[@id="jsMdiContent"]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/table')
	#html = driver.find_element(By.XPATH, '//*[@id="jsMdiContent"]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/table')
	page = driver.page_source
	#f = open('..\\Data\\KOSPI\\page_종목코드.txt', 'w', encoding='UTF-8')
	#f.write(page)
	#f.close()
	#soup = bs4(page, 'lxml')
	soup = bs4(page, 'html.parser')
	#f = open('..\\Data\\KOSPI\\soup.txt', 'w', encoding='UTF-8')
	#f.write(soup.prettify())
	#f.close()
	table = soup.find_all('table')
	#table = soup.find('table',{'class':'CI-GRID-BODY-TABLE'})
	#print(table)
	p = parser.make2d(table[6])
	#print(p)
	#data = pd.DataFrame(p[2:],columns=p[0])

	fname = 'codelist'
	save_to_file_json(fname, p)

	save_to_file_csv(fname, p)
except  Exception as e :
	print(traceback.format_exc(), "\nnot recorgnaized table(종목코드)")

# テーブル内容取得
#try:
#	#해당 연도 항공통계 데이터 불러오기
#	page = driver.page_source
#	soup = BeautifulSoup(page, 'html.parser')
#	#temp = soup.find_all('table')
#	#p=parser.make2d(temp[1])
#	#data=pd.DataFrame(p[2:],columns=p[0])
#	##각 데이터 합치기
#	#df = pd.concat([df,data])
#	cnt = 0
#	th_list = []
#	td_list = []
#	got_title = 0
#	for tr in soup.find_all('tr') :
#		if got_title == 0 :
#			th = tr.find_all('th')
#			if th != [] :
#				if th[1].text.strip() == '표준코드' :
#					for i in range(0,len(th)) :
#						data = th[i].text.strip()
#						data = data.replace('\n','')
#						if data == '' :
#							data = '-'
#						th_list.append(data)
#						print(i, data )
#					print('')
#					got_title = 1
#
#		td = tr.find_all('td')
#		try : 
#			#if int(td[0].text.strip()) == cnt :
#			info = {}
#			line = ""
#			for i in range(0,len(td)) :
#				data = td[i].text.strip()
#				data = data.replace('\n','')
#				if data == '' :
#					data = '-'
#				info[th_list[i]] = data
#				if i < len(td) :
#					line += "%s\t" % (data)
#				else:
#					line += "%s" % (data)
#			print(line)
#			td_list.append(info)
#			cnt+=1
#		except :
#			print('fail to read td')
#			continue
#    #
#	##tableElement = driver.find_element_by_class_name("CI-GRID-BODY-TABLE")
#	#tableElement = driver.find_element(By.XPATH, '//*[@id="jsMdiContent"]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/table')
#	#tr_list = tableElement.find_elements(By.TAG_NAME, "tr")
#	##print("tr_list lens=[" + len(tr_list) + "]")
#	#print(tr_list)
#    #
#	#got_title = 0
#	#cnt = 0
#	#th_list = []
#	#prices = []
#	## ヘッダ行は除いて取得
#	#for i in range(1,len(tr_list)):
#	#	if got_title == 0 :
#	#		# 헤더(첫번째 레코드)의 경우
#	#		th_list= tr_list[i].find_elements(By.TAG_NAME, "th")
#	#		#print("th_list lens=[" + len(th_list) + "]")
#	#		#if th_list != [] :
#	#		# 헤더가 존재하는 경우
#	#		#if th_list[1].text.strip() == '표준코드' :
#	#		# 헤더의 첫 항목이 '표준코드'인 경우
#	#		info = {}
#	#		for i in range(0,len(th_list)) :
#	#			data = th_list[i].text.strip()
#	#			if data == '' :
#	#				data = 'N'
#	#			data = data.replace('\n','')
#	#			#th_list.append(data)
#	#			print(i, data )
#	#		print('')
#	#		#got_title = 1
#	#		#else :
#	#		#	# 헤더의 첫 항목이 '표준코드'가 아닌 경우
#	#		#	print('is not 표준코드')
#	#		#else :
#	#		#	# 헤더가 존재하지않는 경우
#	#		#	print('fail to get header')
#
#	#	tds = tr_list[i].find_elements(By.TAG_NAME, "td")
#	#	print("td lens=[" + len(tds) + "]")
#	#	info = {}
#	#	for j in range(0,len(tds)):
#	#		data = tds[i].text.strip()
#	#		data = data.replace('\n','')
#	#		info[th_list[i]] = data
#	#		if j < len(tds):
#	#			line += "%s\t" % (tds[j].text)
#	#		else:
#	#			line += "%s" % (tds[j].text)
#	#	print(line)
#except  Exception as e :
#	print(e, "not recorgnaized table(주식종목)")
#	#print traceback.format_exc()
#finally:
#	if driver is not None:
#		driver.quit()

#time.sleep(240)
# 현재의 브라우저만 닫기
driver.close()

# 모든 브라우저 닫기
#driver.quit()

print("end")
