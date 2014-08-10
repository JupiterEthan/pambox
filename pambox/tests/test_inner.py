# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import csv
import os.path
import pytest
import numpy as np
from scipy import io as sio, io
from pambox import inner
import scipy.io as sio
from numpy.testing import assert_allclose


__DATA_ROOT__ = os.path.join(os.path.dirname(__file__), 'data')


def test_lowpass_filtering_of_envelope():
    mat = sio.loadmat(__DATA_ROOT__ + "/test_hilbert_env_and_lp_filtering_v1.mat",
                      squeeze_me=True)
    envelope = mat['unfiltered_env']
    target = mat['lp_filtered_env']
    filtered_envelope = inner.lowpass_env_filtering(envelope, 150., 1, 22050.)
    assert_allclose(filtered_envelope, target, atol=1e-7)


def test_erb():
    bw = inner.erbbw(1000)
    assert_allclose(bw, 132.63, rtol=1e-4)


def test_GammatoneFilterbank_filtering():
    from itertools import product
    mat = sio.loadmat(__DATA_ROOT__ + '/test_GammatoneFilterbank_filtering.mat',
                        squeeze_me=True)
    cf = [63, 1000]
    fs = [22050, 44100]
    for c, f in product(cf, fs):
        g = inner.GammatoneFilterbank(c, f)
        y = g.filter(mat['x'])
        target_file = 'y_%d_%d' % (f, c)
        np.testing.assert_allclose(y[0], mat[target_file])


def test_third_octave_filtering_of_noise_():
    with open(os.path.join(__DATA_ROOT__,
                           'test_third_octave_filtering_of_noise.csv')) as \
            csv_file:
        pass
        data_file = csv.reader(csv_file)
        temp = next(data_file)
        n_samples = int(temp[0])
        x = np.empty(n_samples)

        for i, s in enumerate(data_file):
            x[i] = np.asarray(s, dtype=np.float)

    target = np.array([ 151.66437785,  688.6881118 ])
    center_f = [63, 125]
    fs = 22050
    rms_out = inner.noctave_filtering(x, center_f, fs, width=3)
    assert_allclose(rms_out, target, rtol=1e-4)


def test_mod_filtering_for_simple_signal():
    signal = np.asarray([1, 0, 1, 0, 1])
    fs = 2205
    modf = np.asarray([1., 2., 4., 8., 16., 32., 64.])
    p, _ = inner.mod_filterbank(signal, fs, modf)
    target = np.asarray([6.69785298e-18, 6.06375859e-06, 2.42555385e-05,
                         9.70302212e-05, 3.88249957e-04, 1.55506496e-03,
                         6.25329663e-03])
    assert_allclose(p, target, rtol=1e-2)
