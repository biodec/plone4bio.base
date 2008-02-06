__author__ = '''Mauro Amico <m@biodec.com>'''
__docformat__ = 'plaintext'

import sys

from zope.interface import implements
from zope.component.factory import Factory

from plone.locking.interfaces import ITTWLockable
from plone.app.content.interfaces import INameFromTitle
from plone.app.content.container import Container
from plone.memoize.instance import memoize

from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName
from OFS.OrderSupport import OrderSupport

# biopython
from Bio.Seq import Seq

# plone4bio
from plone4bio.base import Plone4BioMessageFactory as _
from plone4bio.base.interfaces import ISequence
from plone4bio.base.interfaces import IGenericPrediction

import re

import logging
logger = logging.getLogger('plone4bio')

class Sequence(OrderSupport, Container):
    """ """
    implements(ISequence, ITTWLockable, INameFromTitle)
    portal_type='Sequence'
    
    title = u""
    description = u""
    sequence = u""
    
    # @memoize
    def getSeqObj(self):
        s = re.compile('[^A-Za-z]').sub('',self.sequence).upper()
        return Seq(s)

    # @memoize
    def getSequenceRaw(self):
        return self.getSeqObj().tostring()
    
    # @memoize
    def getSequenceTxt(self, wordwrap=40, sep='\n'):
        # import pdb; pdb.set_trace()
        seq = self.getSeqObj().tostring()
        if (wordwrap > 0):
            if len(seq) <= wordwrap:
                stringseq = seq
            else:
                stringseq = u''
                for i in range(0,len(seq),wordwrap):
                    stringseq += seq[i:i+wordwrap]+sep
        else:
            stringseq = seq
        return stringseq

    def getPredictions(self):
        # import pdb;   pdb.set_trace()
        p = []
        for o in self.getFolderContents(full_objects=True):
            if IGenericPrediction.providedBy(o):
                p.append(o)
        return p
    
    def havePrediction(self, name, dict):
        """Return ...
                TODO: utilizzare una maniera piu' elegante e efficace 
                per cercare all'interno del folder/sequenza
        """
        # import pdb;   pdb.set_trace()
        try:
            predictions_done = self.getPredictions()
            for d in predictions_done:
                if d.getPredname() == name:
                    if not dict.has_key('database'):
                        return True
                    else:
                        if d.getDatabase() == dict['database']:
                            return True
        finally:
            return False

sequenceFactory = Factory(Sequence, title=_(u"Create a new sequence"))