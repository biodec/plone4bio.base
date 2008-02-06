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

from plone4bio.base.interfaces import IGenericPrediction
from plone4bio.base.png.interfaces import IPNGPresentation

# matplotlib
"""
import matplotlib
matplotlib.use('Agg')
import pylab
from matplotlib.backends.backend_agg import FigureCanvasAgg
"""

# PIL
from PIL import Image,ImageDraw,ImageFont

from StringIO import StringIO
from PIL import Image as PILImage

class PNGView(BrowserPage):
    def __call__(self):
        response = self.request.response
        response.setHeader('Pragma', 'no-cache')
        response.setHeader('Content-Type', 'image/png')
        return getMultiAdapter((self.context,self.request),IPNGPresentation)

@adapter(IGenericPrediction,IRequest)
@implementer(IPNGPresentation)
def predictionPNG(context,request):
    # context.getId
    # context.getDataCharts() = [{'chart':(line,bar,...),'data':[(x,y),(x,y),...}, ...]
    width = 600
    height = 20
    bgcolor = 0xFFFFFF
    img = Image.new("RGB", [width,height], bgcolor)
    gdi = ImageDraw.Draw(img)
    data = context.getDataCharts()
    for d in data:
        gdi = drawData(gdi,d)
    imgfile=StringIO()
    img.save(imgfile, "PNG")
    imgfile.seek(0)
    return imgfile.getvalue()

def drawData(gdi, d, x0=0, y0=0, y1=20):
    if (d['chart'] == 'bar'):
        for t in d['data']:
             gdi.line([x0+t[0],y0,x0+t[0],y1],d['color'][t[1]])
    return gdi
        
"""         
    pylab.clf()
    img_dpi=72
    width=600
    height=120
    fig=pylab.figure(dpi=img_dpi, figsize=(width/img_dpi, height/img_dpi))
    x=context.xrange()
    prob=pylab.plot(x,context.prob())
    # pylab.legend(prob, "prob", "upper right")
    pylab.xlabel('index')
    pylab.ylabel('prob')
    pylab.grid(True)
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    size = (int(canvas.figure.get_figwidth())*img_dpi, int(canvas.figure.get_figheight())*img_dpi)
    buf=canvas.tostring_rgb()
    im=PILImage.fromstring('RGB', size, buf, 'raw', 'RGB', 0, 1)
    imgdata=StringIO()
    im.save(imgdata, 'PNG')
    return imgdata.getvalue()
"""