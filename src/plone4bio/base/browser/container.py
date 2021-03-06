# -*- coding: utf-8 -*-
#
# File: container.py
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


from datetime import datetime
import Acquisition

from Products.Five import BrowserView

from plone4bio.base import Plone4BioMessageFactory as _
from plone4bio.base.interfaces import ISeqRecordContainer
from plone4bio.base.interfaces import ISeqRecordUploader

# TODO:
def guess_dbtype(filename):
    return "GenBank"

class LoadForm(object): #base.EditForm):
    """Edit form """
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def errors(self):
        form = self.request.form
        if "UPLOAD_SUBMIT" in form:
            filename = getattr(form["field.data"], "filename", None)
            dbtype = form.get("field.dbtype")
            if filename:
                if not dbtype:
                    dbtype = guess_dbtype(filename)[0]
            return self.upload_data(form["field.data"], dbtype)
        return ''

    def upload_data(self, data, dbtype):        
        error = ISeqRecordUploader(self.context).loadData(data, dbtype)
        if error:
            return error
        else:
            return _("Updated ${data} of ${dbtype} on ${date_time}",
                 mapping={'date_time': repr(datetime.utcnow()),
                          'data': repr(data),
                          'dbtype': dbtype})

class DisplayLoadView(BrowserView):
    """Returns True or False depending on whether the upload tab is allowed
    to be displayed on the current context.
    """

    def can_upload(self):
        context = Acquisition.aq_inner(self.context)
        if not context.displayContentsTab():
            return False
        obj = context
        if context.restrictedTraverse('@@plone').isDefaultPageInFolder():
            obj = Acquisition.aq_parent(Acquisition.aq_inner(obj))
        return ISeqRecordContainer.providedBy(obj)

    def upload_url(self):
        context = Acquisition.aq_inner(self.context)
        if context.restrictedTraverse('@@plone').isStructuralFolder():
            url = context.absolute_url()
        else:
            url = Acquisition.aq_parent(context).absolute_url()
        return url + '/@@load'
