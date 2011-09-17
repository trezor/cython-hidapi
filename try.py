import hid
import time

h = hid.device(0x461, 0x20)

h.set_nonblocking(1)

for k in range(10):
    for i in [0, 1]:
        for j in [0, 1]:
            h.write([0x80, i, j])
            d = h.read(5)
            if d:
                print d
            time.sleep(0.05)



