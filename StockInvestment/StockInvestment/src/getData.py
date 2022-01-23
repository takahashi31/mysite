import win32com.client
import pandas as pd
import time
import datetime

column_dailychart = ['code', 'section', 'date', 'open', 'high', 'low', 'close']

instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
nCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")

row = list(range(len(column_dailychart)))
rows = list()

CPE_MARKET_KIND = {'KOSPI':'U001', 'KOSDAQ':'U201'}

instStockChart.SetInputValue(1, ord('1'))
instStockChart.SetInputValue(2, '20140714')
instStockChart.SetInputValue(3, '20140101')
instStockChart.SetInputValue(5, (0, 2, 3, 4, 5))
instStockChart.SetInputValue(6, ord('D'))
instStockChart.SetInputValue(9, ord('1'))

for key, value in CPE_MARKET_KIND.items():

	remain_request_count = nCpCybos.GetLimitRemainCount(1)
	print(key, value, '남은 요청 : ', remain_request_count)
	
	if remain_request_count == 0:
		print('남은 요청이 모두 소진되었습니다. 잠시 대기합니다.')
		
		while True:
			time.sleep(2)
			remain_request_count = nCpCybos.GetLimitRemainCount(1)
			if remain_request_count > 0:
				print('작업을 재개합니다. (남은 요청 : {0})'.format(remain_request_count))
				break
			print('대기 중...')

	instStockChart.SetInputValue(0, value)
	
	# BlockRequest
	instStockChart.BlockRequest()
	
	# GetHeaderValue
	numData = instStockChart.GetHeaderValue(3)
	numField = instStockChart.GetHeaderValue(1)
	
	# GetDataValue
	for i in range(numData):
		row[0] = value
		row[1] = key # 코스피, 코스닥 여부
		row[2] = instStockChart.GetDataValue(0, i) # 날짜
		row[3] = instStockChart.GetDataValue(1, i) # 시가
		row[4] = instStockChart.GetDataValue(2, i) # 고가
		row[5] = instStockChart.GetDataValue(3, i) # 저가
		row[6] = instStockChart.GetDataValue(4, i) # 종가
		rows.append(list(row))

print('데이터를 모두 불러왔습니다.')
dailychart= pd.DataFrame(data = rows, columns= column_dailychart)
dailychart = dailychart.sort_values(['code','date'])
dailychart.to_csv('dailychart_index.csv', index=False)

print('모든 데이터를 저장하였습니다.')
