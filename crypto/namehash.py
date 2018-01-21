# Modified version of https://github.com/ConsenSys/ens-namehash-py
import codecs
import functools

import sha3
# Remember to pip3 install pysha3


def is_bytes(value):
    return isinstance(value, (bytes, bytearray))


def combine(f, g):
    return lambda x: f(g(x))


def compose(*functions):
    return functools.reduce(combine, functions, lambda x: x)


def Esha3(value):
    return sha3.keccak_256(value).digest()


# ensure we have the *correct* sha3 installed (keccak)
# assert codecs.encode(sha3(b''), 'hex') == b'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'  # noqa


def _sub_hash(value, label):
    return Esha3(value + Esha3(label))


def namehash(name, encoding=None):
    """
    Implementation of the namehash algorithm from EIP137.
    """
    node = b'\x00' * 32
    if name:
        if encoding is None:
            if is_bytes(name):
                encoded_name = name
            else:
                encoded_name = codecs.encode(name, 'utf8')
        else:
            encoded_name = codecs.encode(name, encoding)

        labels = encoded_name.split(b'.')

        return compose(*(
            functools.partial(_sub_hash, label=label)
            for label
            in labels
        ))(node)
    return node
