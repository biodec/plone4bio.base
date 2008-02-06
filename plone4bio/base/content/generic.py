__author__ = '''Mauro Amico <m@biodec.com>'''
__docformat__ = 'plaintext'

import sys

from zope.interface import implements
from zope.component.factory import Factory

from plone.locking.interfaces import ITTWLockable
from plone.app.content.interfaces import INameFromTitle
from plone.app.content.item import Item
from plone.memoize.instance import memoize

from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName

from plone4bio.base import Plone4BioMessageFactory as _
from plone4bio.base.interfaces import IGenericPrediction, IPredictionState

import logging
log = logging.getLogger('plone4bio')

class GenericPrediction(Item):
    """ 
    """
    implements(IGenericPrediction, ITTWLockable, INameFromTitle)
    portal_type='Generic Prediction'
    predname = 'generic'
    
    def getPredname(self):
        """ """
        return self.predname

    def getTitle(self):
        """ """
        return self.title
    
    def getState(self):
        """ """
        state = IPredictionState(self)
        return state.state
        # return self.workflow().getInfoFor(self, 'review_state')
    
    def do_prediction(self):
        pass
    
    def run(self):
        """ """
        self.do_prediction()
        self.workflow().doActionFor(self, 'done')
        """
        try:
            self.do_prediction()
            self.workflow().doActionFor(self, 'done')
        except WorkflowException, e:
            # can happen if state changes during execution of this method
            log.warn("Workflow exception caught during prediction sumbission: %s" % str(e))
            self.workflow().doActionFor(self, 'fail')
        except:
            log.warn("Exception caught during prediction sumbission: %s" % str(sys.exc_info()[0]))
            self.workflow().doActionFor(self, 'fail')
        """
            
    def kill(self):
        """ """
        import pdb; pdb.set_trace()
        try:
            self.workflow().doActionFor(self,'kill')
        except WorkflowException, e:
            # can happen if state changes during execution of this method
            log.warn("Exception caught during prediction kill: %s" % str(e))

    def workflow(self):
        return getToolByName(self, 'portal_workflow')

genericPredictionFactory = Factory(GenericPrediction, title=_(u"Create a new generic prediction"))