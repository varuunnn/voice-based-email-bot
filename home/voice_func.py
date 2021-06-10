import speech_recognition as sr
import pyttsx3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from django.conf import settings
import email
import imaplib
from email.header import decode_header

def speak(text):
    engine.say(text)
    engine.runAndWait()


def hear():
    with sr.Microphone() as source:
        try:
            listener.pause_threshold = 1
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            info = listener.recognize_google(voice)
            print("User said: {}".format(info))
            return info
        except:
            speak("Sorry, couldn't hear your voice properly!!")
            hear()

def get_email_info():
    speak('Reciever\'s name?')
    name = hear()
    name = mail_list[name]
    speak("Okay")
    speak("Subject of your email?")
    subject = hear()
    speak("Okay")
    speak("Tell me the message in your email")
    message = hear()
    speak("Okay")
    speak("done")
    return name, subject, message


if __name__ == '__main__':
    PATH = "C:\\Program Files (x86)\\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("http:\\localhost:8000")

    listener = sr.Recognizer()
    engine = pyttsx3.init()
    engine.setProperty('rate', 145)
    speak("Welcome to your Email Bot")

    mail_list = {
        "Varun": "varunbhangre.11@gmail.com",
        "Pratham": "prathamsolanki.32.e.fe@gmail.com"
    }
    while True:
        query = hear().lower()

        if "quit" in query:
            speak("I am quitting")
            break

        elif "go to compose" in query:
            element = WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.ID, "compose-btn"))
            )
            element.click()
            speak("You may compose your mail now!")

        elif "start" in query:
            n, s, m = get_email_info()
            email = driver.find_element_by_id("email")
            email.send_keys(n)

            sub = driver.find_element_by_id("sub")
            sub.send_keys(s)

            mes = driver.find_element_by_id("message")
            mes.send_keys(m)

            speak("Should i send the mail?")
            x = hear().lower()
            if "yes" in x:
                send = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.ID, "send-btn"))
                )
                send.click()
                speak("Your mail is sent")
            elif "discard" in x:
                reset = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.ID, "reset-btn"))
                )
                reset.click()

        elif "inbox" in query:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "inbox-btn"))
            )
            element.click()
            host = 'imap.gmail.com'
            username = 'pythonminiprojectsem4@gmail.com'
            password = 'thadomalshahani'
            mail = imaplib.IMAP4_SSL(host)
            mail.login(username, password)
            mail.select("inbox")
            _, search_data = mail.search(None, 'UNSEEN')
            search_data = search_data[0].split()
            my_message = []
            if search_data:
                for num in search_data:
                    email_data = {}
                    _, data = mail.fetch(num, '(RFC822)')
                    email_message = email.message_from_bytes(data[0][1])
                    for header in ['subject', 'to', 'from']:
                        print("{}: {}".format(header, email_message[header]))
                        email_data[header] = email_message[header]
                    speak("Email from {}".format(email_data["from"]))
                    speak("The subject is {}".format(email_data["subject"]))
                    speak("Do you want me to read the mail?")
                    x = hear().lower()
                    if "yes" in x:
                        speak("The mail is")
                        for part in email_message.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True)
                                email_data['body'] = body.decode("utf-8")
                                print(email_data['body'])
                                speak(email_data['body'])

                        email = driver.find_element_by_id("email")
                        email.send_keys(email_data["from"])

                        sub = driver.find_element_by_id("sub")
                        sub.send_keys(email_data["subject"])

                        mes = driver.find_element_by_id("message")
                        mes.send_keys(email_data['body'])
                    elif "stop reading" in x:
                        break
                    else:
                        continue
                    #my_message.append(email_data)
                    # speaker.say(my_message)
                    # speaker.runAndWait()
            else:
                speak("No unread messages")
            speak("Done!")
