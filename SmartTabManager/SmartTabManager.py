from selenium import webdriver
import time
import os
import platform
import http.server
import socketserver
from datetime import datetime, timedelta
import sys

if platform.system() == "Windows":
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
else:
    hosts_path = "/etc/hosts"

redirect_ip = "127.0.0.1"
marker = "# SmartTabManager"

def open_default_tabs(driver):
    websites = ["https://classroom.google.com/",
                "https://www.physicsandmathstutor.com/",
                "https://mail.google.com/mail/u/0/#inbox",
                "https://web.uplearn.co.uk/learn"
                ]
    for website in websites:
        driver.switch_to.new_window("tab")
        driver.get(website)


def open_study_tabs(driver):
    studyMode = ["https://classroom.google.com/",
                 "https://www.physicsandmathstutor.com/",
                 "https://quizlet.com/gb",
                 "https://www.madasmaths.com/",
                 "https://revisionworld.com/",
                 "https://www.alevelphysicsonline.com/",
                 "https://web.uplearn.co.uk/learn",
                 "https://www.aqa.org.uk/",
                 "https://mail.google.com/mail/u/0/#inbox"
                 "https://senecalearning.com/en-GB/"
                 ]
    driver.switch_to.new_window("window")
    newWindow = driver.current_window_handle
    filePath = os.path.abspath("study.html")
    driver.get("file://" + filePath)
    for studywebsite in studyMode:
        driver.switch_to.window(newWindow)
        driver.execute_script(f"window.open('{studywebsite}', '_blank');")

def open_break_tabs(driver):
    breakMode = ["https://www.youtube.com/",
                 "https://makecode.microbit.org/",
                 "https://open.spotify.com/",
                 "https://www.linkedin.com/in/samida-r-b7040b333/"
                 ]
    driver.switch_to.new_window("window")
    newWindow = driver.current_window_handle
    filePath = os.path.abspath("break.html")
    driver.get("file://" + filePath)
    for breakwebsite in breakMode:
        driver.switch_to.window(newWindow)
        driver.execute_script(f"window.open('{breakwebsite}', '_blank');")

def open_chill_tabs(driver):
    chillMode = ["https://www.netflix.com/browse",
                 "https://open.spotify.com/",
                 "https://www.youtube.com/",
                 "https://makecode.microbit.org/",
                 "https://www.amazon.co.uk/gp/video/storefront"
                 ]
    driver.switch_to.new_window("window")
    newWindow = driver.current_window_handle
    filePath = os.path.abspath("chill.html")
    driver.get("file://" + filePath)
    for chillwebsite in chillMode:
        driver.switch_to.window(newWindow)
        driver.execute_script(f"window.open('{chillwebsite}', '_blank');")

def open_mindfulness_tabs(driver):
    mindfulnessMode = ["https://www.freemindfulness.org/download",
                       "https://www.breathworks-mindfulness.org.uk/free-meditations",
                       "https://insighttimer.com/meditation-topics/mindfulness",
                       "https://www.youtube.com/"
                       ]
    driver.switch_to.new_window("window")
    newWindow = driver.current_window_handle
    filePath = os.path.abspath("mindfulness.html")
    driver.get("file://" + filePath)
    for mindfulnesswebsite in mindfulnessMode:
        driver.switch_to.window(newWindow)
        driver.execute_script(f"window.open('{mindfulnesswebsite}', '_blank');")

def get_countdown(duration):
    endTime = datetime.now() + timedelta(minutes=duration)
    try:
        while True:
            remainingTime = endTime - datetime.now()
            if remainingTime.total_seconds() <= 0:
                print("\nTime's up!")
                break
            mins, secs = divmod(int(remainingTime.total_seconds()), 60)
            sys.stdout.write(f"\r Time remaining: {mins:02}:{secs:02}")
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSession interrupted by user.")


def get_mode():
    while True:
        try:
            mode = input("Enter a mode (study, break, chill, mindfulness):")
            mode = mode.lower()
            if mode != "study" and mode != "break" and mode != "chill" and mode != "mindfulness":
                print("Invalid input. Please enter one of the following: study, break, chill, mindfulness.")
            else:
                break
        except ValueError:
            print("Please enter a valid input.")
    return mode

def get_duration():
    while True:
        try:
            timer = int(input("Enter the duration in minutes: "))
            break
        except ValueError:
            print("That's not a valid integer. Please try again.")
    return timer

def serve_page():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 80), handler) as httpd:
        httpd.serve_forever()

def block_sites(sites):
    with open(hosts_path, "r+") as file:
        content = file.read()
        for site in sites:
            entry = f"{redirect_ip} {site} {marker}\n"
            if entry not in content:
                file.write(entry)

def unblock_sites():
    with open(hosts_path, "r") as file:
        lines = file.readlines()
    with open(hosts_path, "w") as file:
        for line in lines:
            if marker not in line:
                file.write(line)

def main():
    print("Opening frequently used tabs.")
    driver = webdriver.Chrome()

    open_default_tabs(driver)
    input("Press Enter to continue...")

    mode = get_mode()
    timer = get_duration()


    if mode == "study":
        open_study_tabs(driver)
        restrictedDuringStudy = [
            "www.youtube.com",
            "makecode.microbit.org",
            "open.spotify.com",
            "www.netflix.com",
            "www.amazon.co.uk"
        ]
        block_sites(restrictedDuringStudy)

    elif mode == "break":
        open_break_tabs(driver)
        restrictedDuringChill = [
            "classroom.google.com",
            "www.physicsandmathstutor.com",
            "quizlet.com",
            "www.madasmaths.com",
            "revisionworld.com",
            "www.alevelphysicsonline.com",
            "web.uplearn.co.uk",
            "www.aqa.org.uk",
            "mail.google.com"
        ]
        block_sites(restrictedDuringChill)

    elif mode == "chill":
        open_chill_tabs(driver)
        restrictedDuringChill = [
            "classroom.google.com",
            "www.physicsandmathstutor.com",
            "quizlet.com",
            "www.madasmaths.com",
            "revisionworld.com",
            "www.alevelphysicsonline.com",
            "web.uplearn.co.uk",
            "www.aqa.org.uk",
            "mail.google.com"
        ]
        block_sites(restrictedDuringChill)

    elif mode == "mindfulness":
        open_mindfulness_tabs(driver)
        restrictedDuringMindfulness = [
            "classroom.google.com",
            "www.physicsandmathstutor.com",
            "quizlet.com",
            "www.madasmaths.com",
            "revisionworld.com",
            "www.alevelphysicsonline.com",
            "web.uplearn.co.uk",
            "www.aqa.org.uk",
            "www.netflix.com",
            "open.spotify.com",
            "www.youtube.com",
            "makecode.microbit.org",
            "www.amazon.co.uk",
            "www.linkedin.com",
            "mail.google.com"
        ]
        block_sites(restrictedDuringMindfulness)




    get_countdown(timer)

    driver.quit()
    unblock_sites()



if __name__ == "__main__":
    main()




