from zope.interface import Interface
from zope import schema

from plone4bio.base import Plone4BioMessageFactory as _
from plone4bio.base import fields

class ISeqProxy(Interface):
    #TODO: readonly attribute doesn't work !!!! (????)
    data = schema.Text(title=_(u"Sequence"),
                               description=_(u"The sequence"),
                               required=True,
                               readonly=True)

class ISeqRecordProxy(Interface):
    name = schema.TextLine(title=_(u"Name"),
                            description=_(u"Name of the sequence"),
                            required=True)
    id = schema.TextLine(title=_(u"identifier"), required=True)
    accession = schema.TextLine(title=_(u"accession"), required=True)
    #TODO: readonly attribute doesn't work !!!! (????)
    seq = schema.Object(title=_(u"Sequence"),
                               description=_(u"Sequence"),
                               schema = ISeqProxy,
                               readonly=True)

class ISeqRecord(Interface):
    """ Biopython's SeqRecord ... Plone4Bio
    seqrecord = schema.Object(title=_(u"SeqRecord"),
                               description=_(u"SeqRecord"),
                               schema = ISeqRecordProxy)
    """
    # TODO: custom fields/widgets/validators
    title = schema.TextLine(title=_(u"name"), required=True, default=u'')
    description = schema.Text(title=_(u"Description"))
    # accession = schema.TextLine(title=_(u"accession"), required=True, default=u'')
    sequence = fields.Sequence(title=_(u"Sequence"), 
                           description=_(u"The sequence"),
                           required=True,
                           default=u'')
    # TODO: vocabulary
    alphabet = fields.ChoiceWORM(title=_(u"Alphabet"), values = ["Bio.Alphabet.ProteinAlphabet",
                                                             "Bio.Alphabet.IUPAC.ExtendedIUPACProtein",
                                                             "Bio.Alphabet.IUPAC.IUPACProtein",
                                                             ])
    dbxrefs = schema.List(title=_(u"Dbxrefs"), value_type=schema.TextLine(title=_(u"dbxref")))
    #TODO: annotation value will be also a list ...
    #TODO: there is no default widget for Dict
    #annotations = schema.Dict(title=_(u"Annotations"),
    #                          key_type=schema.TextLine(title=_(u"key")),
    #                          value_type=schema.TextLine(title=_(u"value")))

class ISeqRecordContainer(Interface):
    """ """

class IPredictor(Interface):
    """ """

class IPredictorTool(Interface):
    """ """
