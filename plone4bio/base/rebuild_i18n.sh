#!/bin/sh
PRODUCTNAME=plone4bio
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the templates.
# Also merge it with generated.pot, which includes the items
# from schema.py
i18ndude rebuild-pot --pot locales/${PRODUCTNAME}.pot --create ${I18NDOMAIN} .

# Synchronise the resulting .pot with the .po files
i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/nl/LC_MESSAGES/${PRODUCTNAME}.po

msgfmt -o locales/nl/LC_MESSAGES/${PRODUCTNAME}.mo locales/nl/LC_MESSAGES/${PRODUCTNAME}.po