#R. CODY 2019 ALL RIGHTS ALLOWED. I DON'T CARE. DO WHAT YOU WANT.

#Carry out the necessary imports
import imaplib,smtplib,email,time

#Construct the imap_mail object
class smtp_mail(object):
    def __init__(self,USER,PASS):
        self.USERNAME=USER
        self.PASSWORD=PASS
    
    GMAIL_DEFAULT_ORG='smtp.gmail.com'
    
    def login(self,ORG):
        #Connect to the SMTP server
        self.S = smtplib.SMTP(ORG)
        #Start TLS for secrurity
        self.S.starttls()
        #Authentication 
        self.S.login(self.USERNAME, self.PASSWORD)
        
    def send_mail(self,to,message):
        #send the message
        self.S.sendmail(self.USERNAME,to,message)

    def close(self):
        #closes the connections 
        self.S.quit() 
        
class imap_mail(object):
    DEFAULT_MESSAGE_AMOUNT=10
    GMAIL_DEFAULT_ORG='imap.gmail.com'
    GMAIL_DEFAULT_FOLDER='Inbox'
    BAD_WORDS = ['Facebook','facebook','http','https','on this post','======','below to learn more','Email Settings','unsubscribe','Unsubscribe']
    def __init__(self,USER,PASS):
        #Set username and password
        self.USERNAME=USER
        self.PASSWORD=PASS

    def login(self,ORG):
        #Connect to the Org's ssl layer
        self.M = imaplib.IMAP4_SSL(ORG)
        #try to login
        try:
            rv, data = self.M.login(self.USERNAME,self.PASSWORD)
        except imaplib.IMAP4.error:
            print("LOGIN FAILED!!! ")
            #If it fails the first time try 5 more times
            for i in range(5):
                print("Trying Again!")
                try:
                    rv, data = self.M.login(self.USERNAME,self.PASSWORD)
                    break
                except imaplib.IMAP4.error:
                    time.sleep(4)
                    print("LOGIN FAILED AGAIN!!! ")
                

    def get_mailboxes(self):
        rv, mailboxes = self.M.list()
        if rv == 'OK':
            return mailboxes
        else:
            return list(None)

    def get_mail(self,FOLDER,NUM_EMAILS):
        #Set message amount counter
        message_amount = 0
        #Select the folder we will read from
        rv, data = self.M.select(FOLDER,readonly=True)
        #Check if we got the OK
        if rv == 'OK':
            #If so search for all messages
            typ, data = self.M.search(None, 'ALL')
            #Create the response list
            messages=[]
            #Create the necessary dictionary slots
            #for i in range(NUM_EMAILS):
            #messages.append({})
            #Invert and iterate through the list of mail IDS
            for num in data[0].split()[::-1]:
                #Check if the limit of mails has been reached yet
                if message_amount >= int(NUM_EMAILS):
                    #If so then break the loop
                    break
                #Fetch the specified email
                typ, data = self.M.fetch(num, '(RFC822)')
                #Convert it into an email type object
                msg = email.message_from_bytes(data[0][1])
                messages.append({})
                #Add the date to the response
                messages[int(message_amount)]['date']=msg['Date']
                #Add the sender to the response
                messages[int(message_amount)]['from']=msg['from']
                #Add the subject to the response
                messages[int(message_amount)]['subject']=msg['subject']
                #Sets the text list variable to default
                text = []
                #Finds the plain text version of the body of the message.
                if msg.get_content_maintype() == 'multipart':
                    #If message is multi part we only want the text version of the body
                    #this walks the message and gets the body.
                    for part in msg.walk():
                        #Checks if the part is plain text
                        if part.get_content_type() == "text/plain":
                            #If so the payload is decoded
                            body = str(part.get_payload(decode=True))
                            #The weird newline characters are fixed and the text is split into a lit
                            body = list(body.replace(r"\r\n", "\n").split('\n'))
                            #Iterate through the list of the body
                            for line in body:
                                #Check if any of our "Badwords" are in there
                                if not any(bad_word in line for bad_word in self.BAD_WORDS):
                                    #If not add it to the output
                                    text.append(line)
                #Add the body list to our output file
                messages[int(message_amount)]['body']=text
                #Increase the message number by one
                message_amount += 1
            #Return messages
            return messages
        else:
            print("ERROR: Unable to open mailbox ", rv)
            return None

    def close(self):
        self.M.close()
        self.M.logout()
