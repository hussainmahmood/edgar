#!/usr/bin/env python3
"""Print emails from a given date interval.

Usage:

    $ %(prog)s <since_date> <before_date>

since_date < before_date

Date format: DD-Mon-YYYY e.g., 3-Mar-2014

Based on http://pymotw.com/2/imaplib/
"""
import email
import sys
from datetime import datetime
from imaplib import IMAP4_SSL

import imaplib 
imaplib.Debug = True

def decode_header(header_string):
    try:
        decoded_seq = email.header.decode_header(header_string)
        return str(email.header.make_header(decoded_seq))
    except Exception: # fallback: return as is
        return header_string

def get_text(msg, fallback_encoding='utf-8', errors='replace'):
    """Extract plain text from email."""
    text = []
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            p = part.get_payload(decode=True)
            if p is not None:
                text.append(p.decode(part.get_charset() or fallback_encoding,
                                     errors))

# define since/before dates
date_format = "%d-%b-%Y" # DD-Mon-YYYY e.g., 3-Mar-2014
since_date = datetime.strptime(sys.argv[1], date_format)
before_date = datetime.strptime(sys.argv[2], date_format)

imap_host, imap_port = "imap.gmail.com", 993
login, password = 'efgh63535@gmail.com', 'Welcome@1'

# connect to the imap server
mail = IMAP4_SSL(imap_host, imap_port)
mail.login(login, password)
try:
    mail.select('INBOX', readonly=True)

    # get all messages since since_date and before before_date
    typ, [msg_ids] = mail.search(None,
        '(since "%s" before "%s")' % (since_date.strftime(date_format),
                                      before_date.strftime(date_format)))

    # get complete email messages in RFC822 format
    for num in msg_ids.split():
        typ, msg_data = mail.fetch(num, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                for header in [ 'subject', 'to', 'from', 'date' ]:
                    print('%-8s: %s' % (
                        header.upper(), decode_header(msg[header])))
                print(get_text(msg))
finally:
    try:
        mail.close()
    finally:
        mail.logout()