__author__ = '''Mauro Amico <m@biodec.com>'''
__docformat__ = 'plaintext'

import sys
import copy

from zope.interface import implements
from zope.component import adapts
from zope.component.factory import Factory
from zope.schema.fieldproperty import FieldProperty
# from zope.index.text.interfaces import ISearchableText

from plone.locking.interfaces import ITTWLockable
# from plone.app.content.interfaces import INameFromTitle
from plone.app.content.item import Item
# from plone.memoize.instance import memoize

# from Products.CMFCore.WorkflowCore import WorkflowException
# from Products.CMFCore.utils import getToolByName
# from OFS.OrderSupport import OrderSupport

# biopython
from Bio.Seq import Seq as BioSeq
from Bio.SeqRecord import SeqRecord as BioSeqRecord

# plone4bio
from plone4bio.base import Plone4BioMessageFactory as _
from plone4bio.base.interfaces import ISeqRecord, ISeqRecordProxy, ISeqProxy

import logging
logger = logging.getLogger('plone4bio')

#TODO:
class SeqProxy(BioSeq):
    implements(ISeqProxy)
    def _set_data(self, data):
        self._data = data
    data = property(fget=lambda self: unicode(self._data), fset=_set_data)        
    def __init__(self, data=u''):
        super(SeqProxy, self).__init__(data)
    
#TODO:
class SeqRecordProxy(BioSeqRecord):
    implements(ISeqRecordProxy)
    def __init__(self, seq=None):
        super(SeqRecordProxy, self).__init__(seq)

"""
class SeqRecordSearchableText(object):
    adapts(ISeqRecord)
    implements(ISearchableText)

    def __init__(self, seqrecord):
        self.seqrecord = seqrecord

    def getSearchableText(self):
        return u' '.join(
            unicode(v) for v in self.seqrecord.dbxrefs)
"""

