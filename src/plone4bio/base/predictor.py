import sys
from UserDict import UserDict
from OFS.SimpleItem import SimpleItem
from zope.interface import implements
from Globals import PersistentMapping
try:
    from ZODB.PersistentList import PersistentList
except ImportError:
    from persistent.list import PersistentList

from plone4bio.base import Plone4BioException
from plone4bio.base.content.seqrecord import SeqRecord
from plone4bio.base.interfaces import IPredictor
from plone4bio.base.interfaces import ISeqRecord

def make_config_persistent(kwargs):
    """ iterates on the given dictionnary and replace list by persistent list,
    dictionary by persistent mapping.
    """
    for key, value in kwargs.items():
        if type(value) == type({}):
            p_value = PersistentMapping(value)
            kwargs[key] = p_value
        elif type(value) in (type(()), type([])):
            p_value = PersistentList(value)
            kwargs[key] = p_value

def make_config_nonpersistent(kwargs):
    """ iterates on the given dictionary and replace ListClass by python List,
        and DictClass by python Dict
    """
    for key, value in kwargs.items():
        if isinstance(value, PersistentMapping):
            p_value = dict(value)
            kwargs[key] = p_value
        elif isinstance(value, PersistentList):
            p_value = list(value)
            kwargs[key] = p_value

class Predictor(SimpleItem):
    """A predictor is an external method with
    additional configuration information
    """

    implements(IPredictor)

    meta_type = 'Predictor'
    meta_types = all_meta_types = ()

    def __init__(self, id, module, predictor=None):
        self.id = id
        self.module = module
        self._class = predictor.__class__.__name__
        # DM 2004-09-09: 'Transform' instances are stored as
        #  part of a module level configuration structure
        #  Therefore, they must not contain persistent objects
        self._config = UserDict()
        self._config.__allow_access_to_unprotected_subobjects__ = 1
        self._config_metadata = UserDict()
        self._predictor_init(1, predictor)

    def predictorclass(self):
        """ """
        return self.module + "." + self._class

    def name(self):
        """return the name of the predictor instance"""
        return self.id

    def _predictor_init(self, set_conf=0, predictor=None):
        """ """
        __traceback_info__ = (self.module, )
        if predictor is None:
            predictor = self._load_predictor()
        else:
            self._v_predictor = predictor
        # check this is a valid predictor
        if not hasattr(predictor, '__class__'):
            raise Plone4BioException('Invalid predictor : predictor is not a class')
        if not IPredictor.providedBy(predictor):
            raise Plone4BioException('Invalid predictor : IPredictor is not implemented by %s' % predictor.__class__)
        # if not hasattr(predictor, 'run'):
        #     raise Plone4BioException('Invalid predictor : missing required "run" attribute')
        # manage configuration
        if set_conf and hasattr(predictor, 'config'):
            conf = dict(predictor.config)
            self._config.update(conf)
            make_config_persistent(self._config)
            if hasattr(predictor, 'config_metadata'):
                conf = dict(predictor.config_metadata)
                self._config_metadata.update(conf)
                make_config_persistent(self._config_metadata)
        predictor.config = dict(self._config)
        make_config_nonpersistent(predictor.config)
        predictor.config_metadata = dict(self._config_metadata)
        make_config_nonpersistent(predictor.config_metadata)

        # self.inputs = predictor.inputs
        # self.output = predictor.output
        # self.output_encoding = getattr(predictor, 'output_encoding', None)
        return predictor

    def _load_predictor(self):
        klass = self.predictorclass()
        __traceback_info__ = klass
        parts = klass.split( '.' )
        if not parts:
            raise ValueError, "incomplete klass name: %s" % klass
        parts_copy = parts[:]
        while parts_copy:
            try:
                module = __import__( '.'.join( parts_copy ) )
                break
            except ImportError:
                # Reraise if the import error was caused inside the imported file
                if sys.exc_info()[2].tb_next is not None: raise
                del parts_copy[ -1 ]
                if not parts_copy:
                    return None
        parts = parts[ 1: ] # Funky semantics of __import__'s return value
        obj = module
        for part in parts:
            try:
                obj = getattr( obj, part )
            except AttributeError:
                return None
        self._v_predictor = obj()

    def run(self, obj, context=None, store=False, argv=([],{})):
        """ """
        assert type(argv[0]) == list
        assert type(argv[1]) == dict
        import pdb; pdb.set_trace()
        if not hasattr(self, '_v_predictor'):
            self._load_predictor()
        if ISeqRecord.providedBy(obj):
            newseqr = self._v_predictor.run(obj.seqrecord, *argv[0], **argv[1])
            if store:
                #TODO: need locking?
                obj.features = newseqr.features
                #TODO: raise event
                return obj
            else:
                return SeqRecord(title=newseqr.name, seqrecord=newseqr)
        else:
            newseqr = self._v_predictor.run(obj, *argv[0], **argv[1])
            if store:
                obj.features = newseqr.features
                return obj
            else:
                return newseqr
