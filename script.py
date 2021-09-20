import os
import errno
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyperclip
import sys
print()
print()
print("************************************************************************")
print("************************************************************************")
print("*******                                                          *******")
print("*******            Welcome to Codeforces Downloader              *******")
print("*******                                                          *******")
print("************************************************************************")
print("************************************************************************")
print()
print()
# Input user's root path
root_path = os.getcwd()

# create directories
print("\nCreating directory required to store files........\n")

code = os.path.join(root_path, "codes")
accepted_file = "accepted_code_link.txt"

try:
    os.makedirs(code)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

with open(os.path.join(root_path, accepted_file), 'w') as f:
    pass

print('\nCreated directory named as "codes"\n')

f = open("accepted_code_link.txt","w")
f.write("")
f.close()


# get UserID
userid = ''
print("\nEnter User name:", end=" ")
userid = input().strip().lower()
print("\n Enter extension for the files(.cpp/.c/.txt/.java/.py/........)      :",end = " ")
ext = input().strip().lower()
# start Browser
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
chromedriver = "chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriver, options=chromeOptions)
desiredUrl = 'https://codeforces.com/submissions/'+userid
driver.get(desiredUrl)
currentUrl = driver.current_url
# loop if incorrect username
if(desiredUrl != currentUrl):
    turns = 0
    while(turns < 4 and currentUrl != desiredUrl):
        print('\nINCORRECT USER-ID\tAttempts left: '+str(4-turns))
        print("\nEnter User name:", end=" ")
        userid = input().strip().lower()
        desiredUrl = 'https://codeforces.com/submissions/'+userid
        driver.get(desiredUrl)
        currentUrl = driver.current_url
        turns += 1
        if(turns==4):
            print("TOO MANY INCORRECT ATTEMPTS!\nEXITING............")
            sys.exit()

print("\nGetting links of accepted submissions...............\n")            
while(True):
    tbody = driver.find_element_by_class_name("status-frame-datatable").find_element(By.TAG_NAME, "tbody")
    all_tr = tbody.find_elements(By.TAG_NAME, "tr")
    f = open("accepted_code_link.txt","a")
    for rows in all_tr:
        try:
            row_val = rows.find_elements(By.TAG_NAME,"td")
            if(len(row_val)==0):
                continue
            submissionid = row_val[0].find_element(By.TAG_NAME,'a').get_attribute('submissionid')
            contestid = row_val[3].find_element(By.TAG_NAME,'a').get_attribute('href').split("/")[-3]
            status = row_val[5].find_element(By.TAG_NAME,"span").get_attribute('submissionverdict')
            # print(status)
            val = 'https://www.codeforces.com/contest/'+contestid+'/submission/'+submissionid
            # print(val)
            if(status=="OK"):
                f.writelines(val)
                f.writelines("\n")
            # print(val)
        except Exception as e:
            # print("Bad link")
            continue    
    f.close()
    try:
        driver.find_element_by_link_text('→').click()
        time.sleep(2)
    except Exception as e:
        print("Next Page unavailable\n")
        break

print("\nLinks for websites loaded\n\nProceeding to download files................\n")

links = open("accepted_code_link.txt",'r')
for x in links:
    try:
        driver.get(x)
        time.sleep(2)
        driver.find_element_by_class_name('source-copier').click()
        wholeCode = pyperclip.paste()
        wholeCode = wholeCode.replace("\r","")
        tableew = driver.find_element_by_tag_name("table")
        tbody = tableew.find_element(By.TAG_NAME,"tbody")
        rows = tbody.find_elements(By.TAG_NAME,"tr")[1]
        datas = rows.find_elements(By.TAG_NAME,"td")[2].find_element(By.TAG_NAME,'a')
        problemid = datas.get_attribute('href')
        problemid = problemid.split('/')[-3]+problemid.split('/')[-1]+ext
        f = open('codes/'+problemid,'w')
        f.write(wholeCode)
        f.close()

    except Exception as e:
        print(e)
        continue

print("TASK COMPLETED!!!!!!!!!\nPlease Star the repo if you liked")   
driver.quit()
