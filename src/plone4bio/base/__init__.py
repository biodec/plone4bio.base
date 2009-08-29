from zope.i18nmessageid import MessageFactory
Plone4BioMessageFactory = MessageFactory('plone4bio')

class Plone4BioException(Exception):
    pass

def initialize(context):
    """Intializer called when used as a Zope 2 product."""
