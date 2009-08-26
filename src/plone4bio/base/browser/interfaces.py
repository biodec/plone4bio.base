__author__ = """Mauro Amico <amico@biodec.com>"""
__docformat__ = 'plaintext'

from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager


class IBDMSiteForm(IViewletManager):
        """ Marker interface for a Sequence """

class ISequenceView(Interface):
        """ Marker interface for a Sequence """
