# Copyright (c) 2012 Mathieu Lecarme
# This code is licensed under the MIT license (see LICENSE for details)

import imaplib
import os
from salmon.mail import MailRequest

def idle(connection):
    tag = connection._new_tag()
    connection.send(b"%s IDLE" % tag)
    response = connection.readline()
    connection.loop = True
    if response == '+ idling':
        while connection.loop:
            resp = connection.readline()
            uid, message = resp[2:-2].split(' ')
            yield uid, message
    else:
        raise Exception(b"IDLE not handled? : %s" % response)


def done(connection):
    connection.send("DONE")
    connection.loop = False

imaplib.IMAP4.idle = idle
imaplib.IMAP4.done = done

def main():
    conn = imaplib.IMAP4_SSL('imap.gmail.com')
    conn.login('hussainmahmood819', 'hybridme@123')
    conn.select()
    loop = True
    while loop:
        for uid, msg in conn.idle():
            print(uid, msg)
            if msg == "EXISTS":
                conn.done()
                status, datas = conn.fetch(uid, '(RFC822)')
                m = MailRequest('localhost', None, None, datas[0][1])
                print(m.keys())
                print(m.items())
                print(m.is_bounce())

if __name__ == '__main__':
    main()
