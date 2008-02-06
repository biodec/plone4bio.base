from zope.interface import Interface, Invalid, invariant, implements
from zope.component.interfaces import IObjectEvent
from zope import schema
from zope.app.container.constraints import containers, contains
from plone.app.vocabularies.users import UsersSource

from plone4bio.base import Plone4BioMessageFactory as _

class IGenericPrediction(Interface):
    """ """
    # containers('Producst.plone4bio.interfaces.ISequence')
        
class IPredictionState(Interface):
    """ """ 
    state = schema.TextLine(title=_(u"State"), required=True)
    
class ISequence(Interface):
    """ Sequence 
    """
    title = schema.TextLine(title=_(u"Title"),
                            description=_(u"Title of the sequence"),
                            required=True)
                            
    description = schema.Text(title=_(u"Description"),
                              description=_(u"A short description of the sequence"),
                              required=False)
                        
    sequence = schema.Text(title=_(u"Sequence"),
                               description=_(u"The sequence"),
                               required=True)
