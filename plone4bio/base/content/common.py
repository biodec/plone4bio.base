from zope.interface import implements
from zope.component import adapts

from plone4bio.base.interfaces import IGenericPrediction
from plone4bio.base.interfaces import IPredictionState

from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize

import logging
log = logging.getLogger('plone4bio')

class PredictionState(object):
    implements(IPredictionState)
    adapts(IGenericPrediction)
    
    def __init__(self, context):
        self.context = context
     
    @property
    def state(self):
        return self.workflow().getInfoFor(self.context, 'review_state')
        
    @memoize
    def workflow(self):
        return getToolByName(self.context, 'portal_workflow')