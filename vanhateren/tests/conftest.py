import os

import pytest


class Plotter(object):
    def __init__(self, request):
        self.dirname = 'tests.plots'
        self.module_name = request.module.__name__
        self.function_name = request.function.__name__
        self.ext = 'pdf'

    @property
    def path(self):
        filename = "%s.%s.%s" % (
            self.module_name, self.function_name, self.ext)
        return os.path.join(self.dirname, filename)

    def __enter__(self):
        import matplotlib.pyplot as plt
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)
        return plt

    def __exit__(self, type, value, traceback):
        import matplotlib.pyplot as plt
        plt.savefig(self.path)
        plt.close('all')


@pytest.fixture
def plt(request):
    plotter = Plotter(request)
    request.addfinalizer(lambda: plotter.__exit__(None, None, None))
    return plotter.__enter__()
