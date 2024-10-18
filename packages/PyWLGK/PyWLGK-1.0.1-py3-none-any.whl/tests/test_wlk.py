import numpy as np
import pytest
from grakel import WeisfeilerLehman

from pywlgk import wlk
from tests.utils import to_grakel, read, get_dummy_equal, get_dummy_unequal


@pytest.mark.parametrize("normalize", [True, False])
def test_art_equal(normalize: bool):
    (adj1, l1), (adj2, l2) = get_dummy_equal()
    res_pywlgk = wlk([adj1, adj2], [l1, l2], 4, normalize=normalize)
    res_grakel = WeisfeilerLehman(n_iter=4, normalize=normalize).fit_transform([to_grakel(adj1, l1), to_grakel(adj2, l2)])
    assert np.allclose(res_pywlgk, res_grakel)


@pytest.mark.parametrize("normalize", [True, False])
def test_art_unequal(normalize: bool):
    (adj1, l1), (adj2, l2) = get_dummy_unequal()
    res_pywlgk = wlk([adj1, adj2], [l1, l2], 4, normalize=normalize)
    res_grakel = WeisfeilerLehman(n_iter=4, normalize=normalize).fit_transform([to_grakel(adj1, l1), to_grakel(adj2, l2)])
    assert np.allclose(res_pywlgk, res_grakel)


@pytest.mark.parametrize("normalize", [True, False])
def test_prot_equal(normalize: bool):
    (adj1, l1), (adj2, l2) = read("data/1CYN_A.pdb")[1], read("data/1CYN_A.pdb")[1]
    res_pywlgk = wlk([adj1, adj2], [l1, l2], 4, normalize=normalize)
    res_grakel = WeisfeilerLehman(n_iter=4, normalize=normalize).fit_transform([to_grakel(adj1, l1), to_grakel(adj2, l2)])
    assert np.allclose(res_pywlgk, res_grakel)


@pytest.mark.parametrize("normalize", [True, False])
def test_prot_unequal(normalize: bool):
    (adj1, l1), (adj2, l2) = read("data/1CYN_A.pdb")[1], read("data/1XO7_A.pdb")[1]
    res_pywlgk = wlk([adj1, adj2], [l1, l2], 4, normalize=normalize)
    res_grakel = WeisfeilerLehman(n_iter=4, normalize=normalize).fit_transform([to_grakel(adj1, l1), to_grakel(adj2, l2)])
    assert np.allclose(res_pywlgk, res_grakel)
