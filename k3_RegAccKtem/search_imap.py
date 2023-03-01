import imaplib, email, email.parser, email.policy
import html2text
import pprint, sys

#
# Utilities for Debug
#
pp = pprint.PrettyPrinter(indent=4, width=80)


def myprint(str):
    print(str.encode('cp932', 'replace').decode('cp932'))


#
# search mails in IMAP
#
def search_imap(usr, pwd):

    mail = imaplib.IMAP4_SSL("imap-mail.outlook.com")

    mail.login(usr, pwd)
    mail.list()
    mail.select('inbox')  # specify inbox
    # mail.select('register') # specify label

    # typ, [data] = mail.search(None, "UNSEEN")
    typ, [data] = mail.search(None, "(ALL)")

    # print("searched")
    # print(typ)
    # pp.pprint(data.split())

    # check
    # if typ == "OK":
    #     if data != '':
    #         print("New Mail")
    #     else:
    #         print("Non")

    # for each mail searched
    # for num in data.split():
    # get last mail
    for num in data.split()[-1:]:
        # print("START " + str(num) + "--------------------------------------------------")

        # fetch whole message as RFC822 format
        result, d = mail.fetch(num, "(RFC822)")

        # # save to file
        # f = open("mail_" + str(num) + ".txt", "bw")
        # f.write(d[0][1])
        # f.close()

        # print("####################################")

        msg = email2Text(d[0][1])

        # print("------------------------------------")
        # myprint(msg["subject"])
        # myprint(msg["date"])
        # myprint(msg["from"])
        return msg["body"]

    # closing
    mail.close()
    mail.logout()


#
# Get subject, date, from and body as text from email RFC822 style string
#
def email2Text(rfc822mail):
    # parse the message
    msg_data = email.message_from_bytes(rfc822mail, policy=email.policy.default)

    mail_value = {}

    # Get From, Date, Subject
    mail_value["from"] = header_decode(msg_data.get('From'))
    mail_value["date"] = header_decode(msg_data.get('Date'))
    mail_value["subject"] = header_decode(msg_data.get('Subject'))

    # print( mail_value["date"] )
    # print( mail_value["from"] )
    # print( mail_value["subject"] )

    # Get Body
    # print("--- body ---")
    mail_value["body"] = ""
    if msg_data.is_multipart():
        for part in msg_data.walk():
            # print("--- part ---")
            ddd = msg2bodyText(part)
            if ddd is not None:
                mail_value["body"] = mail_value["body"] + ddd
    else:
        # print("--- single ---")
        ddd = msg2bodyText(msg_data)
        mail_value["body"] = ddd

    return mail_value


#
# get body text from a message (EmailMessage instance)
#
def msg2bodyText(msg):
    ct = msg.get_content_type()
    cc = msg.get_content_charset()  # charset in Content-Type header
    cte = msg.get("Content-Transfer-Encoding")
    # print("part: " + str(ct) + " " + str(cc) + " : " + str(cte))

    # skip non-text part/msg
    if msg.get_content_maintype() != "text":
        return None

    # get text
    ddd = msg.get_content()

    # html to text
    if msg.get_content_subtype() == "html":
        try:
            ddd = html2text.html2text(ddd)
        except:
            print("error in html2text")

    return ddd


def header_decode(header):
    hdr = ""
    for text, encoding in email.header.decode_header(header):
        if isinstance(text, bytes):
            text = text.decode(encoding or "us-ascii")
        hdr += text
    return hdr

sys.modules[__name__] = search_imap
