import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
    
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

def generateEmailBody(filename = None):
    """This function generates the body of the email with the option
        to include the filename of the image of unauthorized user.
        
        Inputs:
            filename: name of image 
        Outputs:
            body: body of the email
    """
    
    body = "Hello,\n\nThere was an attempt to access your device at "
    
    now = datetime.datetime.now()
    body += now.strftime("%Y-%m-%d %H:%M") + ".\n"
    
    if filename:
        body += "The individual trying to access your account can be seen in the attached file "
        body += filename + "."
        body += " This individual was denied access to your account.\n"
        
    body += "\nYour friends at C & C Security."
    return body

if __name__ == "__main__":
    fromAddress = "CandCSec370@gmail.com"
    toAddress = "CandCSec370@gmail.com"
    password = #PUT GMAIL PASSWORD HERE
    
    attachFile = ["""IMAGE FILE NAME HERE, IMAGE PATHWAY HERE"""]
    contents = ["Attempted Access", generateEmailBody(attachFile[0])]
    
    sendEmail(fromAddress, toAddress, password, contents, attachFile)
    print("Your email to %s has been sent." % toAddress)
    
