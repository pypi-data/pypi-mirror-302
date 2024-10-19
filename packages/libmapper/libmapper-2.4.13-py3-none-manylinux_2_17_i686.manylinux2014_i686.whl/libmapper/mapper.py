# -*- coding: utf-8 -*-

"""
libmapper bindings for Python

This module provides Python API for using the C library _libmapper_. Libmapper implements a system
for representing input and output signals on a network and allowing arbitrary "mappings" to be
dynamically created between them.

A "mapping" represents a data-streaming association between one or more source signals and a
destination signal, in which data is transported using either shared memory or Open Sound Control
(OSC) streams over a network. In addition to traffic management, libmapper automatically handles
address and datatype translation, and enables the use of arbitrary mathematical expressions for
conditioning, combining and transforming the source values as desired. This can be used for example
to connect a set of sensors to a synthesizer's input parameters.

For more information please visit [libmapper.org](libmapper.org)
"""

__all__ = [

    '__version__', 'has_numpy', 'Device', 'Graph', 'List', 'Map',
    'Object', 'Operator', 'Property', 'Signal', 'Time', 'Type',

    # deprecated
    'Direction', 'Location', 'Protocol', 'Status', 'Stealing'

]

from ctypes import *
from enum import IntFlag, Enum, unique
import weakref, sys
import platform
import os

try:
    import numpy as np
    NPARRAY_NAME = ('nparray').encode('utf-8')
except:
    np = None

__version__ = '2.4.13'

def has_numpy():
    return np != None

# need different library extensions for Linux, Windows, MacOS
if platform.uname()[0] == "Windows":
    name = "libmapper.dll"
elif platform.uname()[0] == "Linux":
    name = "libmapper.so"
else:
    name = "libmapper.dylib"
try:
    mpr = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), name))
except IOError:
    mpr = cdll.LoadLibrary(name)

# configuration of Py_IncRef and Py_DecRef
_c_inc_ref = pythonapi.Py_IncRef
_c_inc_ref.argtypes = [py_object]
_c_dec_ref = pythonapi.Py_DecRef
_c_dec_ref.argtypes = [py_object]

mpr.mpr_obj_get_prop_as_int32.argtypes = [c_void_p, c_int, c_char_p]
mpr.mpr_obj_get_prop_as_int32.restype = c_int
mpr.mpr_obj_get_prop_as_ptr.argtypes = [c_void_p, c_int, c_char_p]
mpr.mpr_obj_get_prop_as_ptr.restype = c_void_p
mpr.mpr_obj_get_prop_as_str.argtypes = [c_void_p, c_int, c_char_p]
mpr.mpr_obj_get_prop_as_str.restype = c_char_p

mpr.mpr_obj_set_prop.argtypes = [c_void_p, c_int, c_char_p, c_int, c_char, c_void_p, c_int]
mpr.mpr_obj_set_prop.restype = c_int

SIG_HANDLER = CFUNCTYPE(None, c_void_p, c_int, c_longlong, c_int, c_char, c_void_p, c_void_p)

@unique
class Operator(IntFlag):
    """Possible operations for composing queries."""

    DOES_NOT_EXIST          = 0x01
    EQUAL                   = 0x02
    EXISTS                  = 0x03
    GREATER_THAN            = 0x04
    GREATER_THAN_OR_EQUAL   = 0x05
    LESS_THAN               = 0x06
    LESS_THAN_OR_EQUAL      = 0x07
    NOT_EQUAL               = 0x08
    BIT_AND                 = 0x09
    BIT_OR                  = 0x0A
    ALL                     = 0x10
    ANY                     = 0x20
    NONE                    = 0x40

    def __repr__(self):
        return 'libmapper.Operator.' + self.name

@unique
class Property(Enum):
    """Symbolic representation of recognized properties."""

    UNKNOWN          = 0x0000
    BUNDLE           = 0x0100
    # 'DATA' DELIBERATELY OMITTED
    DEVICE           = 0x0300
    DIRECTION        = 0x0400
    EPHEMERAL        = 0x0500
    EXPRESSION       = 0x0600
    HOST             = 0x0700
    ID               = 0x0800
    IS_LOCAL         = 0x0900
    JITTER           = 0x0A00
    LENGTH           = 0x0B00
    LIBVERSION       = 0x0C00
    LINKED           = 0x0D00
    MAX              = 0x0E00
    MIN              = 0x0F00
    MUTED            = 0x1000
    NAME             = 0x1100
    NUM_INSTANCES    = 0x1200
    NUM_MAPS         = 0x1300
    NUM_MAPS_IN      = 0x1400
    NUM_MAPS_OUT     = 0x1500
    NUM_SIGNALS_IN   = 0x1600
    NUM_SIGNALS_OUT  = 0x1700
    ORDINAL          = 0x1800
    PERIOD           = 0x1900
    PORT             = 0x1A00
    PROCESS_LOCATION = 0x1B00
    PROTOCOL         = 0x1C00
    RATE             = 0x1D00
    SCOPE            = 0x1E00
    SIGNAL           = 0x1F00
    # SLOT DELIBERATELY OMITTED
    STATUS           = 0x2100
    STEALING         = 0x2200
    SYNCED           = 0x2300
    TYPE             = 0x2400
    UNIT             = 0x2500
    USE_INSTANCES    = 0x2600
    VERSION          = 0x2700
    EXTRA            = 0x2800

    def __repr__(self):
        return 'libmapper.Property.' + self.name

@unique
class Type(IntFlag):
    """Describes the possible data types used by libmapper."""

    UNKNOWN    = 0x00
    DEVICE     = 0x01
    SIGNAL_IN  = 0x02
    SIGNAL_OUT = 0x04
    SIGNAL     = 0x06
    MAP_IN     = 0x08
    MAP_OUT    = 0x10
    MAP        = 0x18
    OBJECT     = 0x1F
    LIST       = 0x40
    GRAPH      = 0x41
    BOOLEAN    = 0x62
    TYPE       = 0x63
    DOUBLE     = 0x64
    FLOAT      = 0x66
    INT64      = 0x68
    INT32      = 0x69
    STRING     = 0x73
    TIME       = 0x74
    POINTER    = 0x76
    NULL       = 0x4E
    NP_DOUBLE  = 0x164
    NP_FLOAT   = 0x166
    NP_INT32   = 0x169

    def __repr__(self):
        return 'libmapper.Type.' + self.name

