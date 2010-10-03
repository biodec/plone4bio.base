from zope.formlib import form
from zope.component import createObject

from plone.app.form import base
from plone.memoize.view import memoize
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# from plone4bio.base.content.seqrecord import SeqRecordProxy, SeqProxy 
from plone4bio.base.interfaces import ISeqRecord
from plone4bio.base import Plone4BioMessageFactory as _

"""
class SeqRecordWidget(ObjectWidget):
    # TODO: create a CustomSeqWidget
    seq_widget = CustomWidgetFactory(ObjectWidget, SeqProxy)
"""

#TODO: use viewlet
class SeqRecordAnnotationsView(BrowserView):
    """ """
    __call__ = ViewPageTemplateFile('templates/annotations.pt')

#TODO: use viewlet
class SeqRecordFeaturesView(BrowserView):
    """ """
    __call__ = ViewPageTemplateFile('templates/features.pt')

#TODO: use viewlet
class SeqRecordDbxrefsView(BrowserView):
    """ """
    
    @property
    @memoize
    def urldict(self):
        dbxrefpatterns_tool =  getToolByName(self.context, 'plone4bio_dbxrefpatterns')
        if dbxrefpatterns_tool:
            dbxref_patterns = dbxrefpatterns_tool.dbxref_patterns
            return dict([(p.name, p.pattern) for p in dbxref_patterns])
        else:
            # TODO: logger.warning ...
            return {}
    """            
    def __init__(self, *args, **kw):
        super(SeqRecordDbxrefsView, self).__init__(*args, **kw)
        self.dbxrefpatterns_tool =  getToolByName(self.context, 'plone4bio_dbxrefpatterns')
        self.urldict = dict([(p.name, p.pattern) 
                for p in self.dbxrefpatterns_tool.dbxrefs_patterns])
    """
        
    __call__ = ViewPageTemplateFile('templates/dbxrefs.pt')
    
    def getdbxref_url(self, dbxrefdb, key):
        if self.urldict.has_key(dbxrefdb):
                if dbxrefdb == 'Internal':
                        dbid, accessionv = key.split(':')
                        try :
                                accession = accessionv.split('.')[0]
                                seqrecord = self.getSeqRecordFromAccession(accession, dbid)
                                id = seqrecord._primary_id
                                url = '/'.join(self.getURL().split('/')[:-2] + [dbid, str(id)])
                                return url
                        except:
                                return '#'
                if dbxrefdb == 'UniGene':
                        cid = key.split('.')[-1]
                        org = key.split('.')[0]
                        return self.urldict[dbxrefdb] % (org, cid)
                if dbxrefdb == 'Ensemble':
                        dbxrefdb = key[:4]
                if dbxrefdb == 'HGNC':
                        key = key.split(':')[-1]
                        if key.isdigit():  dbxrefdb = 'HGNC_ID'
                        else:  dbxrefdb = 'HGNC_NAME'
                if dbxrefdb == 'HPRD':
                        key = key.split('HPRD_')[-1]
                if dbxrefdb == 'IPI':
                        key = key.split('.')[0]
                ## Othewise
                return self.urldict[dbxrefdb] % key

class SeqRecordView(BrowserView):
    """ """

class SeqRecordPredictors(BrowserView):
    """ """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.tool = getToolByName(self.context, "plone4bio_predictors")

    #@property
    #@memoize
    #def tool(self):
    #    return getToolByName(self.context, "plone4bio_predictors")

    def getPredictors(self):
        return self.tool.values()

    def runPredictor(self):
        self.tool(self.request.form['predictor'], self.context, store=True)

