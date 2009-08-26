""" ideas from Products.PortalTransform """
import os
from Globals import package_home
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.permissions import ManagePortal, View
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from OFS.Folder import Folder
# from OFS.SimpleItem import SimpleItem
from zope.interface import implements

from plone4bio.base.predictor import Predictor
from plone4bio.base.interfaces import IPredictor, IPredictorTool
from plone4bio.base import Plone4BioException

_wwwdir = os.path.join(package_home(globals()), 'www')

class PredictorTool(UniqueObject, Folder):
    implements(IPredictorTool)
    id = 'plone4bio_predictors'
    meta_type = id.title().replace('_', ' ')
    isPrincipiaFolderish = 1 # Show up in the ZMI
    security = ClassSecurityInfo()
    security.declareObjectProtected(View)


    #
    #   ZMI
    #
    manage_options =  ( { 'label' : 'Predictors'
                        , 'action' : 'manage_viewPredictors'
                        }
                      ,
                      ) + Folder.manage_options

    def registerPredictor(self, predictor):
        """register a new predictor
        """
        # needed when call from transform.transforms.initialize which
        # register non zope transform
        module = str(predictor.__module__)
        predictor = Predictor(predictor.name(), module, predictor)
        if not IPredictor.providedBy(predictor):
            raise Plone4BioException('%s does not implement IPredictor' % predictor)
        name = predictor.name()
        __traceback_info__ = (name, predictor)
        if name not in self.objectIds():
            self._setObject(name, predictor)
            self._mapPredictor(predictor)

    def _mapPredictor(self, predictor):
        #TODO:
        pass

    #
    #   Accessors
    #
    security.declareProtected(ManagePortal, 'listPredictors')
    def listPredictors(self):

        """ Return a sequence of mappings for predictors
        """
        return self.values()

    def run(self, name, seqr, context=None, **kwargs):
        """run predictor of a given name over a seqrecord

        * name is the name of a registered transform
        """
        try:
            predictor = getattr(self, name)
        except AttributeError:
            raise Exception('No such predictor "%s"' % name)
        seqr = predictor.run(seqr, context=context, **kwargs)
        # self._setMetaData(data, transform)
        return seqr

    def __call__(self, name, seqr, context=None, **kwargs):
        """
        * name is the name of a registered predictor.
        """
        seqr = self.run(name, seqr, context, **kwargs)
        return seqr

    security.declareProtected(ManagePortal, 'manage_viewPredictors')
    manage_viewPredictors = PageTemplateFile('predictionsToolView', _wwwdir)

