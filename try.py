import hid
import time

for d in hid.enumerate(0, 0):
    keys = d.keys()
    keys.sort()
    for key in keys:
        print "%s : %s" % (key, d[key])
    print ""

print "Opening device"
#h = hid.device(0x461, 0x20)
h = hid.device(0x1941, 0x8021)

if h:

    print "Manufacturer: %s" % h.get_manufacturer_string()
    print "Product: %s" % h.get_product_string()
    print "Serial No: %s" % h.get_serial_number_string()

    # try no-blocking mode by uncommenting this line
    #h.set_nonblocking(1)

    # try writing some data to the device by uncommenting this line
    #for k in range(10):
    #    for i in [0, 1]:
    #        for j in [0, 1]:
    #            h.write([0x80, i, j])
    #            d = h.read(5)
    #            if d:
    #                print d
    #            time.sleep(0.05)

    print "Closing device"
    h.close()

else:
    print "Hard coded test hid could not be opened, update this script with one"
    print "from the enumeration list output and try again."

print "Done"




