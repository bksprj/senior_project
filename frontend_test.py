from selenium import webdriver
import time
import urllib.request
import random

word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = urllib.request.urlopen(word_url)
long_txt = response.read().decode()
words = long_txt.splitlines()

upper_words = [word for word in words if word[0].isupper()]
name_words  = [word for word in upper_words if not word.isupper()]
one_name = ' '.join([name_words[random.randint(0, len(name_words))] for i in range(2)])

def rand_name():
   name = ' '.join([name_words[random.randint(0, len(name_words))] for i in range(2)])
   return name

# Start of Test

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

# Going to web app
driver.get("https://data-sense.herokuapp.com/")

# Test Forming a Team
driver.find_element_by_id("form-team").click()
teamname = driver.find_element_by_id("group_name")
name = rand_name()
teamname.send_keys(name)
admin = driver.find_element_by_id("email")
admin.send_keys(user)
driver.find_element_by_id("form-team-btn").click()



# Stop driver
driver.close()