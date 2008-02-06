""" 
implementations:
    - using javascript libs (like timeplot, ...) - TODO
    - using matplotlib - TODO
    - directly using gd libs (currently implemented)
"""

from zope.publisher.interfaces import IRequest
from zope.publisher.browser import BrowserPage
from zope.interface import implementer
from zope.component import adapter
from zope.component import getMultiAdapter

from plone4bio.base.interfaces import ISequence
from plone4bio.base.png.interfaces import IPNGPresentation
from plone4bio.base.png.prediction import drawData as drawDataPrediction

# PIL
from PIL import Image,ImageDraw,ImageFont
from StringIO import StringIO

height = 100
leftM = 140
rightM = 0
topM = 10
zoom = 6     # zoom = font.width
zitems = 100 # zitems * zoom = width
width = 600
margin = 20
width = 720
rowHeight = 12 
barHeight = 7 
bgcolor = 0xFFFFFF

class PNGView(BrowserPage):
    def __call__(self):
        response = self.request.response
        response.setHeader('Pragma', 'no-cache')
        response.setHeader('Content-Type', 'image/png')
        return getMultiAdapter((self.context,self.request),IPNGPresentation)

@adapter(ISequence,IRequest)
@implementer(IPNGPresentation)
def sequencePNG(context,request):
    # prediction.getDataCharts() = [{'chart':(line,bar,...),'data':[(x,y),(x,y),...}, ...]
    # import pdb; pdb.set_trace()
    predictions = context.getPredictions()
    _width = width + leftM + rightM
    _height = topM + 10 + (rowHeight * len(predictions))
    img = Image.new("RGB", [_width,_height], bgcolor)
    gdi = ImageDraw.Draw(img)
    textw = 0
    for pred in predictions:
        (w,h)=drawLabelSize(gdi, pred.predname)
        if w > textw: 
            textw = w
    y = topM
    x = textw + 4
    for pred in predictions:
        data = pred.getDataCharts()
        gdi=drawLabel(gdi, pred.predname, y0=y)
        #for d in data :
        gdi = drawDataPrediction(gdi, data[0], x0=x, y0=y, y1=y+barHeight)
        y = y+rowHeight
    # gdi=drawLabel(gdi, pred.predname, y, y+rowHeight)
    imgfile=StringIO()
    img.save(imgfile, "PNG")
    imgfile.seek(0)
    return imgfile.getvalue()


def drawLabel(gdi, l, x0=0, y0=0, color=0x000000):
    gdi.text([x0, y0], l, color, font=ImageFont.load_default())
    return gdi

def drawLabelSize(gdi, l):
    return gdi.textsize(l,font=ImageFont.load_default())
