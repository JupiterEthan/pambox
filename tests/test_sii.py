# -*- coding: utf-8 -*-
from __future__ import division, print_function
from pandas import read_csv
from pambox.intelligibility_models import sii
from numpy import ones
from numpy.testing import assert_allclose
from tests import __DATA_ROOT__



def test_sii():
    """@todo: Docstring for test_sii.
    :returns: @todo

    """
    data = read_csv(__DATA_ROOT__ + '/test_sii.csv')
    for _, E, N, T, I, SII in data.itertuples():
        s = sii.Sii(T=T*ones(18), I=I)
        ss = s.predict(E*ones(18), N*ones(18))
        assert_allclose(ss, SII, rtol=1e-4)

