class PylabMock():

    def __init__(self, message):
        self._message = message

    def figure(self, num=None,  # autoincrement if None, else integer from 1-N
               figsize=None,  # defaults to rc figure.figsize
               dpi=None,  # defaults to rc figure.dpi
               facecolor=None,  # defaults to rc figure.facecolor
               edgecolor=None,  # defaults to rc figure.edgecolor
               frameon=True, FigureClass=None, **kwargs):
        pass

    def plot(self, *args, **kwargs):
        pass

    def xlabel(self, s, *args, **kwargs):
        pass

    def ylabel(self, s, *args, **kwargs):
        pass

    def title(self, s, *args, **kwargs):
        pass

    def show(self, *args, **kw):
        print "SKIPPING PLOTING AS {}".format(self._message)
