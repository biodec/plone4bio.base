from zope.interface import implements
from zope.component import adapts
from zope.filerepresentation.interfaces import IFileFactory
from plone4bio.base.interfaces import ISeqRecordContainer

class UploadingFileFactory(object):
    implements(IFileFactory)
    adapts(ISeqRecordContainer)

    DEFAULT_TYPE = 'GFF File'

    def __init__(self, context):
        self.context = context

    def __call__(self, name, content_type, data):
        import pdb; pdb.set_trace()

    def loadData(self, *args, **kwargs):
        import pdb; pdb.set_trace()

