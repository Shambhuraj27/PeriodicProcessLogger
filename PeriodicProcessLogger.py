
import os
import time
import psutil
import smtplib
import schedule
from email import encoders
import urllib.request as urllib2
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

# Function to check internet connectivity
def is_connected():
    try:
         # Try to connect to Google's website
        urllib2.urlopen('https://www.google.com/', timeout=1)
        return True
    except urllib2.URLError as err:
        return False

# Function to send the log file via email
def MailSender(filename, time):
    fromaddr = "..........@gmail.com" # Sender's email address
    toaddr = "..........@gmail.com" # Recipient's email address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr

    # Email body content
    body = f"""
         Hello {toaddr},
         Please find attached document which contains log of Running process
         Log file created at : {time}

         This is auto generated mail.
         Thanks & Regards,
         sender's name
        """ 
    # Subject of the email
    Subject = f"Process log generated at: {time}"
    msg['Subject'] = Subject
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p) # Convert binary data into text
    p.add_header('Content-Disposition', "attachment; filename={filename}")
    msg.attach(p)

    # Setup the SMTP server for sending the email
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, 'sender's password')

    # Convert the message to a string and send the email
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
    print("Log file successfully sent through Mail")

# Function to create a log file and send it via email
def ProcessLog(log_dir='Processes'):
    listprocess = []  # List to store process details

    # Check if the log directory exists; if not, create it
    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    seperator = "-" * 80
    time_string = time.ctime().replace(':', '_')
    log_path = os.path.join(log_dir, f"ProcessesLog {time_string}")
    
    # Open the log file in write mode and add headers
    f = open(log_path, 'w')
    f.write(seperator + "\n")
    f.write(f"Process Logger :{time.ctime()}\n")
    f.write(seperator + "\n")
    f.write("\n")

    # Fetch process details using psutil
    for process in psutil.process_iter():
        pinfo = process.as_dict(attrs=['pid', 'name', 'username'])
        listprocess.append(pinfo) # Add process details to the list
    
    # Write process details to the log file 
    for element in listprocess:
        f.write(f"{element}\n")

    print(f"Log file is successfully generated at location,{log_path}")

    # Check internet connectivity before sending the email 
    connected = is_connected()
    if connected:
        startTime = time.time()
        MailSender(log_path, time.ctime())
        endTime = time.time()

        print(f"Took {endTime - startTime:.2f} seconds to send mail")
    else:
        print("There is no internet connection")

# Main function to schedule the log creation and email sending task
def main():
    schedule.every(1).minutes.do(ProcessLog)
    while True:
        schedule.run_pending() # Run any pending scheduled tasks
        time.sleep(1) # Sleep for 1 second before checking again
if __name__ == "__main__":
    main()


