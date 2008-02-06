from Acquisition import aq_inner, aq_parent, Explicit

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import Batch
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.component import createObject
from zope.formlib import form
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet

from plone.app.form import base
from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView

from plone4bio.base.interfaces import ISequence
from plone4bio.base.interfaces import IPredictionState
from plone4bio.base import Plone4BioMessageFactory as _

sequence_form_fields = form.Fields(ISequence)

class SequenceView(BrowserView):
    """ """
    pass

class SequenceAddForm(base.AddForm):
    """Add form """
    form_fields = sequence_form_fields
    label = _(u"Add Sequence")
    form_name = _(u"Edit Sequence")
    def create(self, data):
        sequence = createObject(u"plone4bio.base.Sequence")
        form.applyChanges(sequence, self.form_fields, data)
        return sequence

def add_predictions(context, predictors):
    if predictors is None or len(predictors) == 0:
        message = _(u'msg_no_input', default=u'No input provided')
    else:
        for p in predictors:
            newId = context.generateUniqueId(p)
            context.invokeFactory(id=newId, type_name=p,
                title=context.title + ": " + p)
        # TODO ....
        message = _(u'msg_predictions_added', default=u'Predictions added')
    return message

class AddPredictions(BrowserView):
    def __call__(self):
        """Create new predictions
        """
        predictors = self.request.get('predictors', ())
        message = add_predictions(self.context, predictors)
        self.context.plone_utils.addPortalMessage(message)
        response = self.request.response
        here_url = self.context.absolute_url()
        response.redirect(here_url)
        
class SequenceKSSView(PloneKSSView, SequenceView):
    """ """
    
    listing_template = ViewPageTemplateFile('sequence/listing.pt')
    shortchart_template = ViewPageTemplateFile('sequence/shortchart.pt')
    
    @kssaction
    def run_prediction(self, predictionId):
        """ """
        # import pdb;pdb.set_trace()
        context = aq_inner(self.context)
        prediction = context.get(predictionId, None)
        if prediction is None:
            return
        prediction.run()
        state = IPredictionState(prediction)
        ksscore = self.getCommandSet('core')
        # row = ksscore.getHtmlIdSelector('row-prediction-%s' % predictionId)
        # ksscore.replaceHTML(row,'<tr><td>%s</td></tr>' % state.state)
        listing = ksscore.getHtmlIdSelector('predictions-summary')
        html = self.listing_template()
        ksscore.replaceHTML(listing,html)
        chart = ksscore.getHtmlIdSelector('predictions-shortchart')
        html = self.shortchart_template()
        ksscore.replaceInnerHTML(chart,html)
        
