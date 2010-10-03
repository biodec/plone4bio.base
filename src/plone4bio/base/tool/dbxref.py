# -*- coding: utf-8 -*-
#
# File: dbxref.py
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
# @version $Revision: $:
# @author  $Author: $:
# @date    $Date: $:

from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.permissions import ManagePortal, View

from OFS.SimpleItem import SimpleItem
from zope.interface import implements

from plone4bio.base.interfaces import IDbxrefPatternsTool
from plone4bio.base.interfaces import IDbxrefPattern


class DbxrefPattern:
    implements(IDbxrefPattern)
    def __init__(self, name='', pattern=''):
        self.name = name
        self.pattern = pattern


class DbxrefPatternsTool(UniqueObject, SimpleItem):
    implements(IDbxrefPatternsTool)
    id = 'plone4bio_dbxrefpatterns'
    meta_type = id.title().replace('_', ' ')
    isPrincipiaFolderish = 1 # Show up in the ZMI
    security = ClassSecurityInfo()
    security.declareObjectProtected(View)
    dbxref_patterns = []

