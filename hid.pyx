cimport chid

cdef extern from "stdlib.h":
  void free(void* ptr)
  void* malloc(size_t size)

cdef class device:
  cdef chid.hid_device *_c_hid
  def __cinit__(self, vendor_id, product_id):
      self._c_hid = chid.hid_open(vendor_id, product_id, NULL)

  def write(self, buff):
      '''Accept a list of integers (0-255) and send them to the device'''
      buff = ''.join(map(chr, buff)) # convert to bytes
      cdef unsigned char* cbuff = buff # covert to c string
      return chid.hid_write(self._c_hid, cbuff, len(buff))

  def set_nonblocking(self, v):
      '''Set the nonblocking flag'''
      return chid.hid_set_nonblocking(self._c_hid, v)

  def read(self, max_length):
      '''Return a list of integers (0-255) from the device up to max_length bytes.'''
      cdef unsigned char* cbuff = <unsigned char *>malloc(max_length)
      n = chid.hid_read(self._c_hid, cbuff, max_length)
      res = []
      for i in range(n):
          res.append(cbuff[i])
      free(cbuff)
      return res