class Time:
    """A class representing NTP timetags for use in communication and synchronization."""

    mpr.mpr_time_add.argtypes = [c_void_p, c_longlong]
    mpr.mpr_time_add.restype = None
    mpr.mpr_time_add_dbl.argtypes = [c_void_p, c_double]
    mpr.mpr_time_add_dbl.restype = None
    mpr.mpr_time_as_dbl.argtypes = [c_longlong]
    mpr.mpr_time_as_dbl.restype = c_double
    mpr.mpr_time_mul.argtypes = [c_void_p, c_double]
    mpr.mpr_time_mul.restype = None
    mpr.mpr_time_set.argtypes = [c_void_p, c_longlong]
    mpr.mpr_time_set.restype = None
    mpr.mpr_time_set_dbl.argtypes = [c_void_p, c_double]
    mpr.mpr_time_set_dbl.restype = None
    mpr.mpr_time_sub.argtypes = [c_void_p, c_longlong]
    mpr.mpr_time_sub.restype = None

    def __init__(self, *args):
        """
        Create a new Time object.

        Args:
            *args (float or libmapper.Time, optional): initial value
        """

        self.value = c_longlong()
        if args:
            self.set(args[0])
        else:
            # 1 << 32 == MPR_NOW
            self.set(1 << 32)

    def __repr__(self):
        if self.value == (1 << 32):
            return 'libmapper.Time:NOW'
        else:
            return 'libmapper.Time:{:f}'.format(self.get_double())

    def set(self, val):
        """
        Set the timetag to a given value.

        Args:
            val (float or libmapper.Time): the time value to set.

        Returns:
            self
        """

        if isinstance(val, float):
            mpr.mpr_time_set_dbl(byref(self.value), val)
        else:
            if isinstance(val, Time):
                mpr.mpr_time_set(byref(self.value), val.value)
            else:
                mpr.mpr_time_set(byref(self.value), c_longlong(val))
        return self

    def now(self):
        """
        Update the timetag to the current time.

        Returns:
            self
        """
        # 1 << 32 == MPR_NOW
        return self.set(1 << 32)

    def get_double(self):
        """Get the time value as a double-precision floating point number."""

        return mpr.mpr_time_as_dbl(self.value)

    def __add__(self, addend):
        """
        Add Time and another value.

        Args:
            addend (float or libmapper.Time): the value to add.

        Returns:
            a new Time object containing the result
        """

        result = Time(self)
        if isinstance(addend, Time):
            mpr.mpr_time_add(byref(result.value), addend.value)
        elif isinstance(addend, float):
            mpr.mpr_time_add_dbl(byref(result.value), addend)
        else:
            print("libmapper.Time.add() : incompatible type:", type(addend))
        return result

    def __iadd__(self, addend):
        """
        Add to this timetag.

        Args:
            addend (float or libmapper.Time): the value to add.

        Returns:
            self
        """

        if isinstance(addend, int):
            mpr.mpr_time_add(byref(self.value), addend)
        elif isinstance(addend, float):
            mpr.mpr_time_add_dbl(byref(self.value), addend)
        else:
            print("libmapper.Time.iadd() : incompatible type:", type(addend))
        return self

    def __radd__(self, val):
        """
        Add another value and a Time object.

        Args:
            val (numeric): the left value to add.

        Returns:
            the added value
        """

        return val + self.get_double()

    def __sub__(self, subtrahend):
        """
        Subtract another value from a Time object.

        Args:
            subtrahend (float or libmapper.Time): the value to subtract.

        Returns:
            a new Time object containing the result
        """

        result = Time(self)
        if isinstance(subtrahend, Time):
            mpr.mpr_time_sub(byref(result.value), subtrahend.value)
        else:
            mpr.mpr_time_add_dbl(byref(result.value), -subtrahend)
        return result

    def __isub__(self, subtrahend):
        """
        Subtract from this Time object.

        Args:
            subtrahend (float or libmapper.Time): the value to subtract.

        Returns:
            self
        """

        if isinstance(subtrahend, Time):
            mpr.mpr_time_sub(byref(self.value), subtrahend)
        else:
            mpr.mpr_time_add_dbl(byref(self.value), -subtrahend)
        return self

    def __rsub__(self, val):
        """
        Subtract a Time object from another value.

        Args:
            val (numeric): the value to subtract from.

        Returns:
            the result
        """

        return val - self.get_double()

    def __mul__(self, multiplicand):
        """
        Multiply Time using another value.

        Args:
            multiplicand (float or libmapper.Time): the value to multiply.

        Returns:
            a new Time object containing the result
        """

        result = Time(self)
        mpr.mpr_time_mul(byref(result.value), multiplicand)
        return result

    def __imul__(self, multiplicand):
        """
        Multiply this Time object.

        Args:
            multiplicand (float or libmapper.Time): the value to multiply.

        Returns:
            self
        """

        mpr.mpr_time_mul(byref(self.value), multiplicand)
        return self

    def __rmul__(self, val):
        """
        Multiply another value by Time object.

        Args:
            val (numeric): the value to multiply.

        Returns:
            the result
        """

        return val * self.get_double()

    def __div__(self, divisor):
        """
        Divide Time by another value.

        Args:
            divisor (float or libmapper.Time): the divisor to use.

        Returns:
            a new Time object containing the result
        """

        result = Time(self)
        mpr.mpr_time_mul(byref(result.value), 1/divisor)
        return result

    def __idiv__(self, divisor):
        """
        Divide this Time object.

        Args:
            divisor (float or libmapper.Time): the divisor to use.

        Returns:
            self
        """

        mpr.mpr_time_mul(byref(self.value), 1/divisor)
        return self

    def __rdiv__(self, val):
        """
        Divide another value by Time object.

        Args:
            val (numeric): the value to divide.

        Returns:
            the result
        """

        return val / self.get_double()

    def __lt__(self, rhs):
        """Comparison: less than"""

        if isinstance(rhs, Time):
            return self.get_double() < rhs.get_double()
        else:
            return self.get_double() < rhs

    def __le__(self, rhs):
        """Comparison: less than or equal"""

        if isinstance(rhs, Time):
            return self.get_double() <= rhs.get_double()
        else:
            return self.get_double() <= rhs

    def __eq__(self, rhs):
        """Comparison: equal"""

        if isinstance(rhs, Time):
            return self.value.value == rhs.value.value
        else:
            return self.get_double() == rhs

    def __ge__(self, rhs):
        """Comparison: greater than or equal"""

        if isinstance(rhs, Time):
            return self.get_double() >= rhs.get_double()
        else:
            return self.get_double() >= rhs

    def __gt__(self, rhs):
        """Comparison: greater than"""

        if isinstance(rhs, Time):
            return self.get_double() > rhs.get_double()
        else:
            return self.get_double() > rhs

class Object:
    pass

class List:
    """
    Lists provide a data structure for retrieving multiple Objects (Devices, Signals, or Maps) as a
    result of a query.
    """

    def __init__(self, ref):
        mpr.mpr_list_get_cpy.argtypes = [c_void_p]
        mpr.mpr_list_get_cpy.restype = c_void_p
        self._list = mpr.mpr_list_get_cpy(ref)

    def __del__(self):
        if self._list:
            mpr.mpr_list_free.argtypes = [c_void_p]
            mpr.mpr_list_free.restype = None
            mpr.mpr_list_free(self._list)
            self._list = None

    def __contains__(self, obj):
        if self._list and obj and isinstance(obj, Object):
            # use a copy
            cpy = List(mpr.mpr_list_get_cpy(self._list))
            for _obj in cpy:
                if _obj == obj:
                    return True
        return False

    def __repr__(self):
        return 'libmapper.List'

    def __iter__(self):
        return self

    @staticmethod
    def _objectify(ptr):
        # get type of libmapper object
        mpr.mpr_obj_get_type.argtypes = [c_void_p]
        mpr.mpr_obj_get_type.restype = c_byte
        _type = mpr.mpr_obj_get_type(ptr)
        if _type == Type.DEVICE:
            return Device(ptr)
        elif _type == Type.SIGNAL:
            return Signal(ptr)
        elif _type == Type.MAP:
            return Map(ptr)
        else:
            print("libmapper.List error: object is not a Device, Signal, or Map")
            return None

    def next(self):
        """
        Get the next object in the list.

        Raises:
            StopIteration: if no more items in list
        """

        if self._list:
            # self._list is the address of result, need to dereference
            result = cast(self._list, POINTER(c_void_p)).contents.value
            mpr.mpr_list_get_next.argtypes = [c_void_p]
            mpr.mpr_list_get_next.restype = c_void_p
            self._list = mpr.mpr_list_get_next(self._list)
            return List._objectify(result)
        else:
            raise StopIteration

    def filter(self, key_or_idx, val, op=Operator.EQUAL):
        """
        Apply a property-based filter to this list.

        Args:
            key_or_idx (str, int, or libmapper.Property): name, index, or symbolic identifier of
                the property to filter.
            val: value to compare with the property
            op (libmapper.Operator): operator to evaluate. Defaults to `Operator.EQUAL`.

        Returns:
            self
        """

        key, idx = c_char_p(), c_int()
        _type = type(key_or_idx)
        if _type is str:
            key.value = key_or_idx.encode('utf-8')
            idx.value = Property.UNKNOWN.value
        elif _type is Property:
            idx.value = key_or_idx.value
        elif _type is int:
            idx.value = key_or_idx
        else:
            print("libmapper.List.filter() : bad index type", _type)
            return self

        _type = type(op)
        if _type is Operator:
            op = c_int(op.value)
        elif _type is int:
            op = c_int(op)
        else:
            print("libmapper.List.filter() : bad operator type", _type)
            return self

        mpr.mpr_list_filter.argtypes = [c_void_p, c_int, c_char_p, c_int, c_char, c_void_p, c_int]
        mpr.mpr_list_filter.restype = c_void_p
        _type = type(val)
        if _type is int:
            if key_or_idx == Property.ID or key_or_idx == 'id':
                # use int64
                self._list = mpr.mpr_list_filter(self._list, idx, key, 1, Type.INT64, byref(c_longlong(val)), op)
            else:
                self._list = mpr.mpr_list_filter(self._list, idx, key, 1, Type.INT32, byref(c_int(val)), op)
        elif _type is bool:
            # convert value to int
            val = val * 1
            self._list = mpr.mpr_list_filter(self._list, idx, key, 1, Type.INT32, byref(c_int(val)), op)
        elif _type is float:
            self._list = mpr.mpr_list_filter(self._list, idx, key, 1, Type.FLOAT, byref(c_float(val)), op)
        elif _type is str:
            self._list = mpr.mpr_list_filter(self._list, idx, key, 1, Type.STRING, c_char_p(val.encode('utf-8')), op)
        else:
            print("libmapper.List.filter() : unhandled filter value type", _type)
        return self

    def join(self, rhs):
        """
        Join this list with another list.

        Args:
            rhs (libmapper.List): the list to join

        Returns:
            self
        """

        if not isinstance(rhs, List):
            return self
        if rhs._list is None:
            return self
        # need to use a copy of rhs list
        cpy = mpr.mpr_list_get_cpy(rhs._list)
        mpr.mpr_list_get_union.argtypes = [c_void_p, c_void_p]
        mpr.mpr_list_get_union.restype = c_void_p
        self._list = mpr.mpr_list_get_union(self._list, cpy)
        return self

    def intersect(self, rhs):
        """
        Intersect this list with another list.

        Args:
            rhs (libmapper.List): the list to intersect

        Returns:
            self
        """

        if not isinstance(rhs, List):
            return self
        if rhs._list is None:
            return self
        # need to use a copy of list
        cpy = mpr.mpr_list_get_cpy(rhs._list)
        mpr.mpr_list_get_isect.argtypes = [c_void_p, c_void_p]
        mpr.mpr_list_get_isect.restype = c_void_p
        self._list = mpr.mpr_list_get_isect(self._list, cpy)
        return self

    def subtract(self, rhs):
        """
        Exclude items from another list from this list.

        Args:
            rhs (libmapper.List): the list to subtract

        Returns:
            self
        """

        if not isinstance(rhs, List):
            return self
        if rhs._list is None:
            return self
        # need to use a copy of list
        cpy = mpr.mpr_list_get_cpy(rhs._list)
        mpr.mpr_list_get_diff.argtypes = [c_void_p, c_void_p]
        mpr.mpr_list_get_diff.restype = c_void_p
        self._list = mpr.mpr_list_get_diff(self._list, cpy)
        return self

    def __getitem__(self, index):
        """
        Retrieve an object in the list by index.

        Args:
            index (int): index of the list item to retrieve.

        Returns:
            the object located at the specified index.

        Raises:
            IndexError: if index is invalid
        """

        # python lists allow a negative index
        if index < 0:
            mpr.mpr_list_get_size.argtypes = [c_void_p]
            mpr.mpr_list_get_size.restype = c_int
            index += mpr.mpr_list_get_size(self._list)
        if index >= 0:
            mpr.mpr_list_get_idx.argtypes = [c_void_p, c_uint]
            mpr.mpr_list_get_idx.restype = c_void_p
            ret = mpr.mpr_list_get_idx(self._list, index)
            if ret:
                return List._objectify(ret)
        raise IndexError
        return None

    def __next__(self):
        """Get the next object in the list."""

        return self.next()

    def __len__(self):
        """Retrieve the number of objects in the list."""

        mpr.mpr_list_get_size.argtypes = [c_void_p]
        mpr.mpr_list_get_size.restype = c_int
        return mpr.mpr_list_get_size(self._list)

    def print(self):
        """
        Print the contents of the list.

        Returns:
            self
        """

        mpr.mpr_list_print.argtypes = [c_void_p]
        mpr.mpr_list_print.restype = None
        mpr.mpr_list_print(self._list)
        return self

