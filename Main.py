from Model import return_voorspelling
import smtplib
import ssl

port = 465
smtp_server = "smtp.gmail.com"
sender_email = "Wifinityalerting@gmail.com"  # Enter your address
receiver_email = "Wifinityalerting@gmail.com"  # Enter receiver address
password = str(input("Geef het wachtwoord op van het emailadres\n"))

lijst_van_redenen_van_uitval = ["Probleem met switch", "Internet is uitgevallen", "Stroom is uitgevallen", "AP defect door mogelijk (deels) defecte antenne"]

voorspelling_klasse =  return_voorspelling()

reden_van_uitval = lijst_van_redenen_van_uitval[voorspelling_klasse]

message = """\
Subject: Machine learning alert

Beste Wifinity,

Het machine learning model heeft een reden uitval kunnen herkennen.

Reden van uitval:

{}


Met vriendelijke groet,

Het machine learning model

""".format(reden_van_uitval)

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
