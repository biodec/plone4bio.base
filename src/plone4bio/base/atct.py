# -*- coding: utf-8 -*-
#
# File: atct.py
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

from zope.interface import implements
from Bio import SeqIO
from plone4bio.base.interfaces import ISeqRecordUploader


class UploadingFileFactory(object):
    implements(ISeqRecordUploader)

    DEFAULT_TYPE = 'genbank'

    def __init__(self, context):
        self.context = context

    def loadData(self, data, data_type=DEFAULT_TYPE):
        if data_type.lower() == 'genbank':
            for seqr in SeqIO.parse(data, "genbank"):
                newid = self.context.invokeFactory('SeqRecord', seqr.id, title=seqr.name)
                obj = getattr(self.context, newid)
                obj.sequence = seqr.seq.tostring()
                obj.alphabet = str(seqr.seq.alphabet.__class__)
                obj.features = seqr.features
                obj.annotations = seqr.annotations
        else:
            raise
