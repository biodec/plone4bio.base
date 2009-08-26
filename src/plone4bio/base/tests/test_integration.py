import unittest
from Testing import ZopeTestCase as ztc
from plone4bio.base.tests.base import BaseTestCase


def test_suite():
    return unittest.TestSuite([
        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
                'README.txt', package='plone4bio.base',
                test_class=BaseTestCase),
        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