class Object:
    """Objects provide a generic representation of Graphs, Devices, Signals, and Maps."""

    class Status(IntFlag):
        """Describes the possible statuses for a libmapper object."""

        UNDEFINED   = 0x0000
        NEW         = 0x0001
        MODIFIED    = 0x0002
        REMOVED     = 0x0004
        EXPIRED     = 0x0008
        STAGED      = 0x0010
        ACTIVE      = 0x0020
        HAS_VALUE   = 0x0040
        NEW_VALUE   = 0x0080
        UPDATE_LOC  = 0x0100
        UPDATE_REM  = 0x0200
        REL_UPSTRM  = 0x0400
        REL_DNSTRM  = 0x0800
        OVERFLOW    = 0x1000
        ANY         = 0x1FFF

        def __str__(self):
            if self._name_ is not None:
                return self._name_
            members, uncovered = _decompose(self.__cls__, self._value_)
            return '|'.join([str(m._name_ or m._value_) for m in members])

        def __repr__(self):
            return 'libmapper.Object.Status(' + str(self) + ')'

    def __init__(self, ref):
        self._obj = ref

    def graph(self):
        """Retrieve the parent `Graph` object for an object."""

        mpr.mpr_obj_get_graph.argtypes = [c_void_p]
        mpr.mpr_obj_get_graph.restype = c_void_p
        return Graph(None, mpr.mpr_obj_get_graph(self._obj))

    def get_status(self):
        """Get the status of an object"""

        mpr.mpr_obj_get_status.argtypes = [c_void_p]
        mpr.mpr_obj_get_status.restype = c_int
        return Status(mpr.mpr_obj_get_status(self._obj))

    def reset_status(self):
        """Reset the ephemeral status flags of an object"""

        mpr.mpr_obj_reset_status.argtypes = [c_void_p]
        mpr.mpr_obj_reset_status.restype = c_void_p
        mpr.mpr_obj_reset_status(self._obj)

    def get_num_properties(self):
        """Get an object's number of properties."""

        mpr.mpr_obj_get_num_props.argtypes = [c_void_p]
        mpr.mpr_obj_get_num_props.restype = c_int
        return mpr.mpr_obj_get_num_props(self._obj)
    num_properties = property(get_num_properties)

    def set_property(self, key_or_idx, val, publish=True):
        """
        Set an object property.

        Args:
            key_or_idx (str, int, or libmapper.Property): name, index, or symbolic identifier of
                the property to set.
            val: a value or list of values to set
            publish (boolean): True if property should be public, False otherwise

        Returns:
            self
        """

        if np and isinstance(val, np.ndarray):
            val = val.flatten().tolist()
        elif val is None:
            self.remove_property(key_or_idx)
            return self

        publish = 1 if True else 0
        _key, _idx, _val, _pub = c_char_p(), c_int(), c_void_p(), c_int()
        _len = 1
        _type = type(key_or_idx)
        if _type is str:
            _key.value = key_or_idx.encode('utf-8')
            _idx.value = Property.UNKNOWN.value
        elif _type is Property:
            _idx.value = key_or_idx.value
        elif _type is int:
            if key_or_idx == 0x0200: # MPR_PROP_DATA
                print("libmapper.Object.set_property({}) : key 0x0200 (DATA) is protected".format(key_or_idx))
                return self
            _idx.value = key_or_idx
        else:
            print("libmapper.Object.set_property({}) : bad key type".format(key_or_idx), _type)
            return self

        _type = type(val)
        if _type is list:
            _len = len(val)
            _type = type(val[0])
            if _len == 1:
                val = val[0]
            # TODO: check if types are homogeneous
        if _type is str:
            _type = c_char(Type.STRING.value)
            if _len == 1:
                _val = c_char_p(val.encode('utf-8'))
                mpr.mpr_obj_set_prop(self._obj, _idx, _key, _len, _type, _val, publish)
            else:
                str_array = (c_char_p * _len)()
                str_array[:] = [x.encode('utf-8') for x in val]
                mpr.mpr_obj_set_prop(self._obj, _idx, _key, _len, _type, str_array, publish)
        elif _type is int:
            _type = c_char(Type.INT32.value)
            if _len == 1:
                mpr.mpr_obj_set_prop(self._obj, _idx, _key, _len, _type, byref(c_int(val)), publish)
            else:
                int_array = (c_int * _len)()
                int_array[:] = [ int(x) for x in val ]
                mpr.mpr_obj_set_prop(self._obj, _idx, _key, _len, _type, int_array, publish)
        elif _type is float:
            _type = c_char(Type.FLOAT.value)
            if _len == 1:
                mpr.mpr_obj_set_prop(self._obj, _idx, _key, _len, _type, byref(c_float(val)), publish)
            else:
                float_array = (c_float * _len)()
                float_array[:] = [ float(x) for x in val ]
                mpr.mpr_obj_set_prop(self._obj, _idx, _key, _len, _type, float_array, publish)
        elif _type is Signal.Direction or _type is Map.Location or _type is Map.Protocol or _type is Signal.Stealing:
            _type = c_char(Type.INT32.value)
            if _len == 1:
                mpr.mpr_obj_set_prop(self._obj, _idx, _key, _len, _type, byref(c_int(val.value)), publish)
            else:
                int_array = (c_int * _len)()
                int_array[:] = [ x.value for x in val ]
                mpr.mpr_obj_set_prop(self._obj, _idx, _key, _len, _type, int_array, publish)
        elif _type is bool:
            _type = c_char(Type.BOOLEAN.value)
            if _len == 1:
                mpr.mpr_obj_set_prop(self._obj, _idx, _key, _len, _type, byref(c_int(val)), publish)
            else:
                int_array = (c_int * _len)()
                int_array[:] = [ int(x) for x in val ]
                mpr.mpr_obj_set_prop(self._obj, _idx, _key, _len, _type, int_array, publish)
        else:
            print("libmapper.Object.set_property({}) : unhandled type".format(key_or_idx), _type)
        return self

    def get_property(self, key_or_idx):
        """
        Retrieve an object property.

        Args:
            key_or_idx (str, int, or libmapper.Property): name, index, or symbolic identifier of
                the property to get.

        Returns:
            If called with a string or symbolic identifier argument the value of the property will
            be returned. If called with an integer index both key and value will be returned. In
            either case `None` will be returned if the property does not exist.
        """

        _len, _type, _val, _pub = c_int(), c_char(), c_void_p(), c_int()
        if isinstance(key_or_idx, str):
            _key = key_or_idx.encode('utf-8')
            mpr.mpr_obj_get_prop_by_key.argtypes = [c_void_p, c_char_p, c_void_p, c_void_p, c_void_p, c_void_p]
            mpr.mpr_obj_get_prop_by_key.restype = c_int
            prop = mpr.mpr_obj_get_prop_by_key(self._obj, _key, byref(_len), byref(_type), byref(_val), byref(_pub))
        elif isinstance(key_or_idx, int) or isinstance(key_or_idx, Property):
            if isinstance(key_or_idx, Property):
                _idx = c_int(key_or_idx.value)
            else:
                _idx = c_int(key_or_idx)
                if key_or_idx > self.num_properties:
                    raise StopIteration
            _key = c_char_p()
            mpr.mpr_obj_get_prop_by_idx.argtypes = [c_void_p, c_int, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p]
            mpr.mpr_obj_get_prop_by_idx.restype = c_int
            prop = mpr.mpr_obj_get_prop_by_idx(self._obj, _idx, byref(_key), byref(_len),
                                               byref(_type), byref(_val), byref(_pub))
        else:
            return None
        if prop == 0 or prop == 0x0200: # MPR_PROP_DATA
            return None
        is_np_array = False
        if np and (prop == 0x0E00 or prop == 0x0F00 or prop == 0x2400): # MAX, MIN, or TYPE
            # check if obj is signal and has 'nparray' property
            if isinstance(self, Signal) and mpr.mpr_obj_get_prop_as_int32(self._obj, 0x2800, NPARRAY_NAME):
                is_np_array = True
        prop = Property(prop)

        _type = _type.value
        _len = _len.value
        val = None
        if _val.value == None:
            val = None
        elif _type == b's':
            if _len == 1:
                val = string_at(cast(_val, c_char_p)).decode('utf-8')
            else:
                _val = cast(_val, POINTER(c_char_p))
                val = [_val[i].decode('utf-8') for i in range(_len)]
        elif _type == b'b':
            _val = cast(_val, POINTER(c_int))
            if _len == 1:
                val = _val[0] != 0
            else:
                val = [(_val[i] != 0) for i in range(_len)]
        elif _type == b'i':
            _val = cast(_val, POINTER(c_int))
            if _len == 1:
                val = _val[0]

                # translate some values into Enums
                if prop == Property.DIRECTION:
                    val = Signal.Direction(val)
                elif prop == Property.PROCESS_LOCATION:
                    val = Map.Location(val)
                elif prop == Property.PROTOCOL:
                    val = Map.Protocol(val)
                elif prop == Property.STATUS:
                    status = Object.Status.UNDEFINED
                    for name, member in Object.Status.__members__.items():
                        if member.value > val:
                            break
                        status = member
                    val = status
                elif prop == Property.STEALING:
                    val = Signal.Stealing(val)
            else:
                val = [_val[i] for i in range(_len)]
            if is_np_array:
                val = np.array(val)
        elif _type == b'h':
            _val = cast(_val, POINTER(c_longlong))
            if _len == 1:
                val = _val[0]
            else:
                val = [_val[i] for i in range(_len)]
        elif _type == b'f':
            _val = cast(_val, POINTER(c_float))
            if _len == 1:
                val = _val[0]
            else:
                val = [_val[i] for i in range(_len)]
            if is_np_array:
                val = np.array(val)
        elif _type == b'd':
            _val = cast(_val, POINTER(c_double))
            if _len == 1:
                val = _val[0]
            else:
                val = [_val[i] for i in range(_len)]
            if is_np_array:
                val = np.array(val)
        elif _type == b'\x01': # device
            if _len != 1:
                print("libmapper.Object.get_property({}:{}) : can't handle device array type".format(prop, key_or_idx))
                return None
            elif _val.value == None:
                val = None
            else:
                val = Device(_val.value)
        elif _type == b'@': # list
            if _len != 1:
                print("libmapper.Object.get_property({}:{}) : can't handle list array type".format(prop, key_or_idx))
                return None
            elif _val.value == None:
                val = None
            else:
                val = List(_val.value);
        elif _type == b'c':
            if prop != Property.TYPE:
                print("libmapper.Object.get_property({}:{}) : unhandled char type".format(prop, key_or_idx), val)
                return None
            _val = cast(_val, POINTER(c_byte))
            if _len == 1:
                val = _val[0]
                if val == 102: # 'f'
                    val = Type.NP_FLOAT if is_np_array else Type.FLOAT
                elif val == 104: # 'i'
                    val = Type.NP_INT32 if is_np_array else Type.INT32
                elif val == 100: # 'd'
                    val = Type.NP_DOUBLE if is_np_array else Type.DOUBLE
                else:
                    val = Type(val)
            else:
                val = [Type(_val[i]) for i in range(_len)]
        elif _type == b't':
            _val = cast(_val, POINTER(c_longlong))
            if _len == 1:
                val = Time(_val[0])
            else:
                val = [Time(_val[i]) for i in range(_len)]
        else:
            print("libmapper.Object.get_property({}:{}) : can't handle prop type".format(prop, key_or_idx), _type)
            return None

        if isinstance(key_or_idx, int):
            return (string_at(_key).decode("utf-8"), val)
        else:
            return val

    def get_properties(self):
        """Get a dictionary specifying all object properties."""

        props = {}
        for i in range(self.num_properties):
            prop = self.get_property(i)
            if prop:
                props.update({prop[0]: prop[1]})
        return props

    def __propgetter(self):
        obj = self
        props = self.get_properties()
        class propsetter(dict):
            __getitem__ = props.__getitem__
            def __setitem__(self, key, val):
                props[key] = val
                obj.set_property(key, val)
        return propsetter(self.get_properties())
    properties = property(__propgetter)

    def set_properties(self, props):
        """
        Set an object property.

        Args:
            props (list): List of property key-value pairs to set. See documentation for
                `set_property` for more information on acceptable keys.
        """

        [self.set_property(k, props[k]) for k in props]
        return self

    def __getitem__(self, key):
        return self.get_property(key)

    def __setitem__(self, key, val):
        self.set_property(key, val)
        return self

    def remove_property(self, key_or_idx):
        """
        Remove a property from a libmapper object.

        Args:
            key_or_idx (str, int, or libmapper.Property): name, index, or symbolic identifier of
                the property to remove.

        Returns:
            self
        """

        mpr.mpr_obj_remove_prop.argtypes = [c_void_p, c_int, c_char_p]
        mpr.mpr_obj_remove_prop.restype = c_int
        if isinstance(key_or_idx, str):
            mpr.mpr_obj_remove_prop(self._obj, Property.UNKNOWN.value, key_or_idx.encode('utf-8'))
        elif isinstance(key_or_idx, int):
            mpr.mpr_obj_remove_prop(self._obj, key_or_idx, None)
        elif isinstance(key_or_idx, Property):
            mpr.mpr_obj_remove_prop(self._obj, key_or_idx.value, None)
        else:
            print("libmapper.Object.remove_property({}) : bad key or index type".format(key_or_idx))
        return self

    def __contains__(self, key):
        """
        Check whether a libmapper object contains the named property.

        Args:
            key (str or libmapper.Property): name or symbolic identifier of the property to check for.

        Returns:
            True if the property exists, False otherwise.
        """

        return self[key] is not None

    def __nonzero__(self):
        return False if self.this is None else True

    def __eq__(self, rhs):
        """Evaluate equality between libmapper objects by comparing object ids"""

        return rhs != None and self['id'] == rhs['id']

    def type(self):
        """Retrieve the `Type` of a libmapper object."""

        mpr.mpr_obj_get_type.argtypes = [c_void_p]
        mpr.mpr_obj_get_type.restype = c_byte
        _type = int(mpr.mpr_obj_get_type(self._obj))
        return Type(_type)

    def print(self, staged=0):
        """Print the properties of an object."""

        mpr.mpr_obj_print.argtypes = [c_void_p, c_int]
        mpr.mpr_obj_print(self._obj, staged)
        return self

    def push(self):
        """Push any staged property changes out to the distributed graph."""

        mpr.mpr_obj_push.argtypes = [c_void_p]
        mpr.mpr_obj_push.restype = None
        if self._obj:
            mpr.mpr_obj_push(self._obj)
        return self

