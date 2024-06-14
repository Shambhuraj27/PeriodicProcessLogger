
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
def is_connected():
    try:
        urllib2.urlopen('https://www.google.com/', timeout=1)
        return True
    except urllib2.URLError as err:
        return False
def MailSender(filename, time):
    fromaddr = "27.sspatil@gmail.com"
    toaddr = "shambhurajpatil27@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr

    body = """
         Hello %s,
         Please find attached document which contains log of Running process
         Log file created at : %s

         This is auto generated mail.
         Thanks & Regards,
         Shambhuraj Patil
            """ % (toaddr, time)

    Subject = """
         Process log generated at : %s
         """ % (time)
    msg['Subject'] = Subject
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename=%s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, '-----------')

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()
    print("Log file successfully sent through Mail")
def ProcessLog(log_dir='Processes'):
    listprocess = []

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    seperator = "-" * 80
    time_string = time.ctime().replace(':', '_')
    log_path = os.path.join(log_dir, "ProcessesLog %s.log" % (time_string))
    f = open(log_path, 'w')
    f.write(seperator + "\n")
    f.write("Process Logger :" + time.ctime() + "\n")
    f.write(seperator + "\n")
    f.write("\n")

    for process in psutil.process_iter():
        pinfo = process.as_dict(attrs=['pid', 'name', 'username'])
        listprocess.append(pinfo);

    for element in listprocess:
        f.write("%s\n" % element)

    print("Log file is successfully generated at location", (log_path))

    connected = is_connected()

    if connected:
        startTime = time.time()
        MailSender(log_path, time.ctime())
        endTime = time.time()

        print('Took %s seconds to send mail' % (endTime - startTime))
    else:
        print("There is no internet connection")
def main():
    schedule.every(1).minutes.do(ProcessLog)
    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == "__main__":
    main()










