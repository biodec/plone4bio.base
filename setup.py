from setuptools import setup, find_packages

version = '0.9'
readme = open('README.txt')
long_description = readme.read()
readme.close()

setup(name='plone4bio.base',
      version=version,
      description="",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='BioDec Srl',
      author_email='',
      url='http://www.biodec.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone4bio'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
