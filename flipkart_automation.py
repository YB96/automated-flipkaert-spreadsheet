import smtplib
import pandas as pd
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
from password import username, password 
#create a .py file in same folder contaning username and password of you id and import it to send the automated email. 

base_url = 'https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3DAPPLE&page='

def mobile_name(doc_new):
    prase = doc_new.find_all('div', class_='_4rR01T')
    names = []
    for tag in prase:
        names.append(tag.text.strip())
    return names

def prices(doc_new):
    price = doc_new.find_all('div',class_='_30jeq3 _1_WHN1')
    price_link = []
    for i in price:
        price_link.append(i.text.strip())
    return price_link

def percentage_off(doc_new):
    off = doc_new.find_all('div',class_='_3Ay6Sb')
    off_link =[]
    for i in off:
        off_link.append({'Percentage off':i.text.strip()})
    return off_link  

def rating(doc_new):
    ratings = doc_new.find_all('div', class_='_3LWZlK')
    all_ratings = []
    for i in ratings:
        all_ratings.append(i.text.strip())
    return all_ratings

def mobile_description(doc_new):
    mobile_description = doc_new.find_all('ul', class_='_1xgFaf')
    mobile_info_link=[]
    for i in mobile_description:
        mobile_info_link.append(i.text.strip())
    return mobile_info_link 

def for_all_pages(page_no):
    page_no_url = base_url +  str(page_no)
    response = requests.get(page_no_url)
    
    if response.status_code != 200:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page ' + page_no_url)
        
    doc_new =  BeautifulSoup(response.text, features='html.parser')
    mobile_names_new = mobile_name(doc_new)
    all_prices_new = prices(doc_new)
    all_ratings_new = rating(doc_new)
    first_page_new = mobile_description(doc_new)
    data_new = {'Name': mobile_names_new,  #getting all the information in a dictionary
       'Prices':all_prices_new,
       'ratings':all_ratings_new,
       'Description':first_page_new}
    
    return pd.DataFrame(data_new)   #return directly a dataframe.

#Below is our helper function to add all data frames.

def all_info(num_of_page):
    # define an empty list
    all_df = []
    # Run a loop from 1 to n+1
    for i in range(1, num_of_page+1):
        all_df.append(for_all_pages(page_no=i))
        # Outside the loop variable you can directly merge the df and return it in the same line.
        merge = pd.concat(all_df)
        csv = merge.to_csv('all info.csv',index=None)
    return csv

def send_email(body):
    
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()   

    emailfrom = 'yb4coding@gmail.com'
    emailto = 'yb4coding@gmail.com'
    fileToSend = "all info.csv"

    username_mail = username
    password_mail = password
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Spreadsheet of iPhones present in flipkart contating all information."
        

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(username_mail,password_mail)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()

if __name__ == "__main__":
    print('Creating dataframe')
    df = for_all_pages(8)

    print('Creating csv file')
    csv_file = all_info(8)
#Note - no of pages for dataframe and csv file should be equal to let the code work because they are connected.
    print("Send the csv file over email")
    body = csv_file
    send_email(body)
    print('Your file has been delivered')


