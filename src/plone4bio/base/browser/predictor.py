import Acquisition

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import Batch
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.component import createObject
from zope.formlib import form
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

from plone.app.form import base

from plone4bio.base import Plone4BioMessageFactory as _
from plone4bio.base.browser.seqrecord import SeqRecordAddForm
from plone4bio.base.content.seqrecord import SeqRecord
from plone4bio.base.interfaces import ISeqRecord

class PredictorsView(BrowserView):
    """ """

    def can_predict(self):
        context = Acquisition.aq_inner(self.context)
        if not context.displayContentsTab():
            return False
        return ISeqRecord.providedBy(context)

