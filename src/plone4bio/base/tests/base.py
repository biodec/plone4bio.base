from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.CMFCore.utils import getToolByName
import plone4bio.base


@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml',
                     plone4bio.base)
    fiveconfigure.debug_mode = False
    ztc.installPackage('plone4bio.base')


class BaseTestCase(ptc.PloneTestCase):
    """Base test case for.
    """

    def afterSetUp(self):
        # Products.plonehrm adds plonehrm.checklist to the Non
        # Installable Products so they do not clutter the QuickInstaller
        # interface.  We need to undo that here or work around it.
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        product = 'plone4bio.base'
        if not qi.isProductInstalled(product):
            qi.installProduct(product)


setup_product()
ptc.setupPloneSite(products=['plone4bio'])
