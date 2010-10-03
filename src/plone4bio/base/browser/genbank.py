# -*- coding: utf-8 -*-
#
# File: genbank.py
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

from Products.Five import BrowserView
from StringIO import StringIO
from Bio import SeqIO


class SeqRecord2Genbank(BrowserView):
    """ """
    def __call__(self):
        io = StringIO()
        # FIXME:
        # self.context.Description()
        seqrecord = self.context.getSeqRecord()
        # the maximum length of locus name, for genbak format, is 16
        seqrecord.name = seqrecord.name[:16]
        # features
        for f in seqrecord.features:
            f.type = f.type.replace(" ", "_")
        SeqIO.write([seqrecord, ], io, "genbank")
        return io.getvalue()