# TODO
class SeqRecord(Item):
    #TODO: move to zcml ???
    implements(ISeqRecord, ITTWLockable) #, INameFromTitle)
    portal_type='SeqRecord'

    # seqrecord = FieldProperty(ISeqRecord['seqrecord'])
    # title = SeqRecordProperty('name', u'')
    title = FieldProperty(ISeqRecord['title'])
    sequence = FieldProperty(ISeqRecord['sequence'])
    alphabet = FieldProperty(ISeqRecord['alphabet'])
    dbxrefs = FieldProperty(ISeqRecord['dbxrefs'])
    # annotations = FieldProperty(ISeqRecord['annotations'])
    annotations = {}
    features = [] # TODO

    def __init__(self, *args, **kwargs):
        import pdb; pdb.set_trace()
        seqrecord = None
        if kwargs.has_key('seqrecord'):
            seqrecord = kwargs['seqrecord']
            del(kwargs['seqrecord'])
        if kwargs.has_key('parent'):
            parent = kwargs['parent']
            del(kwargs['parent'])
        kwargs['title'] = unicode(kwargs.get('title', ''))
        super(SeqRecord, self).__init__(*args, **kwargs)
        if seqrecord:
            self.sequence = unicode(seqrecord.seq.data)
            self.alphabet = "%s.%s" % (seqrecord.seq.alphabet.__class__.__module__, seqrecord.seq.alphabet.__class__.__name__)
            self.features = copy.deepcopy(seqrecord.features)

    def Accession(self):
        return self.id

    def Name(self):
        return self.title

    def GeneIdentifier(self):
        if self.annotations.has_key('gi'):
            return self.annotations['gi']
        else:
            return None

    @property
    def seqrecord(self):
        """
            id
            seq         - The sequence itself (Seq object)
            Additional attributes:
            name        - Sequence name, e.g. gene name (string)
            description - Additional text (string)
            dbxrefs     - List of database cross references (list of 
                          strings)
            features    - Any (sub)features defined (list of 
                          SeqFeature objects)
            annotations - Further information about the whole 
                          sequence (dictionary)
        """
        # from stxnext import pdb;pdb.set_trace()
        seqr = BioSeqRecord(id=self.Accession(),  
                            seq=BioSeq(self.Sequence(), self.alphabetClass()()),
                            name=self.Name(), 
                            description=self.Description())
        seqr.features = self.features
        return seqr

    def alphabetClass(self):
        alphabet = self.alphabet
        __traceback_info__ = alphabet
        parts = alphabet.split( '.' )
        if not parts:
            raise ValueError, "incomplete alphabet name: %s" % alphabet
        parts_copy = parts[:]
        while parts_copy:
            try:
                module = __import__( '.'.join( parts_copy ) )
                break
            except ImportError:
                # Reraise if the import error was caused inside the imported file
                if sys.exc_info()[2].tb_next is not None: raise
                del parts_copy[ -1 ]
                if not parts_copy:
                    return None
        parts = parts[ 1: ] # Funky semantics of __import__'s return value
        obj = module
        for part in parts:
            try:
                obj = getattr( obj, part )
            except AttributeError:
                return None
        return obj

    # override this function on different implementation (e.g. biosql)
    def _getSeqRecord(self):
        """ """
        return self.seqrecord

    """
    @property
    def title(self):
        ## TODO: defire un criterio per generare un Title:
        ## soluzione probabile e' utlizzare i campi accession
        ## e name del seqrecord in cui poter mettere HGNC e/o
        ## codice IPI
        seqrecord =  self.__getSeqRecord__()
        if seqrecord:
            return seqrecord.name
        else:
            return u''
    """
    
    """    
    #TODO: ???    
    def Title(self):
        return self.title
    """

    def Sequence(self):
        return self.sequence
        
    """

    def SeqId(self):
        return self.__getSeqRecord__().id

    def Accession(self):
        seqrecord =  self.__getSeqRecord__()
        if seqrecord:
            return seqrecord.id
        else:
            return u''

    def Name(self):
        seqrecord =  self.__getSeqRecord__()
        if seqrecord:
            return seqrecord.name
        else:
            return u''
    
    def gi(self):
        return self.Id()

    
    def features(self):
        seqrecord =  self.__getSeqRecord__()
        if seqrecord:
            return seqrecord.features
        else:
            return []
    """

    #TODO: check
    def features_dict(self):
        """
        Return a Dictionary of features, surtable to be
        represented in a clusterized way.
        Each cluster is composed by feature with the same:
              - ft_accession
              - ft_type
        """
        features = self.features
        features_dict = {}
        for f in features:
            clustkey = ''
            subclustkey = ''
            if f.type:
                clustkey = f.type
                subclustkey += f.type + '_'
            if f.qualifiers.has_key('ft_accession'):
                subclustkey += f.qualifiers['ft_accession'][0]
            if not features_dict.has_key(clustkey):
                features_dict[clustkey] = {}
            if features_dict[clustkey].has_key(subclustkey):
                features_dict[clustkey][subclustkey].append(f)
            else:
                features_dict[clustkey][subclustkey] = [f]
        return features_dict

    #TODO: check
    def SeqStatistics(self, type=''):
        return dict(
                    Length=0,
                    )
        alphabet = ''
        if type:
            if type.lower() == 'protein':
                alphabet = 'ACDEFGHIKLMNPQRSTVWYBXZJUO'
            elif type.lower() in ('dna', 'rna', 'nucleotide'):
                alphabet = 'CGATU' 
        seq = self.Sequence()
        if not alphabet:
            if 'DNA' in str(seq.alphabet) or 'RNA' in str(seq.alphabet) or 'Nucleotide' in str(seq.alphabet):
                alphabet = 'CGATU'
            elif 'Protein' in str(seq.alphabet):
                alphabet = 'ACDEFGHIKLMNPQRSTVWYBXZJUO'     
        seqstat = {}
    
        ## Length
        seqstat['Length'] = len(seq.data)
    
        ## Composition
        if alphabet:
            composition = {}
            for l in alphabet:
                count = seq.data.count(l)
                if count > 0:
                    composition[l] = l + ': ' + str(count) + ' -  ' + str(round((count*100.0)/seqstat['Length'],2)) + '%'
            seqstat['Composition'] = composition
        return seqstat

    #TODO: check
    def annotation_sequences(self, proteintags=[]):
        """
        Return the protein sequences that are in the annotation
        dictionary. Return them as a dictionary. The dictionary keys
            are the annotation keys and their value are the sequences.
            The annotation tags that contains protein can be passed
        as a list of tags. 
        """
        annotations = self.annotations()
        if not proteintags:
            proteintags = ['vega_calculated_protein',
                           'ncbi_cds_translated_protein',
                           'ensembl_translated_protein',
                           'ncbi_cds_calculated_protein',
                           'ensembl_calculated_protein',
                   'uniprot_sequence']
        annotation_sequences = {}
        for t in proteintags:
            if annotations.has_key(t):
                annotation_sequences[t] = annotations[t]
        return annotation_sequences

    """
    def dbxrefs(self):
        seqrecord =  self.__getSeqRecord__()
        if seqrecord:
            return seqrecord.dbxrefs
        else:
            return []

    def annotations(self):
        seqrecord =  self.__getSeqRecord__()
        if seqrecord:
            return seqrecord.annotations
        else:
            return {}
    """

seqRecordFactory = Factory(SeqRecord, title=_(u"Create a new SeqRecord"))
