from zope.component import createObject
from zope.formlib import form

from plone.app.form import base
from plone.app.form.widgets.uberselectionwidget import UberMultiSelectionWidget

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone4bio.base.interfaces import IGenericPrediction
from plone4bio.base import Plone4BioMessageFactory as _

generic_form_fields = form.Fields(IGenericPrediction)

class GenericPredictionView(BrowserView):
    """ """
    pass

class GenericPredictionAddForm(base.AddForm):
    """Add form for prediction
    """
    form_fields = generic_form_fields
    label = _(u"Add Generic Prediction")
    form_name = _(u"Edit Generic Prediction")
    def create(self, data):
        prediction = createObject(u"plone4bio.base.GenericPrediction")
        form.applyChanges(prediction, self.form_fields, data)
        return prediction

# TODO: actually unused    
#class ActionForm(viewlet.SimpleAttributeViewlet, formbase.SubPageForm):
#    form_template = formbase.FormBase.template
#    renderForm = formbase.FormBase.render
