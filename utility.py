def bytearray_to_binary(ba):
  return ' '.join('{0:08b}'.format(c, 'b') for c in ba)

def bytearray_to_int(ba):
  return int.from_bytes(ba, byteorder="big")

def int_to_bytes(n):
  return bytes([n])

def bytes_to_binary(b):
  ' '.join('{0:08b}'.format(c, 'b') for c in b)

def bytes_to_int(b):
  return int.from_bytes(b, byteorder="big")