c_sig_cb_type = CFUNCTYPE(None, c_void_p, c_int, c_longlong, c_int, c_char, c_void_p, c_longlong)

@CFUNCTYPE(None, c_void_p, c_int, c_longlong, c_int, c_char, c_void_p, c_longlong)
def signal_cb_py(_sig, _evt, _inst, _len, _type, _val, _time):
    data = mpr.mpr_obj_get_prop_as_ptr(_sig, 0x0200, None) # MPR_PROP_DATA
    cb = cast(data, py_sig_cb_type)

    if cb == None:
        print("error: couldn't retrieve signal callback")
        return

    if _val == None:
        val = None
    elif _type == b'i':
        _val = cast(_val, POINTER(c_int))
        if _len == 1:
            val = _val[0]
        else:
            val = [_val[i] for i in range(_len)]
    elif _type == b'f':
        _val = cast(_val, POINTER(c_float))
        if _len == 1:
            val = _val[0]
        else:
            val = [_val[i] for i in range(_len)]
    elif _type == b'd':
        _val = cast(_val, POINTER(c_double))
        if _len == 1:
            val = _val[0]
        else:
            val = [_val[i] for i in range(_len)]
    else:
        print("sig_cb_py : unknown signal type", _type)
        return

    if np and mpr.mpr_obj_get_prop_as_int32(_sig, 0x2800, NPARRAY_NAME):
        val = np.array(val)

    # TODO: check if cb was registered with signal or instances
    cb(Signal(_sig), Signal.Event(_evt), _inst, val, Time(_time))

