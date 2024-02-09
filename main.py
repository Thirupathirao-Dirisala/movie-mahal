from queue import Queue
from threading import Thread
import requests
from flask import Flask, Request, Response, redirect, render_template, request, session, url_for
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
app = Flask(__name__)
result_queue=Queue()
app.secret_key='movie_mahal'
movies=["saindhav","hinanna","salaar","neru","bhagavanthkesari","mad","animal","pushpa","virupaksha","paramporul","pindam"]
links=["https://bestfile.io/en/T3oPbZ94sdf3QFO/file","https://bestfile.io/en/i9to5RpiY3so2c2/file","https://bestfile.io/en/JiJcjrkl1hErhJe/file",
       "https://bestfile.io/en/wZ0STCQGgHUpFxL/file","https://bestfile.io/en/XyZGmtHIebJZ3Eh/file","https://bestfile.io/en/NxkbyQQftQ4atwT/file",
       "https://bestfile.io/en/RD2JNT1Ileb5i0L/file","https://bestfile.io/en/UYx3whN1UXafU8r/file","https://bestfile.io/en/CzP2fhSqZdp8N8s/file",
       "https://bestfile.io/en/MWncZwk2E9bN482/file","https://bestfile.io/en/JNwKzzsxdfJf6FW/file"]
def perform_web_scraping(text,result_queue):
    # Create a WebDriver instance
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    
        # Load the webpage
    driver.get(text)

        # Wait for the element to be present
    element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "download-link"))
    )

        # Get the attribute value
    link= element.get_attribute("href")

        # Output the attribute value
    print("Attribute Value:", link)
    result_queue.put(link)
        # Close the WebDriver instance
    driver.quit()
    return link

@app.route('/')
def index():
    # Define some data to pass to the template
    message = "Hello from Python!"

    # Render the HTML template with the data
    return render_template('index.html', message=message)
@app.route('/scrape',methods=['POST'])
def scrape():
    if request.method == 'POST':
        name = request.form['movie']
        for i in range(len(movies)):
            if movies[i]==name:
                text=links[i]            
    t = Thread(target=perform_web_scraping,args=(text,result_queue))
    t.start()
    
    # Start the timer before performing the web scraping
    return render_template('scrape.html')
    
@app.route('/download')
def submit():
    link = result_queue.get()
    return render_template('video.html',link=link)


if __name__ == '__main__':
    app.run(debug=True)