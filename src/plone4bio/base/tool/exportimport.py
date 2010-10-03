from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.utils import _resolveDottedName
from Products.GenericSetup.utils import _getDottedName

from Products.CMFCore.utils import getToolByName

from plone4bio.base.interfaces import IPredictorTool
from plone4bio.base.interfaces import IDbxrefPatternsTool
from plone4bio.base.tool.dbxref import DbxrefPattern


class DbxrefPatternsToolXMLAdapter(XMLAdapterBase):
    __used_for__ = IDbxrefPatternsTool
    _LOGGER_ID = 'plone4bio_dbxrefpatterns'

    def _exportNode(self):
        """Export the object as a DOM node"""
        root = self._doc.createElement('plone4bio')
        child = self._doc.createElement('dbxrefpatterns')
        for p in getattr(self.context, 'dbxrefs_patterns', []):            
            node = self._doc.createElement('pattern')
            node.setAttribute('name', p.name)
            node.appendChild(self._doc.createTextNode(p.pattern))
            child.appendChild(node)        
        root.appendChild(child)
        self._logger.info('Plone4Bio dbxref patterns tool exported.')
        return root

    def _importNode(self, node):
        """Import the object from the DOM node"""
        if self.environ.shouldPurge():
            self.context.dbxref_patterns = []
            self._logger.info('Plone4Bio dbxref patterns tool purged.')
        # BBB: manage as dict
        dbxref_patterns = {} 
        for child in node.childNodes:
            if child.nodeName == 'dbxrefpatterns':
                for pnode in child.childNodes:
                    if pnode.nodeName == 'pattern':
                        dbxref_patterns[pnode.getAttribute('name')] = '\n'.join([n.toxml() for n in pnode.childNodes])
        dbxref_patterns.update(dict([(p.name, p.pattern) 
                for p in self.context.dbxref_patterns]))
        self.context.dbxref_patterns = [DbxrefPattern(name, pattern) for (name, pattern) in dbxref_patterns.items()]
        self._logger.info('Plone4Bio dbxref patterns tool imported.')

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

def importSettings(context):
    """Import tool settings from an XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, 'plone4bio_predictors', None)
    if tool:
        importObjects(tool, '', context)
    tool = getToolByName(site, 'plone4bio_dbxrefpatterns', None)
    if tool:
        importObjects(tool, '', context)

def exportSettings(context):
    """Export tool settings as an XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, 'plone4bio_predictors', None)
    if tool:
        exportObjects(tool, '', context)
    tool = getToolByName(site, 'plone4bio_dbxrefpatterns', None)
    if tool:
        exportObjects(tool, '', context)


