from setuptools import setup, find_packages
import os

version = '1.1.0rc3.dev0'

tests_require = [
#  'plone.app.testing',
  'Products.PloneTestCase',
]

setup(name='plone4bio.base',
      version=version,
      description="Plone4Bio base package",
      long_description='\n'.join(
          open(os.path.join(*path)).read() for path in [
              ("src", "plone4bio", "base", "README.txt"),
              ("docs", "CHANGES.txt"), ("docs", "AUTHORS.txt")]),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Framework :: Bio",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Mauro Amico',
      author_email='mauro@biodec.com',
      url='http://www.plone4bio.org',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir = {'':'src'},
      namespace_packages=['plone4bio'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Plone',
          'collective.js.jqueryui',
          'biopython',
	  ##moved to the buildout eggs. 
          #'numpy',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
