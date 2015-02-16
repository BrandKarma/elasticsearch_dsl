from __future__ import with_statement

import unittest

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_dummy(self):
        self.assertEqual(1, 1)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicTestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
