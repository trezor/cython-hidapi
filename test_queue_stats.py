"""Hardware-free checks; never enumerate or open a device."""
import unittest
import hid
import hidraw


class QueueStatsTests(unittest.TestCase):
    def test_closed_devices(self):
        for backend in (hid, hidraw):
            with self.subTest(backend=backend.__name__):
                device = backend.device()
                with self.assertRaisesRegex(ValueError, "device not open"):
                    device.get_queue_stats()
                device.close()
                with self.assertRaises(ValueError):
                    device.get_queue_stats()


if __name__ == "__main__":
    unittest.main()
