from zope.publisher.interfaces import IRequest
from zope.publisher.browser import BrowserPage
from zope.interface import implementer
from zope.component import adapter
from zope.component import getMultiAdapter

from Products.Five import BrowserView

from plone4bio.base.interfaces import ISeqRecord
from plone4bio.base.png.interfaces import IPNGPresentation
from plone4bio.base.png.interfaces import IImagemapPresentation

from StringIO import StringIO

# BioPerl
import subprocess
import os
from Bio import SeqIO

class PNGFeaturesView(BrowserPage):
    def __call__(self):
        response = self.request.response
        response.setHeader('Pragma', 'no-cache')
        response.setHeader('Content-Type', 'image/png')
        return getMultiAdapter((self.context, self.request), IPNGPresentation)

class ImagemapFeaturesView(BrowserView):
    def __call__(self):
        return getMultiAdapter((self.context, self.request), IImagemapPresentation)

# TODO: refactoring with genometools (?)
@adapter(ISeqRecord, IRequest)
@implementer(IImagemapPresentation)
def seqrecordImagemap(context, request):
    perlpath = os.sep.join((os.path.dirname(__file__), "perl"))
    cmd = ["perl", "-I"+ perlpath, os.sep.join((perlpath, "graphics-imagemap-cmd.pl")), "-"]
    graphics = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    # FIXME: XXX
    context.Description()
    genbank=StringIO()
    SeqIO.write([context.seqrecord, ], genbank, "genbank")
    (stdoutdata, stderrdata) = graphics.communicate(genbank.getvalue())
    return stdoutdata

# TODO: refactoring with genometools (?)
@adapter(ISeqRecord, IRequest)
@implementer(IPNGPresentation)
def seqrecordPNG(context, request):
    # prediction.getDataCharts() = [{'chart':(line,bar,...),'data':[(x,y),(x,y),...}, ...]

    # BioPerl
    perlpath = os.sep.join((os.path.dirname(__file__), "perl"))
    cmd = ["perl", "-I"+ perlpath, os.sep.join((perlpath, "graphics-cmd.pl")), "-"]
    graphics = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    # FIXME: XXX
    context.Description()
    genbank=StringIO()
    SeqIO.write([context.seqrecord, ], genbank, "genbank")
    (stdoutdata, stderrdata) = graphics.communicate(genbank.getvalue())
    return stdoutdata