class Signal(Object):
    """
    Signals define inputs or outputs for Devices.  A Signal consists of a scalar or vector value
    of some integer or floating-point type.  A Signal is created by adding an input or output to
    a Device by calling `Device.add_signal()`.  It can optionally be provided with some metadata
    such as range, unit, or other properties.  Signals can be dynamically connected together in a
    dataflow graph by creating Maps using the libmapper API or an external session manager.
    """

    @unique
    class Direction(IntFlag):
        """The set of possible directions for a signal."""

        INCOMING   = 1
        OUTGOING   = 2
        ANY        = 3
        BOTH       = 4

        def __repr__(self):
            return 'libmapper.Signal.Direction.' + self.name

    @unique
    class Event(IntFlag):
        """The set of possible signal events, used to register and inform callbacks."""

        NONE        = 0x0000
        INST_NEW    = 0x0001
        UPDATE      = 0x0200
        REL_UPSTRM  = 0x0400
        REL_DNSTRM  = 0x0800
        INST_OFLW   = 0x1000
        ALL         = 0x1FFF

        def __repr__(self):
            return 'libmapper.Signal.Event.' + self.name

    @unique
    class Status(IntFlag):
        """The set of possible status flags for a signal instance."""

        UNDEFINED           = 0x0000
        NEW                 = 0x0001

        STAGED              = 0x0010
        ACTIVE              = 0x0020

        HAS_VALUE           = 0x0040
        NEW_VALUE           = 0x0080

        UPDATE_LOC          = 0x0100
        UPDATE_REM          = 0x0200
        REL_UPSTRM          = 0x0400
        REL_DNSTRM          = 0x0800
        OVERFLOW            = 0x1000
        ANY                 = 0x1FFF

        def __str__(self):
            if self._name_ is not None:
                return self._name_
            members, uncovered = _decompose(self.__cls__, self._value_)
            return '|'.join([str(m._name_ or m._value_) for m in members])

        def __repr__(self):
            return 'libmapper.Signal.Status(' + str(self) + ')'

    @unique
    class Stealing(Enum):
        """The set of possible instance-stealing modes."""

        NONE    = 0
        OLDEST  = 1
        NEWEST  = 2

        def __repr__(self):
            return 'libmapper.Signal.Stealing.' + self.name

    def __init__(self, sigptr=None):
        self._obj = sigptr
        self.id = 0
        self._is_sig_inst = False
        self.callback = None

    def __repr__(self):
        return 'libmapper.Signal:{}'.format(self[Property.NAME])

    def free(self):
        if not self[Property.IS_LOCAL]:
            return

        data = mpr.mpr_obj_get_prop_as_ptr(self._obj, 0x0200, None) # MPR_PROP_DATA
        if data != None:
            cb = cast(data, py_sig_cb_type)
            _c_dec_ref(cb)

        mpr.mpr_sig_free.argtypes = [c_void_p]
        mpr.mpr_sig_free.restype = None
        mpr.mpr_sig_free(self._obj)
        self._obj = None

    def set_callback(self, callback, events=Event.ALL):
        """
        Set or unset the message handler for a signal.

        Args:
            callback: a function to be called when the Signal is updated.
            events (bitflags: libmapper.Signal.Event): The type(s) of events that will trigger the
                callback.

        Returns:
            self
        """

        data = mpr.mpr_obj_get_prop_as_ptr(self._obj, 0x0200, None) # MPR_PROP_DATA
        if data != None:
            cb = cast(data, py_sig_cb_type)
            _c_dec_ref(cb)
        if callback:
            self.callback = py_sig_cb_type(callback)
            _c_inc_ref(self.callback)
        else:
            self.callback = None
        mpr.mpr_obj_set_prop(self._obj, 0x0200, None, 1, Type.POINTER.value, self.callback, 0) # MPR_PROP_DATA

        mpr.mpr_sig_set_cb.argtypes = [c_void_p, c_sig_cb_type, c_int]
        mpr.mpr_sig_set_cb.restype = None
        mpr.mpr_sig_set_cb(self._obj, signal_cb_py, events.value)
        return self

    def set_value(self, value):
        """
        Update the value of a signal instance.

        Args:
            value (number or list of numbers): The value to set

        Returns:
            self
        """

        mpr.mpr_sig_set_value.argtypes = [c_void_p, c_longlong, c_int, c_char, c_void_p]
        mpr.mpr_sig_set_value.restype = None

        if np and isinstance(value, np.ndarray):
            value = value.flatten().tolist()
        elif value is None:
            mpr.mpr_sig_set_value(self._obj, self.id, 0, MPR_INT32, None)
            return self
        if isinstance(value, list):
            if any(not (isinstance(x, int) or isinstance(x, float)) for x in value):
                print("libmapper.Signal.set_value() accepts only scalars or lists of type float and int")
                return self
            _len = len(value)
            if any(isinstance(x, float) for x in value):
                float_array = (c_float * _len)()
                float_array[:] = [ float(x) for x in value ]
                mpr.mpr_sig_set_value(self._obj, self.id, _len, Type.FLOAT.value, float_array)
            else:
                int_array = (c_int * _len)()
                int_array[:] = [ int(x) for x in value ]
                mpr.mpr_sig_set_value(self._obj, self.id, _len, Type.INT32.value, int_array)
        else:
            _type = type(value)
            if _type is int:
                mpr.mpr_sig_set_value(self._obj, self.id, 1, Type.INT32.value, byref(c_int(value)))
            elif _type is float:
                mpr.mpr_sig_set_value(self._obj, self.id, 1, Type.FLOAT.value, byref(c_float(value)))
            else:
                print("libmapper.Signal.set_value() accepts only scalars or lists of type float and int")
        return self

    def get_value(self):
        """
        Get the value of a Signal or Signal Instance.

        Note:
            Remote Signals and local Signals that have not yet been updated will not have a value.
            Similarly, "ephemeral" Signal Instances may not have an associated value at a given
            time.

        Returns:
            The current value of the Signal, or `None` if the Signal/Instance has no value.
        """

        mpr.mpr_sig_get_value.argtypes = [c_void_p, c_longlong, c_void_p]
        mpr.mpr_sig_get_value.restype = c_void_p
        _time = Time()
        _val = mpr.mpr_sig_get_value(self._obj, self.id, byref(_time.value))
        if _val == None:
            return None

        _type = mpr.mpr_obj_get_prop_as_int32(self._obj, Property.TYPE.value, None)
        if _type == Type.INT32.value:
            _val = cast(_val, POINTER(c_int))
        if _type == Type.FLOAT.value:
            _val = cast(_val, POINTER(c_float))
        if _type == Type.DOUBLE.value:
            _val = cast(_val, POINTER(c_double))

        _len = mpr.mpr_obj_get_prop_as_int32(self._obj, Property.LENGTH.value, None)
        if _len == 1:
            return [_val[0], _time]
        else:
            _val = [_val[i] for i in range(_len)]
            return [_val, _time]

    def reserve_instances(self, arg):
        """
        Allocate new instances and add them to the reserve list.

        Args:
            arg (int or list): An `int` it is interpreted as the number of new instances to
                allocate. If a `list` is passed instead it is interpreted as a list of instance
                `ids` for which instances should be allocated.

        Note:
            If instance ids are specified, libmapper will not add multiple instances with the same id.

        Returns:
            self
        """

        mpr.mpr_sig_reserve_inst.argtypes = [c_void_p, c_int, c_void_p, c_void_p]
        if isinstance(arg, int):
            count = mpr.mpr_sig_reserve_inst(self._obj, arg, None, None)
        elif isinstance(arg, list):
            _len = len(arg)
            array = (c_longlong * _len)()
            array[:] = [ int(x) for x in arg ]
            count = mpr.mpr_sig_reserve_inst(self._obj, _len, array, None)
        return self

    def Instance(self, id):
        """
        Allocate and/or access a specific Signal Instance

        Signal Instances can be used to describe the multiplicity and/or ephemerality of phenomena
        associated with Signals. A signal describes the phenomena, e.g. the position of a 'blob' in
        computer vision, and the signal's instances will describe the positions of actual detected
        blobs.

        Args:
            id: The identifier of the Instance to allocate/access.
        """

        ret = Signal(self._obj)
        ret.id = id
        ret._is_sig_inst = True
        return ret

    def release(self):
        """Release this signal instance."""

        mpr.mpr_sig_release_inst.argtypes = [c_void_p, c_longlong]
        mpr.mpr_sig_release_inst.restype = None
        mpr.mpr_sig_release_inst(self._obj, self.id)

    def get_status(self):
        """Get the status of this signal or signal instance."""

        if self._is_sig_inst:
            mpr.mpr_sig_get_inst_status.argtypes = [c_void_p, c_longlong]
            mpr.mpr_sig_get_inst_status.restype = c_int
            return Signal.Status(mpr.mpr_sig_get_inst_status(self._obj, self.id))
        else:
            return super().get_status()

    def num_instances(self, status=Status.ANY):
        """
        Get the number of instances for this Signal.

        Args:
            status (libmapper.Signal.Status): The statuses of the instances to search for.

        Returns:
             The number of allocated signal instances matching the specified status.
        """

        mpr.mpr_sig_get_num_inst.argtypes = [c_void_p, c_int]
        mpr.mpr_sig_get_num_inst.restype = c_int
        if not isinstance(status, Signal.Status):
            status = Signal.Status(status)
        return mpr.mpr_sig_get_num_inst(self._obj, status.value)

    def instance_id(self, idx, status=Status.ANY):
        """
        Get a Signal Instance's identifier by its index.

        Args:
            idx (int): The numerical index of the instance to retrieve.  Should be between zero
                and the number of instances.
            status (libmapper.Signal.Status): The statuses of the instances to search for.

        Returns:
            The instance identifier associated with the given index, or `0` if unsuccessful.
        """

        mpr.mpr_sig_get_inst_id.argtypes = [c_void_p, c_int, c_int]
        mpr.mpr_sig_get_inst_id.restype = c_longlong
        if not isinstance(status, Signal.Status):
            status = Signal.Status(status)
        return mpr.mpr_sig_get_inst_id(self._obj, idx, status.value)

    def device(self):
        """
        Retrieve the parent Device for this Signal.

        Returns:
            The parent Device
        """

        mpr.mpr_sig_get_dev.argtypes = [c_void_p]
        mpr.mpr_sig_get_dev.restype = c_void_p
        device = mpr.mpr_sig_get_dev(self._obj)
        return Device(device)

    def maps(self, direction=Direction.ANY):
        """
        Get the list of Maps for a given Signal.

        Args:
            direction (libmapper.Signal.Direction): The direction of the Maps to return.
                Defaults to `ANY`.

        Returns:
            mpr.List
        """

        mpr.mpr_sig_get_maps.argtypes = [c_void_p, c_int]
        mpr.mpr_sig_get_maps.restype = c_void_p
        return List(mpr.mpr_sig_get_maps(self._obj, direction))

