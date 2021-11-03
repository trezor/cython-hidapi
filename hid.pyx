import sys
import weakref

from chid cimport *
from libc.stddef cimport wchar_t, size_t

cdef extern from "ctype.h":
    int wcslen(wchar_t*)

cdef extern from "stdlib.h":
    void free(void* ptr)
    void* malloc(size_t size)

cdef extern from *:
    object PyUnicode_FromWideChar(const wchar_t *w, Py_ssize_t size)
    Py_ssize_t PyUnicode_AsWideChar(object unicode, wchar_t *w, Py_ssize_t size)

cdef object U(wchar_t *wcs):
    if wcs == NULL:
        return ''
    cdef int n = wcslen(wcs)
    return PyUnicode_FromWideChar(wcs, n)

def enumerate(int vendor_id=0, int product_id=0):
    """Return a list of discovered HID devices.

    The fields of dict are:

     - 'path'
     - 'vendor_id'
     - 'product_id'
     - 'serial_number'
     - 'release_number'
     - 'manufacturer_string'
     - 'product_string'
     - 'usage_page'
     - 'usage'
     - 'interface_number'

    :param vendor_id: Vendor id to look for, default = 0
    :type vendor_id: int, optional
    :param product_id: Product id to look for, default = 0
    :type product_id: int, optional
    :return: List of device dictionaries
    :rtype: List[Dict]
    """
    cdef hid_device_info* info
    with nogil:
        info = hid_enumerate(vendor_id, product_id)
    cdef hid_device_info* c = info
    res = []
    while c:
        res.append({
            'path': c.path,
            'vendor_id': c.vendor_id,
            'product_id': c.product_id,
            'serial_number': U(c.serial_number),
            'release_number': c.release_number,
            'manufacturer_string': U(c.manufacturer_string),
            'product_string': U(c.product_string),
            'usage_page': c.usage_page,
            'usage': c.usage,
            'interface_number': c.interface_number,
        })
        c = c.next
    hid_free_enumeration(info)
    return res

cdef class _closer:
    """Wrap a hid_device *ptr and a provide a way to call hid_close() on it.

    Used internally for weakref.finalize, which only accepts Python objects.
    """

    cdef hid_device *_ptr

    @staticmethod
    cdef wrap(hid_device *ptr):
        cdef _closer closer = _closer()
        closer._ptr = ptr
        return closer

    def close(self):
        hid_close(self._ptr)

