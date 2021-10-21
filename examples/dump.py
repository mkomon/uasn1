#
# This file is part of uASN1. uASN1 is free software that is
# made available under the MIT license. Consult the file "LICENSE" that is
# distributed together with this file for the exact licensing terms.
#
# uASN1 is copyright (c) 2007-2021 by the uASN1 authors. See the
# file "AUTHORS" for a complete overview.

import sys
import os.path
import base64

import uasn1
import optparse


def read_pem(input_data):
    """Read PEM formatted input."""
    data = []
    state = 0
    for line in input_data:
        if state == 0:
            if line.startswith('-----BEGIN'):
                state = 1
        elif state == 1:
            if line.startswith('-----END'):
                state = 2
            else:
                data.append(line)
        elif state == 2:
            break
    if state != 2:
        raise ValueError('No PEM encoded input found')
    data = ''.join(data)
    data = base64.b64decode(data)
    return data

def strid(id):
    """Return a string representation of a ASN.1 id."""
    if id == uasn1.Boolean:
        s = 'BOOLEAN'
    elif id == uasn1.Integer:
        s = 'INTEGER'
    elif id == uasn1.OctetString:
        s = 'OCTET STRING'
    elif id == uasn1.Null:
        s = 'NULL'
    elif id == uasn1.ObjectIdentifier:
        s = 'OBJECT IDENTIFIER'
    elif id == uasn1.Enumerated:
        s = 'ENUMERATED'
    elif id == uasn1.Sequence:
        s = 'SEQUENCE'
    elif id == uasn1.Set:
        s = 'SET'
    elif id == uasn1.Null:
        s = 'NULL'
    else:
        s = '%#02x' % id
    return s
 
def strclass(id):
    """Return a string representation of an ASN.1 class."""
    if id == uasn1.ClassUniversal:
        s = 'UNIVERSAL'
    elif id == uasn1.ClassApplication:
        s = 'APPLICATION'
    elif id == uasn1.ClassContext:
        s = 'CONTEXT'
    elif id == san1.ClassPrivate:
        s = 'PRIVATE'
    else:
        raise ValueError('Illegal class: %#02x' % id)
    return s

def strtag(tag):
    """Return a string represenation of an ASN.1 tag."""
    return '[%s] %s' % (strid(tag[0]), strclass(tag[2]))

def prettyprint(input_data, output, indent=0):
    """Pretty print ASN.1 data."""
    while not input_data.eof():
        tag = input_data.peek()
        if tag[1] == uasn1.TypePrimitive:
            tag, value = input_data.read()
            output.write(' ' * indent)
            output.write('[%s] %s (value %s)' %
                         (strclass(tag[2]), strid(tag[0]), repr(value)))
            output.write('\n')
        elif tag[1] == uasn1.TypeConstructed:
            output.write(' ' * indent)
            output.write('[%s] %s:\n' % (strclass(tag[2]), strid(tag[0])))
            input_data.enter()
            prettyprint(input_data, output, indent+2)
            input_data.leave()


# Main script

parser = optparse.OptionParser()
parser.add_option('-p', '--pem', dest='mode', action='store_const',
                  const='pem', help='PEM encoded input')
parser.add_option('-r', '--raw', dest='mode', action='store_const',
                  const='raw', help='raw input')
parser.add_option('-o', '--output', dest='output',
                  help='output to FILE instead', metavar='FILE')
parser.set_default('mode', 'pem')
(opts, args) = parser.parse_args()

if len(args) == 1:
    input_data = open(sys.argv[1])
else:
    input_data = sys.stdin

if opts.mode == 'pem':
    input_data = read_pem(input_data)
else:
    input_data = input.read()

if opts.output:
    output = open(opts.output, 'w')
else:
    output = sys.stdout

data = []
for line in input_data:
    data.append(line)
if isinstance(data[0], str):
    data = b''.join(data)
elif isinstance(data[0], int):
    data = bytes(data)
else:
    print('invalid data')

dec = uasn1.Decoder()
dec.start(data)

prettyprint(dec, output)
