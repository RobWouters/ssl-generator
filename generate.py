#!/usr/bin/python

import re
import os
import sys
import subprocess as sp

HERE = os.path.dirname(__file__)

def main(cmd, domain):
    if cmd == 'csr':
        mkdir(domain)
        csr = generate_csr(domain)

def mkdir(domain):
    directory = os.path.join(HERE, domain)
    cmd = ['mkdir', '-p', directory]
    sp.call(cmd)

def generate_private_key(path):
    cmd = [
        'openssl',
        'genrsa',
        '-out',
        path,
    ]
    sp.call(cmd)
        
def get_private_key(key_file='./server.key'):
    key_file = os.path.abspath(os.path.realpath(key_file))
    if not os.path.isfile(key_file):
        generate_private_key(key_file)
    return key_file

def sign_csr(domain, csr):
    filename = 'server.crt'
    cmd = [
        'openssl', 'x509',
        '-req',
        '-days', '365',
        '-in', csr,
        '-signkey', '../server.key',
        '-out', filename,
    ]
    sp.call(cmd)
    return filename

def generate_csr(domain):
    filename = os.path.join(domain, 'server.csr')
    key = get_private_key()
    cmd = [
        'openssl', 'req',
        '-sha256',
        '-new',
        '-key', key,
        '-out', filename,
        '-subj', ('/C=NL/ST=Noord-Brabant/L=Schijndel'
                  '/O=Rob Wouters/CN={}').format(domain),
    ]
    sp.call(cmd)
    return filename

def get_domain(infile):
    cmd = [
        'openssl', 'req',
        '-in', infile,
        '-noout',
        '-text',
    ]
    output = sp.check_output(cmd)
    matches = re.search('CN=(.+)$', output, re.MULTILINE)
    return matches.group(1)

def usage():
    print('''Usage:

    {} csr <domain>
    '''.format(sys.argv[0]))

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        usage()
        sys.exit()

    main(*args)
