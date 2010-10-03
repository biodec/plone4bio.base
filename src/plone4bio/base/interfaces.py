# -*- coding: utf-8 -*-
#
# File: interfaces.py
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

from zope.interface import Interface
from zope.schema import TextLine


class ISeqRecord(Interface):
    """ """


class ISeqRecordUploader(Interface):
    """ """
    def loadData(self, data, data_type):
        """ """


class ISeqRecordContainer(Interface):
    """ """


class IPredictor(Interface):
    """ """


#TODO: remove
class IPlone4BioConfiguration(Interface):
    """ """


class IPredictorTool(Interface):
    """ """
    
    
class IDbxrefPatternsTool(Interface):
    """ """
    
class IDbxrefPattern(Interface):
    """ """
    name = TextLine(title=u"name")
    pattern = TextLine(title=u"pattern")