py_sig_cb_type = CFUNCTYPE(None, py_object, py_object, c_longlong, py_object, py_object)

class Map(Object):
    """
    Maps define dataflow connections between sets of signals. A map consists of one or more sources,
    one destination, and properties which determine how the source data is processed.
    """

    @unique
    class Location(IntFlag):
        """Describes the possible endpoints of a map."""

        SOURCE      = 1
        DESTINATION = 2
        ANY         = 3

        def __repr__(self):
            return 'libmapper.Map.Location.' + self.name

    @unique
    class Protocol(Enum):
        """Describes the possible network protocol for map communication."""

        UDP = 1
        TCP = 2

        def __repr__(self):
            return 'libmapper.Map.Protocol.' + self.name

    def __init__(self, *args):
        """
        Create a map between a set of signals.

        Note:
            The map will not take effect until it has been added to the distributed graph using
            `push()`.

        If the first argument of the Map constructor is a string it will be interpreted as the Map
        "expression" with embedded format specifiers (%x for map source(s) and %y for the
        destination) which will be associated with subsequent arguments, e.g.:

            my_map = libmapper.Map("%y = (%x + %x) * 0.5;", dst_sig, src_sig1, src_sig2)

        To construct a Map with the default expression---or if you intend to specify the expression
        property value later---simply call the constructor with a source Signal and a destination
        Signal as arguments. Convergent maps can be constructed by passing a listmof source Signals
        for the first argument.

            my_map = libmapper.Map(src_sig, dst_sig)
            my_convergent_map = libmapper.Map([src_sig1, src_sig2], dst_sig)

        Returns:
            The new Map object.
        """

        mpr.mpr_map_new.argtypes = [c_int, c_void_p, c_int, c_void_p]
        mpr.mpr_map_new.restype = c_void_p

        # initialize from preallocated mpr_obj
        if args and isinstance(args[0], int):
            self._obj = args[0]
            return

        if len(args) < 2 or len(args) > 11:
            print("libmapper.Map: wrong number of arguments", len(args))
            return

        self._obj = None
        if isinstance(args[0], str):
            expr = args[0].encode('utf-8')
            sigs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # initialize to NULL
            for i in range(len(args) - 1):
                if not isinstance(args[i+1], Signal):
                    print("libmapper.Map() argument", i, "is not a libmapper.Signal object")
                    return
                sigs[i] = c_void_p(args[i+1]._obj)
            mpr.mpr_map_new_from_str.argtypes = [c_char_p]
            mpr.mpr_map_new_from_str.restype = c_void_p
            self._obj = mpr.mpr_map_new_from_str(expr, sigs[0], sigs[1], sigs[2], sigs[3], sigs[4],
                                                 sigs[5], sigs[6], sigs[7], sigs[8], sigs[9])
        else:
            if not isinstance(args[1], Signal):
                print("libmapper.Map() destination argument is not a libmapper.Signal object")
                return
            if isinstance(args[0], list):
                num_srcs = len(args[0])
                array_type = c_void_p * num_srcs
                src_array = array_type()
                for i in range(num_srcs):
                    if not isinstance(args[0][i], Signal):
                        print("libmapper.Map() source argument", i, "is not a libmapper.Signal object")
                        return
                    src_array[i] = args[0][i]._obj
                self._obj = mpr.mpr_map_new(num_srcs, src_array, 1, byref(c_void_p(args[1]._obj)))
            elif isinstance(args[0], Signal):
                num_srcs = 1
                self._obj = mpr.mpr_map_new(1, byref(c_void_p(args[0]._obj)), 1, byref(c_void_p(args[1]._obj)))
            else:
                print("libmapper.Map() source argument is not a libmapper.Signal object")

    def release(self):
        """
        Remove a map between a set of signals.

        Note:
            After releasing a Map the object should no longer be used.
        """

        mpr.mpr_map_release.argtypes = [c_void_p]
        mpr.mpr_map_release.restype = None
        mpr.mpr_map_release(self._obj)

    def signals(self, location=Location.ANY):
        """
        Retrieve a list of connected signals for a specific map.

        Args:
            location (libmapper.Map.Location): The relative location of the map endpoint, must be
                `SOURCE`, `DESTINATION`, or `ANY`.

        Returns:
            A `libmapper.List` of results.
        """

        mpr.mpr_map_get_sigs.argtypes = [c_void_p, c_int]
        mpr.mpr_map_get_sigs.restype = c_void_p
        return List(mpr.mpr_map_get_sigs(self._obj, location))

    def index(self, signal):
        """
        Retrieve the index for a specific map signal.

        Args:
            signal (libmapper.Signal): The signal to find.

        Returns:
             The signal index, or `-1` if not found.
        """

        if not isinstance(signal, Signal):
            print("libmapper.Map.index() : bad argument type", type(signal))
            return None
        mpr.mpr_map_get_sig_idx.argtypes = [c_void_p, c_void_p]
        mpr.mpr_map_get_sig_idx.restype = c_int
        idx = mpr.mpr_map_get_sig_idx(self._obj, signal._obj)
        return idx

    def get_is_ready(self):
        """
        Get whether a Map is completely initialized.

        Returns:
            True if initialized, False otherwise.
        """

        mpr.mpr_map_get_is_ready.argtypes = [c_void_p]
        mpr.mpr_map_get_is_ready.restype = c_int
        return 0 != mpr.mpr_map_get_is_ready(self._obj)
    ready = property(get_is_ready)

    def add_scope(self, device):
        """
        Add a map scope

        Note:
            Changes to remote maps will not take effect until synchronized with the distributed
            graph using `push()`

        Args:
            device (libmapper.Device): Device to add as a scope for this map. After taking effect,
                this setting will cause instance updates originating at this device to be propagated
                across the map.

        Returns:
            self
        """

        if isinstance(device, Device):
            mpr.mpr_map_add_scope.argtypes = [c_void_p, c_void_p]
            mpr.mpr_map_add_scope.restype = None
            mpr.mpr_map_add_scope(self._obj, device._obj)
        return self

    def remove_scope(self, device):
        """
        Remove a map scope

        Note:
            Changes to remote maps will not take effect until synchronized with the distributed
            graph using `push()`

        Args:
            device (libmapper.Device): Device to remove as a scope for this map. After taking
                effect, this setting will cause instance updates originating at this device to be
                blocked from propagating across the map.

        Returns:
            self
        """

        if isinstance(device, Device):
            mpr.mpr_map_remove_scope.argtypes = [c_void_p, c_void_p]
            mpr.mpr_map_remove_scope.restype = None
            mpr.mpr_map_remove_scope(self._obj, device._obj)
        return self

