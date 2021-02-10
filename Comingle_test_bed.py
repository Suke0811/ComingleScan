from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import time
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains


# here put the names of the room you want to scan
other = ['p5','Morta']


# url to search
url_comingle = 'https://comingle.csail.mit.edu/m/E4owJXWthR2jGRy2G#ymRHY2ffrmx8B3XfJ'

# set chrome options (max window)
options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")

# this is recuqired to get into rooms. Allow mic and camera access
options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1,     # 1:allow, 2:block
    "profile.default_content_setting_values.media_stream_camera": 1,  # 1:allow, 2:block
   #"profile.default_content_setting_values.geolocation": 1,          # 1:allow, 2:block
   #"profile.default_content_setting_values.notifications": 1         # 1:allow, 2:block
  })

# launch chrome
driver = webdriver.Chrome(options=options)

data=[]
cnt = 0
# file name (UTC)
ct= time.strftime("%m_%d_%H_%M",time.gmtime())
file_name = 'attendance_' + ct + '.xlsx'

# get web page
driver.get(url_comingle)
# sleep for 5s to make sure the page loads
time.sleep(5)

# get all room addresses
url_videos_full = [elem.get_attribute("href") for elem in driver.find_elements_by_xpath('//*[@class="list-group-item list-group-item-action room-info"]')]
room_info = driver.find_elements_by_xpath('//*[@class="list-group-item list-group-item-action room-info"]')
url_videos = []

# find rooms with specified names
for i in range(len(url_videos_full)):
    if any(x in room_info[i].text for x in other):
        url_videos.append(url_videos_full[i])



for url_video in url_videos:

    # get web page
    driver.get(url_video)
    # sleep for 5s to make sure the page loads
    time.sleep(5)
    #switch to video iframe
    iframe = driver.find_elements_by_tag_name("iframe")
    #asking users to select which iframe to scan (there was a problem searching iframes)
    driver.switch_to.frame(iframe[int(input('iframe?'))])

    #find menu to hover mouse
    menu = driver.find_element_by_class_name('button-group-right')
    ActionChains(driver).move_to_element(menu).perform()
    time.sleep(1)
    #find menu for speaker stats
    menu_button = driver.find_element_by_class_name('toolbox-button-wth-dialog')
    ActionChains(driver).click(menu_button).perform()
    time.sleep(1)
    speaker_button = driver.find_element_by_xpath('//*[@aria-label="Toggle speaker statistics"]')
    ActionChains(driver).click(speaker_button).perform()
    time.sleep(1)

    print('scanning')
    #scan speaker info
    results = driver.find_elements_by_xpath('//*[@class="speaker-stats-item "]')
    results_left = driver.find_elements_by_xpath('//*[@class="speaker-stats-item status-user-left"]')

    print('searching')
    #panda
    #find user name and speak time
    for result in results:
        #scan user name and time
        user = result.find_element_by_class_name('speaker-stats-item__name')
        duration = result.find_element_by_class_name('speaker-stats-item__time')

        if user.text.find('me') != -1:
            continue

        data.append({"room#": cnt, "user": user.text, "duration": duration.text})

    for result in results_left:
        #scan user name and time
        # this is inactive (left users) info.
        user = result.find_element_by_class_name('speaker-stats-item__name')
        duration = result.find_element_by_class_name('speaker-stats-item__time')

        if user.text.find('me') != -1:
            continue
            # exclude me.

        data.append({"room#": cnt, "user": user.text, "duration": duration.text})


    df = pd.DataFrame(data)
    df.to_excel(file_name)
    print('saved')
    print(cnt)
    cnt = cnt + 1



#close chrome
driver.quit()

