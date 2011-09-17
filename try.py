from hid import hid, hid_enumerate
import time

for i in hid_enumerate():
    print i
    
h = Hid(0x461, 0x20)

h.set_nonblocking(1)

for k in range(100):
    for i in [0, 1]:
        for j in [0, 1]:
            h.write([0, i, j])
            d = h.read(5)
            if d:
                print d
            time.sleep(0.05)



