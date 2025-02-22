"""EnvGen.sc"""

from ...base import utils as utl
from .. import ugen as ugn
from .. import env as env


class Done(ugn.UGen):
    NONE = 0
    PAUSE_SELF = 1
    FREE_SELF = 2
    FREE_SELF_AND_PREV = 3
    FREE_SELF_AND_NEXT = 4
    FREE_SELF_AND_FREE_ALL_IN_PREV = 5
    FREE_SELF_AND_FREE_ALL_IN_NEXT = 6
    FREE_SELF_TO_HEAD = 7
    FREE_SELF_TO_TAIL = 8
    FREE_SELF_PAUSE_PREV = 9
    FREE_SELF_PAUSE_NEXT = 10
    FREE_SELF_AND_DEEP_FREE_PREV = 11
    FREE_SELF_AND_DEEP_FREE_NEXT = 12
    FREE_ALL_IN_GROUP = 13
    FREE_GROUP = 14
    FREE_SELF_RESUME_NEXT = 15

    @classmethod
    def kr(cls, src):
        return cls._multi_new('control', src)


class FreeSelf(ugn.UGen):
    @classmethod
    def kr(cls, input):
        cls._multi_new('control', input)
        return input


class PauseSelf(ugn.UGen):
    @classmethod
    def kr(cls, input):
        cls._multi_new('control', input)
        return input


class FreeSelfWhenDone(ugn.UGen):
    @classmethod
    def kr(cls, src):
        return cls._multi_new('control', src)


class PauseSelfWhenDone(ugn.UGen):
    @classmethod
    def kr(cls, src):
        return cls._multi_new('control', src)


class Pause(ugn.UGen):
    @classmethod
    def kr(cls, gate, id):
        return cls._multi_new('control', gate, id)


class Free(ugn.UGen):
    @classmethod
    def kr(cls, trig, id):
        return cls._multi_new('control', trig, id)


class EnvGen(ugn.UGen):
    @classmethod
    def ar(cls, envelope, gate=1.0, level_scale=1.0, level_bias=0.0,
           time_scale=1.0, done_action=0):
        '''
        envelope can be a tuple, a list of tuples for multiple channels
        or an instance of Env.
        '''
        if isinstance(envelope, env.Env):
            envelope = utl.unbubble(envelope.envgen_format())  # Was as_multichannel_list.
        return cls._multi_new('audio', gate, level_scale, level_bias,
                              time_scale, done_action, envelope)

    @classmethod
    def kr(cls, envelope, gate=1.0, level_scale=1.0, level_bias=0.0,
           time_scale=1.0, done_action=0):
        '''
        envelope can be a tuple, a list of tuples for multiple channels
        or an instance of Env.
        '''
        if isinstance(envelope, env.Env):
            envelope = utl.unbubble(envelope.envgen_format())  # Was as_multichannel_list.
        return cls._multi_new('control', gate, level_scale, level_bias,
                              time_scale, done_action, envelope)

    @classmethod
    def _new1(cls, rate, *args):
        obj = cls()
        obj._rate = rate
        obj._add_to_synth()
        args = list(args)
        envelope = args.pop()
        return obj._init_ugen(*args, *envelope)

    # Override may be an optimization in sclang.
    # def _init_ugen(self, inputs)  # override

    def _arg_names_inputs_offset(self):  # override
        return 1  # One less than sclang.


class Linen(ugn.UGen):
    @classmethod
    def kr(cls, gate=1.0, attack_time=0.01, sus_level=1.0,
           release_time=1.0, done_action=0):
        return cls._multi_new('control', gate, attack_time, sus_level,
                              release_time, done_action)
