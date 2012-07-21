# -*- coding: utf-8 -*-
#
# File: seqrecord.py
#
# Copyright (c) 2010 by Mauro Amico (Biodec Srl)
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# @version $Revision$:
# @author  $Author$:
# @date    $Date$:

__author__ = '''Mauro Amico <mauro@biodec.com>'''
__docformat__ = 'plaintext'

import sys
import re

from zope.interface import implements

from AccessControl import ClassSecurityInfo

from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema

from Products.Archetypes import atapi

# biopython
from Bio.Seq import Seq as BioSeq
from Bio.SeqRecord import SeqRecord as BioSeqRecord

# plone4bio
# from plone4bio.base import Plone4BioMessageFactory as _
from plone4bio.base.interfaces import ISeqRecord   #, ISeqRecordProxy, ISeqProxy

import logging
logger = logging.getLogger('plone4bio')


SeqRecordSchema = ATContentTypeSchema.copy() + atapi.Schema((
    atapi.TextField("sequence",
        required=True,
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
        widget=atapi.TextAreaWidget(
            label="sequence",
            label_msgid="sequence_label",
            description="Sequence",
            description_msgid="sequence_help",
            i18n_domain="plone4bio")
    ),
    atapi.StringField("alphabet",
        required=True,
        enforceVocabulary=True,
        vocabulary=["Bio.Alphabet.ProteinAlphabet",
            "Bio.Alphabet.IUPAC.ExtendedIUPACProtein",
            "Bio.Alphabet.IUPAC.IUPACProtein",
        ],
        widget=atapi.SelectionWidget(
            label="alphabet",
            label_msgid="alphabet_label",
            description="Alphabet",
            description_msgid="alphabet_help",
            i18n_domain="plone4bio")
    ),
    # TODO: custom widget
    atapi.StringField("dbxrefs",
        required=False,
        widget=atapi.LinesWidget(
            label="dbxrefs",
            label_msgid="dbxrefs_label",
            description="Database cross references",
            description_msgid="dbxrefs_help",
            i18n_domain="plone4bio")
    ),
    ))


class SeqRecord(ATCTContent):
    portal_type='SeqRecord'

    implements(ISeqRecord)

    security = ClassSecurityInfo()
    schema = SeqRecordSchema
    _at_rename_after_creation = True

    # TODO:
    annotations = {}
    features = []

    # TODO: remove from here !!!!
    def Sequences(self):
        '''
        It tries to manage the storage of multiple sequences inside
        the seqrecord. It is able to manage 2 types of multiple sequence:
         - based on annotation-key: if in annotation key there is a key
           named multiple-sequences, and the key is a list of string, one for
           each sequence, where each string is of the type "label:start:end".
             - "label" that is the label of the sequence used also for
               the structure section (where the label is the chain)
             - "start" and "end" that are respectively the start and end
               position of each sequence inside the global sequence.
         - based on separator (a separator inside the sequence is used to
           separate the different sequences). It will use one of these
           three separators: "#", ",", ";"
        It returns a list of tuple, where each tuple is a 'label' and
        a seq object (Bio.Seq.Seq instance).
        '''
        ##start to split on multiple-sequence annotation key
        seq = self.seqrecord.seq
        seq_list = []
        if self.annotations.has_key('multiple-sequences'):
               for label_start_end in self.annotations['multiple-sequences']:
                        label,start,end = label_start_end.split(':')
                        subseq = BioSeq(seq.data[int(start):int(end)], alphabet = seq.alphabet)
                        seq_list.append((label, subseq))
        else:
                listsep = ['#',',',';']
                separator = ''
                for sep in listsep:
                        if seq.data.rfind(sep):  separator = sep
                if separator:
                        seqs = seq.data.split(separator)
                        for seqdata in seqs:
                                ## if separator is multiple... exclude '' objects
                                if seqdata:
                                      subseq = BioSeq(seqdata, alphabet = seq.alphabet)
                                      seq_list.append(('',subseq))
        ## if it didn't do any kind o split... return the whole seq
        if not seq_list: seq_list.append(('',seq))
        return seq_list

    def __init__(self, *args, **kw):
        super(SeqRecord, self).__init__(*args, **kw)
        if 'seqrecord' in kw:
            seqr = kw['seqrecord']
            self.setId(seqr.id)
            self.setSequence(str(seqr.seq))
            self.setAlphabet(str(seqr.seq.alphabet.__class__))
            self.setTitle(seqr.name)
            self.setDescription(seqr.description)
            self.annotations = seqr.annotations
            self.features = seqr.features
            self.dbxrefs = seqr.dbxrefs

    def Accession(self):
        return self.id

    def Name(self):
        return self.title

    def GeneIdentifier(self):
        if self.annotations.has_key('gi'):
            return self.annotations['gi']
        else:
            return None

    # override this function on different implementation (e.g. biosql)
    def getSeqRecord(self):
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
        seqr = BioSeqRecord(id=self.Accession(),
                            seq=BioSeq(self.Sequence(), self.alphabetClass()()),
                            name=self.Name(),
                            description=self.Description())
        seqr.features = self.features
        seqr.annotations = self.annotations
        return seqr

    @property
    def seqrecord(self):
        return self.getSeqRecord()

    #TODO: this is a hack
    def setAlphabet(self, value):
        """
            "<class 'Bio.Alphabet.ProteinAlphabet'>" 
                => "Bio.Alphabet.ProteinAlphabet"
        """
        value = re.sub('<class \'(.*)\'>', '\g<1>', value)
        self.getField('alphabet').set(self, value)

    def alphabetClass(self):
        alphabet = self.getAlphabet()
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

    def Sequence(self):
        return self.getSequence()

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

# seqRecordFactory = Factory(SeqRecord, title=_(u"Create a new SeqRecord"))

atapi.registerType(SeqRecord, 'plone4bio.base')
