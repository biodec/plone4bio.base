# -*- coding: utf-8 -*-
#
# File: __init__.py
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

from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from zope.schema import Object
from zope.schema import List
from zope.schema import TextLine

from zope.formlib.form import FormFields
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import ObjectWidget
from zope.app.form.browser import TextWidget
from zope.app.form.browser import ListSequenceWidget
from zope.app.container.ordered import OrderedContainer
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from plone.app.controlpanel.form import ControlPanelForm
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName

# from plone4bio.base.interfaces import IPlone4BioConfiguration
from plone4bio.base.tool.dbxref import DbxrefPattern
from plone4bio.base.interfaces import IDbxrefPattern
from plone4bio.base import Plone4BioMessageFactory as _

"""
class LongTextWidget(TextWidget):
    displayWidth = 60
    def __call__(self):
        TextWidget.__call__(self)
"""      
        
class IPlone4BioConfigurationSchema(Interface):    
    dbxref_patterns = List(
        title=u'Dbxref patterns',
        description=_(u'help_dbxref_patterns',
        ),
        value_type=Object(IDbxrefPattern, title=u"dbxref pattern")
    )

"""
class Plone4BioConfiguration(OrderedContainer):
    implements(IPlone4BioConfiguration)
"""

class DbxrefPatternWidgetView:
    template = ViewPageTemplateFile('dbxrefpattern.pt')
    def __init__(self, context, request):
        self.context = context
        self.request = request
    def __call__(self):
        return self.template()

class _DbxrefPatternWidget(ObjectWidget):
    def __init__(self, context, request, factory, **kw):
        super(_DbxrefPatternWidget, self).__init__(context, request, factory, **kw)
        self.view = DbxrefPatternWidgetView(self, request)


DbxrefPatternsWidget = CustomWidgetFactory(ListSequenceWidget,
    subwidget=CustomWidgetFactory(_DbxrefPatternWidget, DbxrefPattern))


class ControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IPlone4BioConfigurationSchema)
    
    def __init__(self, context):
        super(ControlPanelAdapter, self).__init__(context)
        self.context = getToolByName(context, 'plone4bio_dbxrefpatterns')
    
    dbxref_patterns = ProxyFieldProperty(IPlone4BioConfigurationSchema['dbxref_patterns'])

class Plone4BioControlPanel(ControlPanelForm):
    form_fields = FormFields(IPlone4BioConfigurationSchema)
    form_fields['dbxref_patterns'].custom_widget = DbxrefPatternsWidget
    label = _('Dbxrefs Patterns settings')
    description = _('Dbxrefs Patterns.')
    form_name = _('Dbxrefs Patterns')
