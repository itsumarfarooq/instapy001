from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import xlsxwriter
# options = Options()
# options.headless = True
driver = webdriver.Chrome()#options=options)
workbook = xlsxwriter.Workbook('E:/inc.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0
file = open("testfile.txt","r")
for url in file.readlines():
    try:
        driver.get(url)
        name=driver.find_element_by_xpath("//article/div/header/h1").text
        print(name)
        desc=driver.find_element_by_xpath("//article/div/header/p").text
        print(desc)
        industry=driver.find_element_by_xpath("//dd[@class='profileCss.singleIndustry']").text
        print(industry)
        year=driver.find_element_by_xpath("//dl[contains(.//dt, 'Founded')]/dd").text
        print(year)
        location=driver.find_element_by_xpath("//dl[contains(.//dt, 'Location:')]/dd").text
        print(location)
        rank=driver.find_element_by_xpath("//dl[contains(.//dt, 'Rank:')]/dd").text
        print(rank)
        worksheet.write(row, col, name)
        worksheet.write(row, col + 1, desc)
        worksheet.write(row, col + 2, industry)
        worksheet.write(row, col + 3, year)
        worksheet.write(row, col + 4, location)
        worksheet.write(row, col + 5, rank[1:])
        row += 1
    except:
        print("Something went wrong")

workbook.close()
