from selenium import webdriver
import time

# Username and Pass to sign in to gmail.
print("Do not use with a gmail account that has two step verification.")
user = str(input("Enter gmail account:\n"))
passw = str(input("Enter Password:\n"))

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
time.sleep(6)

driver.get("https://data-sense.herokuapp.com/")

mkTeam = driver.find_element_by_id("form-team")

# Stop driver
driver.close()