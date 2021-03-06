==============
plone4bio.base
==============

Overview
--------

The *plone4bio* package provides the possibility to add a new content
type, called sequence, than can be either written by hand or imported
from a FASTA file, and to apply to that sequence a program, called
predictor, that gives a back a plot of predicted probabilites for the
sequence to have a given property (the property that the predictor tries
to determine). 

A predictor can try to assess if a protein sequence is trans-membrane,
whether a signal peptide exists, and so on. 

The *plone4bio.base* is a package that defines a skeleton
predictor: deriving from that it is possible to integrate any other
application and visualize all the results together.  A predictor can be
a pure Python program or another application wrapped to be usable by the
interface defined in the *plone4bio.base* package.

Creating a sequence
-------------------

Let us create some sequences.

    >>> self.login()
    >>> self.setRoles(('Manager',))
    >>> self.portal.invokeFactory('SeqRecord', u'ferritin', title=u'Ferritin')
    'ferritin'
    >>> ferritin = getattr(self.portal, u'ferritin')
    >>> ferritin.descritpion = u"Ferritin sequence"
    >>> ferritin.sequence = u"CMSPDQWDKEAAQYDAHAQEFEKKSHRNNGTPEADQYRHMASQYQAMAQKLKAIANQLKKGSETCR"
    >>> ferritin.alphabet="Bio.Alphabet.ProteinAlphabet"
    >>> ferritin.annotations.update(dict(date='10-MAR-2010', data_file_division='PLN'))

Now we can read some sequence properties:

    >>> ferritin.seqrecord
    SeqRecord(seq=Seq('CMSPDQWDKEAAQYDAHAQEFEKKSHRNNGTPEADQYRHMASQYQAMAQKLKAI...TCR', ProteinAlphabet()), id='ferritin', name=u'Ferritin', description='', dbxrefs=[])
    
Export genbank format:
    
    >>> print ferritin.restrictedTraverse('@@gbk')()
    LOCUS       Ferritin                  66 aa                     PLN 10-MAR-2010
    DEFINITION  
    ACCESSION   ferritin
    VERSION     ferritin
    KEYWORDS    .
    SOURCE      .
      ORGANISM  .
                .
    FEATURES             Location/Qualifiers
    ORIGIN
            1 cmspdqwdke aaqydahaqe fekkshrnng tpeadqyrhm asqyqamaqk lkaianqlkk
           61 gsetcr
    //

Prediction's stuff:

    >>> from Products.CMFCore.utils import getToolByName
    >>> pred_tool = getToolByName(self.portal, 'plone4bio_predictors')

Define a fake predictor:

    >>> import copy
    >>> from plone4bio.base.interfaces import IPredictor
    >>> from zope.interface import implements
    >>> from Bio.SeqFeature import FeatureLocation, SeqFeature
    >>> class FakePredictor:
    ...     implements(IPredictor)
    ...     def name(self):
    ...         return self.__class__.__name__
    ...
    ...     def run(self, seqr, **kwargs):
    ...         seqr = copy.deepcopy(seqr)
    ...         seqr.features.append(SeqFeature(location=FeatureLocation(1,len(seqr.seq)), type="fake"))
    ...         return seqr
    ...

Register fake predictor:

    >>> pred_tool.registerPredictor(FakePredictor())
    >>> pred_tool.listPredictors()
    [<Predictor at /plone/plone4bio_predictors/FakePredictor>]

Run fake predictor over ferritin seqrecord:

    >>> seqr_ann = pred_tool('FakePredictor', ferritin.seqrecord, store=False)
    >>> seqr_ann
    SeqRecord(seq=Seq('CMSPDQWDKEAAQYDAHAQEFEKKSHRNNGTPEADQYRHMASQYQAMAQKLKAI...
    >>> len(seqr_ann.features)
    1
    >>> print seqr_ann.features[0]
    type: fake
    location: [1:66]
    qualifiers: 

Original seqrecord must be untouched:

    >>> len(ferritin.seqrecord.features)
    0

Now run the predictor over Plone4Bio's SeqRecord wrapper:

    >>> seqr_ann = pred_tool('FakePredictor', ferritin, store=False)
    >>> seqr_ann
    <SeqRecord at ferritin>
    >>> seqr_ann.seqrecord
    SeqRecord(seq=Seq('CMSPDQWDKEAAQYDAHAQEFEKKSHRNNGTPEADQYRHMASQYQAMAQKLKAI...
    >>> len(seqr_ann.seqrecord.features)
    1
    >>> len(ferritin.seqrecord.features)
    0
    >>> pred_tool('FakePredictor', ferritin, store=True)
    <SeqRecord at /plone/ferritin>
    >>> len(ferritin.seqrecord.features)
    1

...

Developer Notes
===============
The *plone4bio* plone products are mainly developed on Debian Stable, so
they are mainly tested in that environment. Usually there should be no
problem in installing the products in other Zope/Plone environments.

This product is produced independently from the product Plone, and carries no
guarantee from the Plone Foundation about quality, suitability or anything
else. The supplier of this product assumes all responsibility for it.

Getting the source code
-----------------------

The source code is maintained in the Plone4Bio Subversion
repository. To check out the trunk: ::

  $ svn co http://plone4bio.org/svn/plone4bio.base/trunk/

You can also browse the code online at
`http://plone4bio.org/trac/browser/plone4bio.base/trunk
<http://plone4bio.org/trac/browser/plone4bio.base/trunk>`_.

When using setuptools or zc.buildout you can use the following
URL to retrieve the latest development code as Python egg: ::

  $ http://plone4bio.org/svn/plone4bio.base/trunk/#egg=plone4bio.base


Bug tracker
===========
For bug reports, suggestions or questions please use the
Launchpad bug tracker at
`http://plone4bio.org
<http://plone4bio.org>`_.

