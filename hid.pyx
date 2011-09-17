cimport chid
cimport cpython.unicode

cdef extern from "stdlib.h":
  void free(void* ptr)
  void* malloc(size_t size)

# def hid_enumerate(vendor_id=0, product_id=0):
#     cdef chid.hid_device_info* infos = chid.hid_enumerate(vendor_id, product_id)
#     res = []
#     cdef chid.hid_device_info* info = infos
#     while info:
#       serial_number = info.serial_number
#       manufacturer_string = info.manufacturer_string
#       product_string = info.product_string
#       res.append({
#         'path': info.path,
#         'vendor_id': info.vendor_id,
#         'product_id': info.product_id,
#         'serial_number': serial_number,
#         'release_number': info.release_number,
#         'manufacturer_string': manufacturer_string,
#         'product_string': product_string,
#         'usage_page': info.usage_page,
#         'interface_number': info.interface_number
#       })
#       info = info.next
#     chid.hid_free_enumeration(infos)
#     return res

cdef class hid:
  cdef chid.hid_device *_c_hid
  def __cinit__(self, vendor_id, product_id):
      self._c_hid = chid.hid_open(vendor_id, product_id, NULL)

  def write(self, buff):
      buff = ''.join(map(chr, buff)) # convert to bytes
      cdef unsigned char* cbuff = buff # covert to c string
      return chid.hid_write(self._c_hid, cbuff, len(buff))

  def set_nonblocking(self, v):
      return chid.hid_set_nonblocking(self._c_hid, v)

  def read(self, max_length):
      cdef unsigned char* cbuff = <unsigned char *>malloc(max_length)
      n = chid.hid_read(self._c_hid, cbuff, max_length)
      res = []
      for i in range(n):
          res.append(cbuff[i])
      free(cbuff)
      return res

  def get_manufacturer_string(self):
      cdef Py_UNICODE* cbuff = <Py_UNICODE*>malloc(100)
      cdef int n = chid.hid_get_manufacturer_string(self._c_hid, cbuff, 100)
      res = cpython.unicode.PyUnicode_FromUnicode(cbuff, n)
      free(cbuff)
      return res
  
