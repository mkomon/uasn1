#
# This file is part of uASN1. uASN1 is free software that is
# made available under the MIT license. Consult the file "LICENSE" that
# is distributed together with this file for the exact licensing terms.
#
# uASN1 is copyright (c) 2007-2021 by the uASN1 authors. See the
# file "AUTHORS" for a complete overview.

import uasn1
from nose.tools import assert_raises


class TestEncoder(object):
    """Test suite for ASN1 Encoder."""

    def test_boolean(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.write(True, uasn1.Boolean)
        res = enc.output()
        assert res == b'\x01\x01\xff'

    def test_integer(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.write(1)
        res = enc.output()
        assert res == b'\x02\x01\x01'

    def test_long_integer(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.write(0x0102030405060708090a0b0c0d0e0f)
        res = enc.output()
        assert res == b'\x02\x0f\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'

    def test_negative_integer(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.write(-1)
        res = enc.output()
        assert res == b'\x02\x01\xff'

    def test_long_negative_integer(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.write(-0x0102030405060708090a0b0c0d0e0f)
        res = enc.output()
        assert res == b'\x02\x0f\xfe\xfd\xfc\xfb\xfa\xf9\xf8\xf7\xf6\xf5\xf4\xf3\xf2\xf1\xf1'

    def test_twos_complement_boundaries(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.write(127)
        res = enc.output()
        assert res == b'\x02\x01\x7f'
        enc.start()
        enc.write(128)
        res = enc.output()
        assert res == b'\x02\x02\x00\x80'
        enc.start()
        enc.write(-128)
        res = enc.output()
        assert res == b'\x02\x01\x80'
        enc.start()
        enc.write(-129)
        res = enc.output()
        assert res == b'\x02\x02\xff\x7f'

    def test_octet_string(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.write('foo')
        res = enc.output()
        assert res == b'\x04\x03foo'

    def test_null(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.write(None)
        res = enc.output()
        assert res == b'\x05\x00'

    def test_object_identifier(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.write('1.2.3', uasn1.ObjectIdentifier)
        res = enc.output()
        assert res == b'\x06\x02\x2a\x03'

    def test_long_object_identifier(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.write('39.2.3', uasn1.ObjectIdentifier)
        res = enc.output()
        assert res == b'\x06\x03\x8c\x1a\x03'
        enc.start()
        enc.write('1.39.3', uasn1.ObjectIdentifier)
        res = enc.output()
        assert res == b'\x06\x02\x4f\x03'
        enc.start()
        enc.write('1.2.300000', uasn1.ObjectIdentifier)
        res = enc.output()
        assert res == b'\x06\x04\x2a\x92\xa7\x60'

    def test_real_object_identifier(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.write('1.2.840.113554.1.2.1.1', uasn1.ObjectIdentifier)
        res = enc.output()
        assert res == b'\x06\x0a\x2a\x86\x48\x86\xf7\x12\x01\x02\x01\x01'

    def test_enumerated(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.write(1, uasn1.Enumerated)
        res = enc.output()
        assert res == b'\x0a\x01\x01'

    def test_sequence(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.enter(uasn1.Sequence)
        enc.write(1)
        enc.write('foo')
        enc.leave()
        res = enc.output()
        assert res == b'\x30\x08\x02\x01\x01\x04\x03foo'

    def test_sequence_of(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.enter(uasn1.Sequence)
        enc.write(1)
        enc.write(2)
        enc.leave()
        res = enc.output()
        assert res == b'\x30\x06\x02\x01\x01\x02\x01\x02'

    def test_set(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.enter(uasn1.Set)
        enc.write(1)
        enc.write('foo')
        enc.leave()
        res = enc.output()
        assert res == b'\x31\x08\x02\x01\x01\x04\x03foo'

    def test_set_of(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.enter(uasn1.Set)
        enc.write(1)
        enc.write(2)
        enc.leave()
        res = enc.output()
        assert res == b'\x31\x06\x02\x01\x01\x02\x01\x02'

    def test_context(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.enter(1, uasn1.ClassContext)
        enc.write(1)
        enc.leave()
        res = enc.output()
        assert res == b'\xa1\x03\x02\x01\x01'

    def test_application(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.enter(1, uasn1.ClassApplication)
        enc.write(1)
        enc.leave()
        res = enc.output()
        assert res == b'\x61\x03\x02\x01\x01'

    def test_private(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.enter(1, uasn1.ClassPrivate)
        enc.write(1)
        enc.leave()
        res = enc.output()
        assert res == b'\xe1\x03\x02\x01\x01'

    def test_long_tag_id(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.enter(0xffff)
        enc.write(1)
        enc.leave()
        res = enc.output()
        assert res == b'\x3f\x83\xff\x7f\x03\x02\x01\x01'

    def test_long_tag_length(self):
        enc = uasn1.Encoder()
        enc.start()
        enc.write('x' * 0xffff)
        res = enc.output()
        assert res == b'\x04\x82\xff\xff' + b'x' * 0xffff

    def test_error_init(self):
        enc = uasn1.Encoder()
        assert_raises(uasn1.Error, enc.enter, uasn1.Sequence)
        assert_raises(uasn1.Error, enc.leave)
        assert_raises(uasn1.Error, enc.write, 1)
        assert_raises(uasn1.Error, enc.output)

    def test_error_stack(self):
        enc = uasn1.Encoder()
        enc.start()
        assert_raises(uasn1.Error, enc.leave)
        enc.enter(uasn1.Sequence)
        assert_raises(uasn1.Error, enc.output)
        enc.leave()
        assert_raises(uasn1.Error, enc.leave)

    def test_error_object_identifier(self):
        enc = uasn1.Encoder()
        enc.start()
        assert_raises(uasn1.Error, enc.write, '1', uasn1.ObjectIdentifier)
        assert_raises(uasn1.Error, enc.write, '40.2.3', uasn1.ObjectIdentifier)
        assert_raises(uasn1.Error, enc.write, '1.40.3', uasn1.ObjectIdentifier)
        assert_raises(uasn1.Error, enc.write, '1.2.3.', uasn1.ObjectIdentifier)
        assert_raises(uasn1.Error, enc.write, '.1.2.3', uasn1.ObjectIdentifier)
        assert_raises(uasn1.Error, enc.write, 'foo', uasn1.ObjectIdentifier)
        assert_raises(uasn1.Error, enc.write, 'foo.bar', uasn1.ObjectIdentifier)


class TestDecoder(object):
    """Test suite for ASN1 Decoder."""

    def test_boolean(self):
        buf = b'\x01\x01\xff'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (uasn1.Boolean, uasn1.TypePrimitive, uasn1.ClassUniversal)
        tag, val = dec.read()
        assert isinstance(val, int)
        assert val == True
        buf = b'\x01\x01\x01'
        dec.start(buf)
        tag, val = dec.read()
        assert isinstance(val, int)
        assert val == True
        buf = b'\x01\x01\x00'
        dec.start(buf)
        tag, val = dec.read()
        assert isinstance(val, int)
        assert val == False

    def test_integer(self):
        buf = b'\x02\x01\x01'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (uasn1.Integer, uasn1.TypePrimitive, uasn1.ClassUniversal)
        tag, val = dec.read()
        assert isinstance(val, int)
        assert val == 1

    def test_long_integer(self):
        buf = b'\x02\x0f\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag, val = dec.read()
        assert val == 0x0102030405060708090a0b0c0d0e0f

    def test_negative_integer(self):
        buf = b'\x02\x01\xff'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag, val = dec.read()
        assert val == -1

    def test_long_negative_integer(self):
        buf = b'\x02\x0f\xfe\xfd\xfc\xfb\xfa\xf9\xf8\xf7\xf6\xf5\xf4\xf3\xf2\xf1\xf1'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag, val = dec.read()
        assert val == -0x0102030405060708090a0b0c0d0e0f

    def test_twos_complement_boundaries(self):
        buf = b'\x02\x01\x7f'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag, val = dec.read()
        assert val == 127
        buf = b'\x02\x02\x00\x80'
        dec.start(buf)
        tag, val = dec.read()
        assert val == 128
        buf = b'\x02\x01\x80'
        dec.start(buf)
        tag, val = dec.read()
        assert val == -128
        buf = b'\x02\x02\xff\x7f'
        dec.start(buf)
        tag, val = dec.read()
        assert val == -129

    def test_octet_string(self):
        buf = b'\x04\x03foo'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (uasn1.OctetString, uasn1.TypePrimitive, uasn1.ClassUniversal)
        tag, val = dec.read()
        assert isinstance(val, bytes)
        assert val == b'foo'

    def test_null(self):
        buf = b'\x05\x00'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (uasn1.Null, uasn1.TypePrimitive, uasn1.ClassUniversal)
        tag, val = dec.read()
        assert val is None

    def test_object_identifier(self):
        dec = uasn1.Decoder()
        buf = b'\x06\x02\x2a\x03'
        dec.start(buf)
        tag = dec.peek()
        assert tag == (uasn1.ObjectIdentifier, uasn1.TypePrimitive,
                       uasn1.ClassUniversal)
        tag, val = dec.read()
        assert val == '1.2.3'

    def test_long_object_identifier(self):
        dec = uasn1.Decoder()
        buf = b'\x06\x03\x8c\x1a\x03'
        dec.start(buf)
        tag, val = dec.read()
        assert val == '39.2.3'
        buf = b'\x06\x02\x4f\x03'
        dec.start(buf)
        tag, val = dec.read()
        assert val == '1.39.3'
        buf = b'\x06\x04\x2a\x92\xa7\x60'
        dec.start(buf)
        tag, val = dec.read()
        assert val == '1.2.300000'

    def test_real_object_identifier(self):
        dec = uasn1.Decoder()
        buf = b'\x06\x0a\x2a\x86\x48\x86\xf7\x12\x01\x02\x01\x01'
        dec.start(buf)
        tag, val = dec.read()
        assert val == '1.2.840.113554.1.2.1.1'

    def test_enumerated(self):
        buf = b'\x0a\x01\x01'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (uasn1.Enumerated, uasn1.TypePrimitive, uasn1.ClassUniversal)
        tag, val = dec.read()
        assert isinstance(val, int)
        assert val == 1

    def test_sequence(self):
        buf = b'\x30\x08\x02\x01\x01\x04\x03foo'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (uasn1.Sequence, uasn1.TypeConstructed, uasn1.ClassUniversal)
        dec.enter()
        tag, val = dec.read()
        assert val == 1
        tag, val = dec.read()
        assert val == b'foo'

    def test_sequence_of(self):
        buf = b'\x30\x06\x02\x01\x01\x02\x01\x02'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (uasn1.Sequence, uasn1.TypeConstructed, uasn1.ClassUniversal)
        dec.enter()
        tag, val = dec.read()
        assert val == 1
        tag, val = dec.read()
        assert val == 2

    def test_set(self):
        buf = b'\x31\x08\x02\x01\x01\x04\x03foo'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (uasn1.Set, uasn1.TypeConstructed, uasn1.ClassUniversal)
        dec.enter()
        tag, val = dec.read()
        assert val == 1
        tag, val = dec.read()
        assert val == b'foo'

    def test_set_of(self):
        buf = b'\x31\x06\x02\x01\x01\x02\x01\x02'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (uasn1.Set, uasn1.TypeConstructed, uasn1.ClassUniversal)
        dec.enter()
        tag, val = dec.read()
        assert val == 1
        tag, val = dec.read()
        assert val == 2

    def test_context(self):
        buf = b'\xa1\x03\x02\x01\x01'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (1, uasn1.TypeConstructed, uasn1.ClassContext)
        dec.enter()
        tag, val = dec.read()
        assert val == 1

    def test_application(self):
        buf = b'\x61\x03\x02\x01\x01'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (1, uasn1.TypeConstructed, uasn1.ClassApplication)
        dec.enter()
        tag, val = dec.read()
        assert val == 1

    def test_private(self):
        buf = b'\xe1\x03\x02\x01\x01'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (1, uasn1.TypeConstructed, uasn1.ClassPrivate)
        dec.enter()
        tag, val = dec.read()
        assert val == 1

    def test_long_tag_id(self):
        buf = b'\x3f\x83\xff\x7f\x03\x02\x01\x01'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (0xffff, uasn1.TypeConstructed, uasn1.ClassUniversal)
        dec.enter()
        tag, val = dec.read()
        assert val == 1

    def test_long_tag_length(self):
        buf = b'\x04\x82\xff\xff' + b'x' * 0xffff
        dec = uasn1.Decoder()
        dec.start(buf)
        tag, val = dec.read()
        assert val == b'x' * 0xffff

    def test_read_multiple(self):
        buf = b'\x02\x01\x01\x02\x01\x02'
        dec = uasn1.Decoder()
        dec.start(buf)
        tag, val = dec.read()
        assert val == 1
        tag, val = dec.read()
        assert val == 2
        assert dec.eof()

    def test_skip_primitive(self):
        buf = b'\x02\x01\x01\x02\x01\x02'
        dec = uasn1.Decoder()
        dec.start(buf)
        dec.read()
        tag, val = dec.read()
        assert val == 2
        assert dec.eof()

    def test_skip_constructed(self):
        buf = b'\x30\x06\x02\x01\x01\x02\x01\x02\x02\x01\x03'
        dec = uasn1.Decoder()
        dec.start(buf)
        dec.read()
        tag, val = dec.read()
        assert val == 3
        assert dec.eof()
 
    def test_error_init(self):
        dec = uasn1.Decoder()
        assert_raises(uasn1.Error, dec.peek)
        assert_raises(uasn1.Error, dec.read)
        assert_raises(uasn1.Error, dec.enter)
        assert_raises(uasn1.Error, dec.leave)

    def test_error_stack(self):
        buf = b'\x30\x08\x02\x01\x01\x04\x03foo'
        dec = uasn1.Decoder()
        dec.start(buf)
        assert_raises(uasn1.Error, dec.leave)
        dec.enter()
        dec.leave()
        assert_raises(uasn1.Error, dec.leave)

    def test_no_input(self):
        dec = uasn1.Decoder()
        dec.start('')
        tag = dec.peek()
        assert tag is None

    def test_error_missing_tag_bytes(self):
        buf = b'\x3f'
        dec = uasn1.Decoder()
        dec.start(buf)
        assert_raises(uasn1.Error, dec.peek)
        buf = b'\x3f\x83'
        dec.start(buf)
        assert_raises(uasn1.Error, dec.peek)

    def test_error_no_length_bytes(self):
        buf = b'\x02'
        dec = uasn1.Decoder()
        dec.start(buf)
        assert_raises(uasn1.Error, dec.read)

    def test_error_missing_length_bytes(self):
        buf = b'\x04\x82\xff'
        dec = uasn1.Decoder()
        dec.start(buf)
        assert_raises(uasn1.Error, dec.read)

    def test_error_too_many_length_bytes(self):
        buf = b'\x04\xff' + b'\xff' * 0x7f
        dec = uasn1.Decoder()
        dec.start(buf)
        assert_raises(uasn1.Error, dec.read)

    def test_error_no_value_bytes(self):
        buf = b'\x02\x01'
        dec = uasn1.Decoder()
        dec.start(buf)
        assert_raises(uasn1.Error, dec.read)

    def test_error_missing_value_bytes(self):
        buf = b'\x02\x02\x01'
        dec = uasn1.Decoder()
        dec.start(buf)
        assert_raises(uasn1.Error, dec.read)

    def test_error_non_normalized_positive_integer(self):
        buf = b'\x02\x02\x00\x01'
        dec = uasn1.Decoder()
        dec.start(buf)
        assert_raises(uasn1.Error, dec.read)

    def test_error_non_normalized_negative_integer(self):
        buf = b'\x02\x02\xff\x80'
        dec = uasn1.Decoder()
        dec.start(buf)
        assert_raises(uasn1.Error, dec.read)

    def test_error_non_normalised_object_identifier(self):
        buf = b'\x06\x02\x80\x01'
        dec = uasn1.Decoder()
        dec.start(buf)
        assert_raises(uasn1.Error, dec.read)

    def test_error_object_identifier_with_too_large_first_component(self):
        buf = b'\x06\x02\x8c\x40'
        dec = uasn1.Decoder()
        dec.start(buf)
        assert_raises(uasn1.Error, dec.read)
