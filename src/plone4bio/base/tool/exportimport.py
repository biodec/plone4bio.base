from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.utils import _resolveDottedName
from Products.GenericSetup.utils import _getDottedName

from Products.CMFCore.utils import getToolByName

from plone4bio.base.interfaces import IPredictorTool

class PredictorToolXMLAdapter(XMLAdapterBase):
    __used_for__ = IPredictorTool
    _LOGGER_ID = 'plone4bio_predictors'
    name = 'plone4bio_predictors'
    boolean_fields =  [ ]
    list_fields = [ ]

    def _exportNode(self):
        """Export the object as a DOM node"""
        node = self._doc.createElement('plone4bio')
        fragment = self._doc.createDocumentFragment()

        child = self._doc.createElement('predictors')
        child.appendChild(self._extractPredictors())
        self._logger.info('Predictors exported.')
        fragment.appendChild(child)

        self._logger.info('Plone4Bio predictors tool exported.')
        return node

    def _importNode(self, node):
        """Import the object from the DOM node"""
        if self.environ.shouldPurge():
            self._purgePredictors()
            self._logger.info('Predictors purged.')

        for child in node.childNodes:
            if child.nodeName == 'predictors':
                self._initPredictors(child)
                self._logger.info('Predictors registered.')

        self._logger.info('Plone4Bio predictors tool imported.')

    def _purgePredictors(self):
        self._logger.warning('##TODO## Plone4Bio purge predictors.')

    def _initPredictors(self, node):
        for child in node.childNodes:
            if child.nodeName != 'predictor':
                continue
            self._logger.warning('##TODO## Plone4Bio import predictors.')
            klass = _resolveDottedName(child.getAttribute('class'))
            name = unicode(str(child.getAttribute('name')))
            self.context.registerPredictor(klass())

    def _extractPredictors(self):
        """ """
        fragment = self._doc.createDocumentFragment()
        for pred in self.context.listPredictors():
            fragment.appendChild(self._extractPredictorNode(pred))
        return fragment

    def _extractPredictorNode(self, pred):
        """ """
        child = self._doc.createElement('predictor')
        child.setAttribute('class', _getDottedName(pred.__class__))
        child.setAttribute('name', pred.name())
        return child

def importPredictors(context):
    """Import tool settings from an XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, 'plone4bio_predictors', None)
    if tool is None:
        logger = context.getLogger('plone4bio_predictors')
        logger.info('Nothing to import.')
        return
    importObjects(tool, '', context)

def exportPredictors(context):
    """Export tool settings as an XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, 'plone4bio_predictors', None)
    if tool is None:
        logger = context.getLogger('plone4bio_predictors')
        logger.info('Nothing to export.')
        return
    exportObjects(tool, '', context)


