import requests
from bs4 import BeautifulSoup
import smtplib, ssl


if __name__ == "__main__":
    url = "minciencias.gov.co/convocatorias/todas" # URL that you want to extract information from
    id_url = "Minciencias"

    r  = requests.get("https://" + url, verify=False) # Stores a get request to the site

    data = r.text # Extract the get response into variable data

    soup = BeautifulSoup(data) # Creates BeautifulSoup object with data

    file_route = "/home/01_webscrapping/scrapping_file_minciencias.txt" # File route for the file with previous scrapping information
    temp_route = "/home/01_webscrapping/temp.txt" # File route to a temporal file for comparisson with the scrapping file
    
    file_text = open(file_route, 'r', encoding='utf-8')
    lines = file_text.readlines()
    file_text.close()

    if len(lines) == 0:
        empty_file = True
    else:
        empty_file = False

    links = []
    links_in_file = True
    
    # Finds all the links within the scrapped page that contain 'node' and stores them in a list
    for link in soup.find_all('a'):
        str_link = str(link)
        if 'node' in str_link:
            links.append(str_link)
    
    # Writes the temp file with all the links found
    temp_text = open(temp_route, 'w', encoding='utf-8')
    for link in links:
        temp_text.write(link + '\n')
    temp_text.close()

    temp_text = open(temp_route, 'r', encoding='utf-8')
    temp_lines = temp_text.readlines()
    
    # Determines whether the file with the scrapped site (target) is equal to the temp file.
    # If the target file is empty or if both files do not match, it means a change in the web page occured 
    # and the target file is overwritten with the new information.
    if empty_file:
        file_text = open(file_route, 'w+', encoding='utf-8')
        print('Writing file...')
        for link in links:
            file_text.write(link + '\n')
    else:
        for line in temp_lines:
            if line not in lines:
                links_in_file = False

    if not links_in_file:
        print('Writing file...')
        file_text = open(file_route, 'w+', encoding='utf-8')
        for link in links:
            file_text.write(link + '\n')

    # Sets up the email information for the communication
    port = 465  # For SSL
    sender_email = "sender@sender.com" # Replace with sender email
    receiver_email = "receiver@receiver.com" # Replace with receiver email
    password = "PasswordExample" # Replace with password for sender email
    # Formatted message for email
    message = """From: Automatic <{0}>
To: Receiver <{1}>
Subject: Cambio en pagina web {2}

Cambio en pagina {3}
""".format(sender_email, receiver_email, id_url, url)

    # If there was a change in the web page an email is sent
    if empty_file or not links_in_file:
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server: # Change SMTP server accordingly
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

    file_text.close()
    temp_text.close()