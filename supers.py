class Recorder(object):
    def add_recordable(self): return []

    @property
    def recordable(self):
        return super(type(self), self).add_recordable()


class SpikeRecorder(Recorder):
    def add_recordable(self):
        variables = super(SpikeRecorder, self).add_recordable()
        variables.append('spikes')
        return variables


class VRecorder(Recorder):
    def add_recordable(self):
        variables = super(VRecorder, self).add_recordable()
        variables.append('v')
        return variables


class GsynRecorder(Recorder):
    def add_recordable(self):
        variables = super(GsynRecorder, self).add_recordable()
        variables.append('gysn')
        return variables


class C(SpikeRecorder, GsynRecorder, VRecorder):
    pass


c = C()
print c.recordable


class RecorderAlan(object):
    recordables = []

    def __init__(self, name):
        self.recordables.append(name)

    @property
    def recordable(self):
        return self.recordables


class SpikeRecorderAlan(RecorderAlan):

    def __init__(self):
        RecorderAlan.__init__(self, "spikes")


class VRecorderAlan(RecorderAlan):
    def __init__(self):
        RecorderAlan.__init__(self, "v")


class GsynRecorderAlan(RecorderAlan):
    def __init__(self):
        RecorderAlan.__init__(self, "gsyn")


class Alan(SpikeRecorderAlan, GsynRecorderAlan, VRecorderAlan):
    def __init__(self):
        SpikeRecorderAlan.__init__(self)
        GsynRecorderAlan.__init__(self)
        VRecorderAlan.__init__(self)


alan = Alan()
print alan.recordable


class Recorder3(object):
    recordables = []

    def __new__(cls):
        return super(Recorder3, cls).__new__(cls)

    def _add_record_type(self, name):
        self.recordables.append(name)

    @property
    def recordable(self):
        return self.recordables


class SpikeRecorder3(Recorder3):

    def __new__(cls):
        recorder = super(SpikeRecorder3, cls).__new__(cls)
        recorder._add_record_type("spikes")
        return recorder


class VRecorder3(Recorder3):

    def __new__(cls):
        recorder = super(VRecorder3, cls).__new__(cls)
        recorder._add_record_type("v")
        return recorder


class GsynRecorder3(Recorder3):

    def __new__(cls):
        recorder = super(GsynRecorder3, cls).__new__(cls)
        recorder._add_record_type("gsyn")
        return recorder


class Three(SpikeRecorder3, VRecorder3, GsynRecorder3):
    pass


three = Three()
print three.recordable


class WithIter(object):

    @property
    def recordable(self):
        ("one", "two", "three").__iter__()


a = WithIter()
print a.recordable
