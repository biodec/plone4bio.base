plone4bio.base
===================

Overview
--------

The *plone4bio* package provides the possibility to add a new content
type, called `sequence', than can be either written by hand or imported
from a FASTA file, and to apply to that sequence a program, called
`predictor', that gives a back a plot of predicted probabilites for the
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

	>>> self.setRoles(('Manager',))
	>>> self.portal.invokeFactory('Sequence','ferritin')
	'ferritin'
	>>> ferritin = getattr(self.portal,'ferritin')
	
The Sequence objects are simple Zope 3-like persistent content items.. so we 
will configure the project using theirs properties.

	>>> ferritin.title = u"Ferritin"
	>>> ferritin.descritpion = u"Ferritin sequence"
	>>> ferritin.sequence = u"CMSPDQWDKEAAQYDAHAQEFEKKSHRNNGTPEADQYRHMASQYQAMAQKLKAIANQLKKGSETCR"
	
Now we can read some sequence properties:

	>>> ferritin.getSeqObj()
	....
	>>> ferritin.getPredictions()
	[]
	>>> ferritin.havePrediction("predictor")
	False
	
Developer Notes
---------------

The plone4bio* plone products are mainly developed on Debian Stable, so
they are mainly tested in that environment. Usually there should be no
problem in installing the products in other Zope/Plone environments.

This product is produced independently from the product Plone, and carries no
guarantee from the Plone Foundation about quality, suitability or anything
else. The supplier of this product assumes all responsibility for it.

Maintainer
----------

Mauro Amico (amico AT biodec DOT com) is the active maintainer of the
*plone4bio.base* framework.
