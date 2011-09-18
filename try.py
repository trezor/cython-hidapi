import hid
import time

print hid.enumerate(0, 0)

h = hid.device(0x461, 0x20)

print h.get_manufacturer_string()
print h.get_product_string()
print h.get_serial_number_string()

h.set_nonblocking(1)

for k in range(10):
    for i in [0, 1]:
        for j in [0, 1]:
            h.write([0x80, i, j])
            d = h.read(5)
            if d:
                print d
            time.sleep(0.05)



