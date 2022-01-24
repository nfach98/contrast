import time
from urllib.request import urlretrieve

from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://www.footballkitarchive.com/")

navs = driver.find_element_by_class_name("navigation-section")
leagues = navs.find_elements_by_tag_name("a")

for league in leagues:
    time.sleep(2)
    league_name = league.find_element_by_tag_name("span").text
    if league_name != "Champions League" and league_name != "Europa League":
        link = league.get_attribute("href")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)

        load_more = driver.find_elements_by_class_name("load-more")
        driver.execute_script("window.scrollTo(0, " + str(load_more[-1].location['y']) + ");")
        load_more[-1].click()

        time.sleep(5)

        container_season = driver.find_elements_by_class_name("kit-container")
        for season in container_season:
            links = season.find_elements_by_tag_name("a")
            driver.execute_script("window.scrollTo(0, " + str(season.location['y']) + ");")

            time.sleep(3)
            link_season = links[-1].get_attribute("href")
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[2])
            driver.get(link_season)

            teams = driver.find_elements_by_class_name("kit-container")

            for team in teams:
                kits = team.find_elements_by_class_name("kit")
                driver.execute_script("window.scrollTo(0, " + str(team.location['y']) + ");")
                time.sleep(3)

                for kit in kits:
                    img = kit.find_element_by_css_selector(".lazyload")
                    name = kit.find_element_by_class_name("kit-teamname")
                    season = kit.find_element_by_class_name("kit-season")
                    src = img.get_attribute('src')
                    urlretrieve(src, "images/" + league_name + " " + name.text + " " + season.text + ".jpg")

            driver.close()
            driver.switch_to.window(driver.window_handles[1])

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # league.send_keys(Keys.CONTROL + 'w')
