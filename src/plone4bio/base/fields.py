import re
from zope.schema import Choice
from zope.schema import Text

class TextWORM(Text):
    """ Write Once Read Many"""    
    def __init__(self, *args, **kw):
        super(TextWORM, self).__init__(*args, **kw)
    def _getReadonly(self):
        return self.context
    def _setReadonly(self, value):
        pass
    readonly = property(fget=_getReadonly, fset=_setReadonly)   

class ChoiceWORM(Choice):
    """ Write Once Read Many"""    
    def __init__(self, *args, **kw):
        super(ChoiceWORM, self).__init__(*args, **kw)
    def _getReadonly(self):
        return self.context
    def _setReadonly(self, value):
        pass
    readonly = property(fget=_getReadonly, fset=_setReadonly)   

class Sequence(TextWORM):
    """ """

    def set(self, object, value):
        #TODO: use biopython, manage alphabet
        value = re.compile('[^A-Z]').sub('', value.upper())
        super(Sequence, self).set(object, value)

