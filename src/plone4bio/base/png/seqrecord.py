from zope.publisher.interfaces import IRequest
from zope.publisher.browser import BrowserPage
from zope.interface import implementer
from zope.component import adapter
from zope.component import getMultiAdapter

from Products.Five import BrowserView

from plone4bio.base.interfaces import ISeqRecord
from plone4bio.base.png.interfaces import IPNGPresentation
from plone4bio.base.png.interfaces import IImagemapPresentation

from Bio import SeqIO
from cStringIO import StringIO
import logging

logger = logging.getLogger('plone4bio.base')

try:
    from biograpy.seqrecord import SeqRecordDrawer
    HAS_BIOGRAPY = True
except ImportError:
    logger.warning("Missing biograpy. Use BioPerl")
    # BioPerl
    import subprocess
    import os
    HAS_BIOGRAPY = False

@adapter(ISeqRecord, IRequest)
@implementer(IImagemapPresentation)
def seqrecordImagemap(context, request):
    # FIXME: XXX
    # context.Description()
    seqrecord = context.getSeqRecord()
    if HAS_BIOGRAPY:
        imagemap = """<map name="graphicsmap" id="graphicsmap">\n"""
        for box in SeqRecordDrawer(seqrecord, fig_width=1500).boxes():
            box['start'] = box['feature'].start
            box['end'] = box['feature'].end
            box['tag'] = box['feature'].name
            # my $tag = eval {$feature->method} || $feature->primary_tag;
            # $left += $pad_left;
            # $right += $pad_left;
            # next unless $tag;
            imagemap = imagemap + \
                """<area class="tips" shape="rect" """  \
                """coords="%(left)i,%(top)i,%(right)i,%(bottom)i" href="#" """  \
                """rel="#%(tag)sX%(start)sX$%(end)s" title="%(tag)s %(start)s:%(end)s" alt="" />""" \
                % box
        imagemap = imagemap + "</map>\n"
        return imagemap
    else:
        # BIOPERL
        perlpath = os.sep.join((os.path.dirname(__file__), "perl"))
        cmd = ["perl", "-I"+ perlpath, os.sep.join((perlpath, "graphics-imagemap-cmd.pl")), "-"]
        graphics = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        genbank=StringIO()
        seqrecord.name = seqrecord.name[:16]
        for f in seqrecord.features:
            f.type = f.type.replace(" ", "_")
        SeqIO.write([seqrecord, ], genbank, "genbank")
        try:
            (stdoutdata, stderrdata) = graphics.communicate(genbank.getvalue())
            return stdoutdata
        except:
            logger.exception('error with bioperl')
            return None

@adapter(ISeqRecord, IRequest)
@implementer(IPNGPresentation)
def seqrecordPNG(context, request):
    # FIXME: XXX
    # context.Description()
    seqrecord = context.getSeqRecord()
    if HAS_BIOGRAPY:
        imgdata=StringIO()
        SeqRecordDrawer(seqrecord, fig_width=1500).save(imgdata, format='PNG')
        return imgdata.getvalue()
    else:
        # BioPerl
        # prediction.getDataCharts() =
        # [{'chart':(line,bar,...),'data':[(x,y),(x,y),...}, ...]
        perlpath = os.sep.join((os.path.dirname(__file__), "perl"))
        cmd = ["perl", "-I"+ perlpath, os.sep.join((perlpath, "graphics-cmd.pl")), "-"]
        genbank=StringIO()
        seqrecord.name = seqrecord.name[:16]
        for f in seqrecord.features:
            f.type = f.type.replace(" ", "_")
        SeqIO.write([seqrecord, ], genbank, "genbank")
        graphics = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        try:
            (stdoutdata, stderrdata) = graphics.communicate(genbank.getvalue())
            return stdoutdata
        except:
            logger.exception('error with bioperl')
            return None

class PNGFeaturesView(BrowserPage):
    def __call__(self):
        response = self.request.response
        response.setHeader('Pragma', 'no-cache')
        response.setHeader('Content-Type', 'image/png')
        return getMultiAdapter((self.context, self.request), IPNGPresentation)

class ImagemapFeaturesView(BrowserView):
    def __call__(self):
        return seqrecordImagemap(self.context, self.request)
        # return getMultiAdapter((self.context, self.request), IImagemapPresentation)

