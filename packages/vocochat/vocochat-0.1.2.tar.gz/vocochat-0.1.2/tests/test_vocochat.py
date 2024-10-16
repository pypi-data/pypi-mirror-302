import unittest
from vocochat.vocochat import VocoChat

class TestVocochat(unittest.TestCase):
    def test_vocochat_class(self):
        voco_chat = VocoChat("Test")
        self.assertEqual(voco_chat.greet(), "Hello, Test!")

if __name__ == '__main__':
    unittest.main()
