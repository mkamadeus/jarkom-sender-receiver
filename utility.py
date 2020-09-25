def bytearray_to_binary(s):
  return ' '.join('{0:08b}'.format(c, 'b') for c in s)