import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
    
def sendEmail(fromAddress, toAddress, password, contents, attachFile = None):
    """This function sends an email with the possibility to attach a file
    
        Inputs:
            fromAddress: who you want the email to come from
            toAddress: who you want to send the email to
            password: the password for the from email
            contents = [subject: subject for the email, body: email body]
            attachfile = [filename: name of the file, pathway: pathway to get to that file]
    """

    
    msg = MIMEMultipart()
    msg['From'] = fromAddress
    msg['To'] = toAddress
    
    subject, body = contents
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    if attachFile:
        filename, pathway = attachFile
        
        attachment = open(pathway, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename= %s" % filename)
        msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddress, password)
    text = msg.as_string()
    server.sendmail(fromAddress, toAddress, text)
    server.quit()
    
if __name__ == "__main__":
    fromAddress = "CandCSec370@gmail.com"
    toAddress = "CandCSec370@gmail.com"
    password = "grounds4lyfe"
    attachFile = ["hacker.jpg", "./hacker.jpg"]
    contents = ["Testing email alert", "This email is a test for the alerts\n\n Thanks."]
    sendEmail(fromAddress, toAddress, password, contents)
    print("Your email to %s has been sent." % toAddress)
    
