#EMAIL_DRIVER
its literally just an email driver

#COMMAND LIST

s = smtp_mail(USER,PASS)

s.login(s.GMAIL_DEFAULT_ORG)

s.send_mail("EMAIL_ADDRESS","MESSAGE")

s.close()

m = imap_mail(USER,PASS)

m.login(m.GMAIL_DEFAULT_ORG)

m.get_mail(m.GMAIL_DEFAULT_FOLDER,m.DEFAULT_MESSAGE_AMOUNT)

m.close()
