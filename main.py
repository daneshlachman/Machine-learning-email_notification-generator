from model import return_voorspelling
import smtplib
import ssl

# configuratie voor versturen van email-notificatie
poort = 465
smtp_server = "smtp.gmail.com"
verstuurder_email = "Wifinityalerting@gmail.com"
ontvanger_email = "Wifinityalerting@gmail.com"
wachtwoord = str(input("Geef het wachtwoord op van het emailadres\n"))

# definieer mogelijke redenen van uitval
lijst_van_redenen_van_uitval = ["Probleem met switch", "Internet is uitgevallen",
                                "Stroom is uitgevallen",
                                "AP defect door mogelijk (deels) defecte antenne"]


# voor voorspelling uit
voorspelling_klasse =  return_voorspelling()

# correspondeer classificatie getal met reden van uitval text, om  vervolgens te gebruiken in email-notificatie
reden_van_uitval = lijst_van_redenen_van_uitval[voorspelling_klasse]

# opstellen van email-notificatie
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
with smtplib.SMTP_SSL(smtp_server, poort, context=context) as server:
    server.login(verstuurder_email, wachtwoord)
    server.sendmail(verstuurder_email, ontvanger_email, message)
