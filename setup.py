from setuptools import setup, find_packages

version = '1.0.1'
readme = open('./src/plone4bio/base/README.txt')
long_description = readme.read()
readme.close()

setup(name='plone4bio.base',
      version=version,
      description="Plone4Bio base package",
      long_description=long_description,
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
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'numpy',
          'biopython',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