class Graph(Object):
    pass

graph_dev_cbs = set()
graph_sig_cbs = set()
graph_map_cbs = set()

@CFUNCTYPE(None, c_void_p, c_void_p, c_int, c_void_p)
def graph_cb_py(_graph, c_obj, evt, user):
    mpr.mpr_obj_get_type.argtypes = [c_void_p]
    mpr.mpr_obj_get_type.restype = c_byte
    _type = mpr.mpr_obj_get_type(c_obj)
    if _type == Type.DEVICE:
        for f in graph_dev_cbs:
            f(Type.DEVICE, Device(c_obj), Graph.Event(evt))
    elif _type == Type.SIGNAL:
        for f in graph_sig_cbs:
            f(Type.SIGNAL, Signal(c_obj), Graph.Event(evt))
    elif _type == Type.MAP:
        for f in graph_map_cbs:
            f(Type.MAP, Map(c_obj), Graph.Event(evt))

class Graph(Object):
    """
    Graphs are the primary interface through which a program may observe the distributed graph
    and store information about devices and signals that are present.  Each Graph stores records
    of devices, signals, and maps, which can be queried.
    """

    mpr.mpr_graph_get_list.argtypes = [c_void_p, c_int]
    mpr.mpr_graph_get_list.restype = c_void_p

    @unique
    class Event(Enum):
        """The set of possible graph events, used to inform callbacks."""
        NEW      = 0x01
        MODIFIED = 0x02
        REMOVED  = 0x04
        EXPIRED  = 0x08

        def __repr__(self):
            return 'libmapper.Graph.Event.' + self.name

    def __init__(self, subscribe_flags=Type.OBJECT, ptr=None):
        """
        Create a peer in the distributed graph.

        Args:
            subscribe_flags (bitflags: libmapper.Type): A combination of `libmapper.Type` values
                controlling whether the graph should automatically subscribe to information about
                devices, signals and/or maps when it encounters a previously-unseen device.

        Returns:
            The new Graph object
        """

        if ptr != None:
            self._obj = ptr
        else:
            mpr.mpr_graph_new.argtypes = [c_int]
            mpr.mpr_graph_new.restype = c_void_p
            self._obj = mpr.mpr_graph_new(subscribe_flags.value)

#        self._finalizer = weakref.finalize(self, mpr_graph_free, self._obj)
        mpr.mpr_graph_add_cb.argtypes = [c_void_p, c_void_p, c_int, c_void_p]
        mpr.mpr_graph_add_cb(self._obj, graph_cb_py, Type.DEVICE | Type.SIGNAL | Type.MAP, None)

    def free(self):
        """Disconnect from the network and free resources."""
        mpr.mpr_graph_free.argtypes = [c_void_p]
        mpr.mpr_graph_free.restype = None
        mpr.mpr_graph_free(self._obj)
        self._obj = None

    def set_interface(self, iface):
        """
        Set the network interface to use.

        Args:
            iface (str): The human-friendly name of the network interface to use.

        Returns:
            True if successful, False otherwise.
        """

        mpr.mpr_graph_set_interface.argtypes = [c_void_p, c_char_p]
        if isinstance(iface, str):
            mpr.mpr_graph_set_interface(self._obj, iface.encode('utf-8'))
        return self

    def get_interface(self):
        """
        Retrieve the network interface currently in use.

        Returns:
             A string containing the name of the network interface.
        """

        mpr.mpr_graph_get_interface.argtypes = [c_void_p]
        mpr.mpr_graph_get_interface.restype = c_char_p
        iface = mpr.mpr_graph_get_interface(self._obj)
        return string_at(iface).decode('utf-8')
    interface = property(get_interface, set_interface)

    def set_address(self, address, port):
        """
        Set the multicast group and port to use.

        Args:
            address (str): The multicast group for bus communication with the distributed graph.
            port (int): The port to use for multicast communication.

        Returns:
            True if successful, False otherwise.
        """

        if isinstance(address, str) and isinstance(port, int):
            mpr.mpr_graph_set_address.argtypes = [c_void_p, c_char_p, c_int]
            mpr.mpr_graph_set_address.restype = c_int
            return 0 == mpr.mpr_graph_set_address(self._obj, address.encode('utf-8'), port)
        return False

    def get_address(self):
        """
        Retrieve the multicast group currently in use.

        Returns:
            A string specifying the current multicast address.
        """

        mpr.mpr_graph_get_address.argtypes = [c_void_p]
        mpr.mpr_graph_get_address.restype = c_char_p
        address = mpr.mpr_graph_get_address(self._obj)
        return string_at(address).decode('utf-8')
    address = property(get_address, set_address)

    def poll(self, timeout=0):
        """
        Synchronize a local graph copy with the distributed graph.

        Args:
            timeout (timeout): The number of milliseconds to block, or `0` for non-blocking
                behaviour. Defaults to `0`.
        """

        mpr.mpr_graph_poll.argtypes = [c_void_p, c_int]
        mpr.mpr_graph_poll(self._obj, timeout)
        return self

    def add_callback(self, func, types=Type.OBJECT):
        """
        Register a callback for when an object record is added or updated in the graph.

        Args:
            func: a function to be called when object records are added, modified, or removed
            types (bitflags: libmapper.Type): Bitflags setting the type of information of interest.
                Can be a combination of `DEVICE`, `SIGNAL`, and/or `MAP`. Defaults to `OBJECT`
                (any object type).

        Returns:
            self
        """

        updated = False
        if types & Type.DEVICE:
            if func not in graph_dev_cbs:
                graph_dev_cbs.add(func)
                updated = True
        if types & Type.SIGNAL:
            if func not in graph_sig_cbs:
                graph_sig_cbs.add(func)
                updated = True
        if types & Type.MAP:
            if func not in graph_map_cbs:
                graph_map_cbs.add(func)
                updated = True
        return self

    def remove_callback(self, func):
        """
        Remove an object record callback from the graph service.

        Args:
            func: The callback function to remove.

        Returns:
            self
        """

        updated = False
        if func in graph_dev_cbs:
            graph_dev_cbs.remove(func)
            updated = True
        if func in graph_sig_cbs:
            graph_sig_cbs.remove(func)
            updated = True
        if func in graph_map_cbs:
            graph_map_cbs.remove(func)
            updated = True
        return self

    def subscribe(self, device, flags, timeout=-1):
        """
        Subscribe to information about a specific device.

        Args:
            device (libmapper.Device): The device to subscribe to, or `None` for any device.
            flags (bitflags: libmapper.Type): The type of information to subscribe to
                (`DEVICE`, `SIGNAL`, `MAP`, or a combination of these types).
            timeout (int): The length in seconds for this subscription. If set to `-1`, the graph
                will automatically renew the subscription until it is freed or this function is
                called again. Defaults to `-1`.

        Returns:
            self
        """

        mpr.mpr_graph_subscribe.argtypes = [c_void_p, c_void_p, c_int, c_int]
        mpr.mpr_graph_subscribe.restype = None
        if device == None:
            mpr.mpr_graph_subscribe(self._obj, None, flags, timeout)
        elif isinstance(device, Device):
            mpr.mpr_graph_subscribe(self._obj, device._obj, flags, timeout)
        return self

    def unsubscribe(self, device=None):
        """
        Unsubscribe from receiving information from remote objects

        Args:
            device (libmapper.Device, optional): The device to unsubscribe from. If omitted of set
                to `None` the graph will unsubscribe from all devices

        Returns:
            self
        """

        mpr.mpr_graph_unsubscribe.argtypes = [c_void_p, c_void_p]
        mpr.mpr_graph_unsubscribe.restype = None
        if isinstance(device, Device):
            mpr.mpr_graph_unsubscribe(self._obj, device._obj)
        elif device == None:
            mpr.mpr_graph_unsubscribe(self._obj, 0)
        return self

    def devices(self):
        """Retrieve a list of Devices from the Graph."""

        list = mpr.mpr_graph_get_list(self._obj, Type.DEVICE)
        return List(list)

    def signals(self):
        """Retrieve a list of Signals from the Graph."""

        return List(mpr.mpr_graph_get_list(self._obj, Type.SIGNAL))

    def maps(self):
        """Retrieve a list of Maps from the Graph."""

        return List(mpr.mpr_graph_get_list(self._obj, Type.MAP))

    def object(self, id, type=Type.OBJECT):
        """
        Retrieve an object from the Graph

        Args:
            if (libmapper.Id): The identifier of the object to retrieve.
            type (libmapper.Type): The type of the object to look for, or `OBJECT` if not known.

        Returns:
            The object matching the query.
        """

        mpr.mpr_graph_get_obj.argtypes = [c_void_p, c_longlong, c_int]
        mpr.mpr_graph_get_obj.restype = c_void_p
        return Object(mpr.mpr_graph_get_obj(self._obj, id, type))

