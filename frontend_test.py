from selenium import webdriver
import time
import urllib.request
import random
import os

count = 0

# Start of Test

# Username and Pass to sign in to gmail.

# Do not use with a gmail account that has two step verification!

#user = str(input("Enter gmail account:\n"))
#passw = str(input("Enter Password:\n"))
user = "keegan.husom@gmail.com"
passw = "R3dSkull"

# Picking Search Engine
driver = webdriver.Chrome("/Users/KeeganHusom/Downloads/chromedriver")

# Going to gmail
driver.get("http://gmail.com")

# Sending username
elem = driver.find_element_by_id("identifierId")
elem.send_keys(user)

driver.find_element_by_xpath("//*[@id='identifierNext']/content/span").click()
time.sleep(2)

# Sending Password
elem = driver.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input")
elem.send_keys(passw)
time.sleep(2)

# Push Login
driver.find_element_by_xpath("//*[@id='passwordNext']/content/span").click()
time.sleep(4)

# Going to web app
driver.get("https://data-sense.herokuapp.com/")
time.sleep(5)

# Forming a Team
driver.find_element_by_id("form-team").click()
teamname = driver.find_element_by_id("group_name")
time.sleep(2)
num = random.randint(1,10000)
name = "Test Group " + str(num)
teamname.send_keys(name)
time.sleep(2)
admin = driver.find_element_by_id("email")
admin.send_keys(user)
time.sleep(2)
driver.find_element_by_id("form-team-btn").click()

count = count + 1

time.sleep(5)
driver.refresh()
time.sleep(5)


# Add Team Members
driver.find_element_by_id(name).click()
time.sleep(5)
driver.refresh()
time.sleep(5)
driver.find_element_by_id("admin-priv").click()
time.sleep(5)
memberName = driver.find_element_by_id("member_input")
memberName.send_keys("Standard:husoke01@luther.edu")
time.sleep(2)
driver.find_element_by_id("add-mem").click()

count = count + 1

time.sleep(5)
driver.refresh()
time.sleep(5)

# Add file
driver.find_element_by_id("upload_file").click()
time.sleep(2)
driver.find_element_by_id("fileUpload").send_keys(os.getcwd()+"/Senior Project Notes.pdf")
time.sleep(2)
driver.find_element_by_id("enterUp").click()

count = count + 1

time.sleep(5)

# Add task
driver.find_element_by_id("newTask").click()
time.sleep(2)
driver.find_element_by_id("new_task").send_keys("This is a simple task")
time.sleep(2)
driver.find_element_by_id("enterTask").click()

count = count + 1

time.sleep(5)

# Delete file
driver.find_element_by_id("admin-priv").click()
time.sleep(2)
driver.find_element_by_id("file_name_delete").send_keys("Senior_Project_Notes.pdf")
time.sleep(2)
driver.find_element_by_id("dropFile").click()

count = count + 1

time.sleep(5)

# Delete Group
driver.find_element_by_id("admin-priv").click()
time.sleep(2)
deleteteam = driver.find_element_by_id("group_name_delete")
time.sleep(2)
deleteteam.send_keys(name)
driver.find_element_by_id("delete-team").click()

count = count + 1



time.sleep(10)
# Stop driver
driver.close()
result = count / 6
result = result * 100
print("Results from Front End Testing were " + str(result) + "%")