cdef class device:
    """Device class.

    A device instance can be used to read from and write to a HID device.
    """

    cdef hid_device *_c_hid
    cdef object __weakref__  # enable weak-reference support
    cdef object _close

    def open(self, int vendor_id=0, int product_id=0, unicode serial_number=None):
        """Open the connection.

        :param vendor_id: Vendor id to connect to, default = 0
        :type vendor_id: int, optional
        :param product_id: Product id to connect to, default = 0
        :type product_id: int, optional
        :param serial_number:
        :type serial_number: unicode, optional
        :raises IOError:
        """
        cdef wchar_t * cserial_number = NULL
        cdef int serial_len
        cdef Py_ssize_t result
        if self._c_hid != NULL:
            raise RuntimeError('already open')
        try:
            if serial_number is not None:
                serial_len = len(serial_number)
                cserial_number = <wchar_t*>malloc(sizeof(wchar_t) * (serial_len+1))
                if cserial_number == NULL:
                    raise MemoryError()
                result = PyUnicode_AsWideChar(serial_number, cserial_number, serial_len)
                if result == -1:
                    raise ValueError("invalid serial number string")
                cserial_number[serial_len] = 0  # Must explicitly null-terminate
            self._c_hid = hid_open(vendor_id, product_id, cserial_number)
        finally:
            if cserial_number != NULL:
                free(cserial_number)
        if self._c_hid == NULL:
            raise IOError('open failed')
        self._close = weakref.finalize(self, _closer.wrap(self._c_hid).close)

    def open_path(self, bytes path):
        """Open connection by path.

        :param path: Path to device
        :type path: bytes
        :raises IOError:
        """
        cdef char* cbuff = path
        if self._c_hid != NULL:
            raise RuntimeError('already open')
        self._c_hid = hid_open_path(cbuff)
        if self._c_hid == NULL:
            raise IOError('open failed')
        self._close = weakref.finalize(self, _closer.wrap(self._c_hid).close)

    def close(self):
        """Close connection.

        This should always be called after opening a connection.
        """
        if self._c_hid != NULL:
            self._close()
            self._close.detach()
            self._c_hid = NULL

    def write(self, buff):
        """Accept a list of integers (0-255) and send them to the device.

        :param buff: Data to write (must be convertible to `bytes`)
        :type buff: Any
        :return: Write result
        :rtype: int
        """
        if self._c_hid == NULL:
            raise ValueError('not open')
        # convert to bytes
        if sys.version_info < (3, 0):
            buff = ''.join(map(chr, buff))
        else:
            buff = bytes(buff)
        cdef hid_device * c_hid = self._c_hid
        cdef unsigned char* cbuff = buff # covert to c string
        cdef size_t c_buff_len = len(buff)
        cdef int result
        with nogil:
            result = hid_write(c_hid, cbuff, c_buff_len)
        return result

    def set_nonblocking(self, int v):
        """Set the nonblocking flag.

        :param v: Flag value (1 or 0, True or False)
        :type v: int, bool
        :return: Flag result
        :rtype: int
        """
        if self._c_hid == NULL:
            raise ValueError('not open')
        return hid_set_nonblocking(self._c_hid, v)

    def read(self, int max_length, int timeout_ms=0):
        """Return a list of integers (0-255) from the device up to max_length bytes.

        :param max_length: Maximum number of bytes to read
        :type max_length: int
        :param timeout_ms: Number of milliseconds until timeout (default: no timeout)
        :type timeout_ms: int, optional
        :return: Read bytes
        :rtype: List[int]
        """
        if self._c_hid == NULL:
            raise ValueError('not open')
        cdef unsigned char lbuff[16]
        cdef unsigned char* cbuff
        cdef size_t c_max_length = max_length
        cdef int c_timeout_ms = timeout_ms
        cdef hid_device * c_hid = self._c_hid
        try:
            if max_length <= 16:
                cbuff = lbuff
            else:
                cbuff = <unsigned char *>malloc(max_length)
            if timeout_ms > 0:
                with nogil:
                    n = hid_read_timeout(c_hid, cbuff, c_max_length, c_timeout_ms)
            else:
                with nogil:
                    n = hid_read(c_hid, cbuff, c_max_length)
            if n is -1:
                raise IOError('read error')
            res = []
            for i in range(n):
                res.append(cbuff[i])
        finally:
            if max_length > 16:
                free(cbuff)
        return res

    def get_manufacturer_string(self):
        """Return manufacturer string (e.g. vendor name).

        :return:
        :rtype: str
        :raises ValueError: If connection is not opened.
        :raises IOError:
        """
        if self._c_hid == NULL:
            raise ValueError('not open')
        cdef wchar_t buff[255]
        cdef int r = hid_get_manufacturer_string(self._c_hid, buff, 255)
        if r < 0:
            raise IOError('get manufacturer string error')
        return U(buff)


    def get_product_string(self):
        """Return product string (e.g. device description).

        :return:
        :rtype: str
        :raises ValueError: If connection is not opened.
        :raises IOError:
        """
        if self._c_hid == NULL:
            raise ValueError('not open')
        cdef wchar_t buff[255]
        cdef int r = hid_get_product_string(self._c_hid, buff, 255)
        if r < 0:
            raise IOError('get product string error')
        return U(buff)

    def get_serial_number_string(self):
        """Return serial number.

        :return:
        :rtype: str
        :raises ValueError: If connection is not opened.
        :raises IOError:
        """
        if self._c_hid == NULL:
            raise ValueError('not open')
        cdef wchar_t buff[255]
        cdef int r = hid_get_serial_number_string(self._c_hid, buff, 255)
        if r < 0:
            raise IOError('get serial number string error')
        return U(buff)

    def get_indexed_string(self, index):
        """Return indexed string.

        :return:
        :rtype: str
        :raises ValueError: If connection is not opened.
        :raises IOError:
        """
        if self._c_hid == NULL:
            raise ValueError('not open')
        cdef wchar_t buff[255]
        cdef unsigned char c_index = index
        cdef int r = hid_get_indexed_string(self._c_hid, c_index, buff, 255)
        if r < 0:
            raise IOError('get indexed string error')
        return U(buff)

    def send_feature_report(self, buff):
        """Accept a list of integers (0-255) and send them to the device.

        :param buff: Data to send (must be convertible into bytes)
        :type buff: any
        :return: Send result
        :rtype: int
        """
        if self._c_hid == NULL:
            raise ValueError('not open')
        # convert to bytes
        if sys.version_info < (3, 0):
            buff = ''.join(map(chr, buff))
        else:
            buff = bytes(buff)
        cdef hid_device * c_hid = self._c_hid
        cdef unsigned char* cbuff = buff  # covert to c string
        cdef size_t c_buff_len = len(buff)
        cdef int result
        with nogil:
            result = hid_send_feature_report(c_hid, cbuff, c_buff_len)
        return result

    def get_feature_report(self, int report_num, int max_length):
        """Receive feature report.

        :param report_num:
        :type report_num: int
        :param max_length:
        :type max_length: int
        :return: Incoming feature report
        :rtype: List[int]
        :raises ValueError: If connection is not opened.
        :raises IOError:
        """
        if self._c_hid == NULL:
            raise ValueError('not open')
        cdef hid_device * c_hid = self._c_hid
        cdef unsigned char lbuff[16]
        cdef unsigned char* cbuff
        cdef size_t c_max_length = max_length
        cdef int n
        try:
            if max_length <= 16:
                cbuff = lbuff
            else:
                cbuff = <unsigned char *>malloc(max_length)
            cbuff[0] = report_num
            with nogil:
                n = hid_get_feature_report(c_hid, cbuff, c_max_length)
            res = []
            if n < 0:
                raise IOError('read error')
            for i in range(n):
                res.append(cbuff[i])
        finally:
            if max_length > 16:
                free(cbuff)
        return res

    def get_input_report(self, int report_num, int max_length):
        """Get input report

        :param report_num:
        :type report_num: int
        :param max_length:
        :type max_length: int
        :return:
        :rtype: List[int]
        :raises ValueError: If connection is not opened.
        :raises IOError:
        """
        if self._c_hid == NULL:
            raise ValueError('not open')
        cdef hid_device * c_hid = self._c_hid
        cdef unsigned char lbuff[16]
        cdef unsigned char* cbuff
        cdef size_t c_max_length = max_length
        cdef int n
        try:
            if max_length <= 16:
                cbuff = lbuff
            else:
                cbuff = <unsigned char *>malloc(max_length)
            cbuff[0] = report_num
            with nogil:
                n = hid_get_input_report(c_hid, cbuff, c_max_length)
            res = []
            if n < 0:
                raise IOError('read error')
            for i in range(n):
                res.append(cbuff[i])
        finally:
            if max_length > 16:
                free(cbuff)
        return res

    def error(self):
        """Get error from device.

        :return:
        :rtype: str
        :raises ValueError: If connection is not opened.
        :raises IOError:
        """
        if self._c_hid == NULL:
            raise ValueError('not open')
        return U(<wchar_t*>hid_error(self._c_hid))


# Finalize the HIDAPI library *only* once there are no more references to this
# module, and it is being garbage collected.
weakref.finalize(sys.modules[__name__], hid_exit)