class Device(Object):
    """
    A Device is an entity on the distributed graph which typically has input and/or output signals.
    The `Device` is the primary interface through which most programs use libmapper. A Device must
    have a name, to which a unique ordinal is automatically appended. It can also be given other
    user-specified metadata.
    """

    def __init__(self, *args):
        """
        Allocate a new Device.

        Args:
            name (str): A short descriptive string to identify the Device. Must not contain spaces
                or the slash character '/'.
            graph (libmapper.Graph, optional): A previously allocated Graph structure to use. If
                omitted a new Graph strcuture will be allocated.
        """

        mpr.mpr_dev_new.argtypes = [c_char_p, c_void_p]
        mpr.mpr_dev_new.restype = c_void_p
        self._obj = None

        if not args or len(args) < 1:
            return

        # initialize from preallocated mpr_obj
        if isinstance(args[0], int):
            self._obj = args[0]
            return

        graph = None
        if len(args) > 1 and isinstance(args[1], Graph):
            graph = args[1]._obj
        if isinstance(args[0], str):
            cname = c_char_p()
            cname.value = args[0].encode('utf-8')
            self._obj = mpr.mpr_dev_new(cname, graph)
        else:
            print("libmapper.Device: missing name in constructor")

    def free(self):
        """Remove a Device from the graph and free its resources."""

        if not self._obj or not self[Property.IS_LOCAL]:
            return
        for s in self.signals():
            s.free()
        mpr.mpr_dev_free.argtypes = [c_void_p]
        mpr.mpr_dev_free.restype = None
        mpr.mpr_dev_free(self._obj)
        self._obj = None

    def __repr__(self):
        return 'libmapper.Device:{}'.format(self[Property.NAME])

    def poll(self, timeout=0):
        """
        Poll this Device for new messages.

        Note:
            If you have multiple Devices, the right thing to do is call this function for each of
            them with `timeout=0`, and add your own sleep if necessary.

        Args:
            timeout (int): Number of milliseconds to block waiting for messages, or `0` for
                non-blocking behaviour. Defaults to `0`.
        """

        mpr.mpr_dev_poll.argtypes = [c_void_p, c_int]
        mpr.mpr_dev_poll.restype = c_int
        return mpr.mpr_dev_poll(self._obj, timeout)

    def add_signal(self, dir, name, length=1, datatype=Type.FLOAT, unit=None, min=None, max=None,
                   num_inst=None, callback=None, events=Signal.Event.ALL):
        """
        Create a new Signal and add it to this Device.

        Args:
            dir (libmapper.Signal.Direction): The signal Direction.
            name (str): The name of the signal.
            length (int): The length of the signal vector, or `1` for a scalar. Defaults to `1`.
            datatype (libmapper.Type): The type of the signal value. Defaults to `FLOAT`.
            unit (str, optional): The unit of the signal.
            min (numeric, optional): The minimum value for this signal, if any.
            max (numeric, optional): The maximum value for this signal, if any.
            num_inst (int or None): The number of instances for this signal, or None for singleton.
            callback (code, optional): Function to be called when the signal is updated.
            events (libmapper.Signal.Event): The types of events to trigger a call to `callback`.

        Returns:
            The new Signal.
        """

        mpr.mpr_sig_new.argtypes = [c_void_p, c_int, c_char_p, c_int, c_char, c_char_p, c_void_p,
                                    c_void_p, POINTER(c_int), c_void_p, c_int]
        mpr.mpr_sig_new.restype = c_void_p

        is_np_array = np and datatype > 0xFF
        datatype &= 0xFF

        ptr = mpr.mpr_sig_new(self._obj, dir.value, name.encode('utf-8'), length,
                              datatype.value, None, None, None, None, None, Signal.Event.NONE)

        signal = Signal(ptr)
        if is_np_array:
            mpr.mpr_obj_set_prop(ptr, 0, NPARRAY_NAME, 1, 0x62, byref(c_int(1)), 0)
        if callback is not None:
            signal.set_callback(callback, events)
        if unit is not None:
            signal.set_property(Property.UNIT, unit)
        if min is not None:
            signal.set_property(Property.MIN, min)
        if max is not None:
            signal.set_property(Property.MAX, max)
        if num_inst is not None and isinstance(num_inst, int):
            signal.reserve_instances(num_inst)
            signal.set_property(Property.EPHEMERAL, True)
        return signal

    def remove_signal(self, signal):
        """
        Remove a Signal and free its resources.

        Args:
            signal (libmapper.Signal): The Signal to remove.

        Returns:
            self
        """

        if isinstance(signal, Signal):
            signal.free()
        return self

    def signals(self, direction=Signal.Direction.ANY):
        """
        Get the list of Signals for a given Device.

        Args:
            direction (libmapper.Signal.Direction): The Direction of the Signals to return.
                Defaults to `ANY`.

        Returns:
            mpr.List
        """

        mpr.mpr_dev_get_sigs.argtypes = [c_void_p, c_int]
        mpr.mpr_dev_get_sigs.restype = c_void_p
        return List(mpr.mpr_dev_get_sigs(self._obj, direction))

    def maps(self, direction=Signal.Direction.ANY):
        """
        Get the list of Maps for a given Device.

        Args:
            direction (libmapper.Signal.Direction): The Direction of the Maps to return.
                Defaults to `ANY`.

        Returns:
            mpr.List
        """

        mpr.mpr_dev_get_maps.argtypes = [c_void_p, c_int]
        mpr.mpr_dev_get_maps.restype = c_void_p
        return List(mpr.mpr_dev_get_maps(self._obj, direction))

    def get_is_ready(self):
        """
        Get whether a device is completely initialized.

        Returns:
            True if initialized, False otherwise.
        """

        mpr.mpr_dev_get_is_ready.argtypes = [c_void_p]
        mpr.mpr_dev_get_is_ready.restype = c_int
        return 0 != mpr.mpr_dev_get_is_ready(self._obj)
    ready = property(get_is_ready)

    def get_time(self):
        """
        Get the current time for a device.

        Returns:
            libmapper.Time
        """

        mpr.mpr_dev_get_time.argtypes = [c_void_p]
        mpr.mpr_dev_get_time.restype = c_longlong
        return Time(mpr.mpr_dev_get_time(self._obj))

    def set_time(self, val):
        """
        Set the time for a device.

        Note:
            Use only if user code has access to a more accurate timestamp than the operating system.
            This time will be used for tagging signal updates until the next occurrence `set_time()`
            or `poll()`.

        Args:
            val (libmapper.Time or double): The time to set.

        Returns:
            self
        """

        mpr.mpr_dev_set_time.argtypes = [c_void_p, c_longlong]
        mpr.mpr_dev_set_time.restype = None
        if not isinstance(val, Time):
            val = Time(val)
        mpr.mpr_dev_set_time(self._obj, val.value)
        return self

    def update_maps(self):
        """
        Trigger map propagation for a given timestep.

        Note:
            This function can be omitted if `poll()` is called each timestep, however calling
            `poll()` at a lower rate may be more performant.

        Returns:
            self
        """

        mpr.mpr_dev_update_maps.argtypes = [c_void_p]
        mpr.mpr_dev_update_maps.restype = None
        mpr.mpr_dev_update_maps(self._obj)
        return self

# deprecated enums
Direction = Signal.Direction
Location = Map.Location
Protocol = Map.Protocol
Status = Object.Status
Stealing = Signal.Stealing
