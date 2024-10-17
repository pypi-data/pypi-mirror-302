import pytest
import numpy as np
from scipy.stats import multivariate_normal as mvn

from gprob import normal, hstack
from gprob.func import logp, logp_lstsq, dlogp, d2logp, fisher

from reffunc import logp as logp_
from reffunc import dlogp_eigh as dlogp_
from reffunc import d2logp as d2logp_


np.random.seed(0)


def num_dlogp(x, m, cov, dm, dcov, delta=1e-7):
    """Finite-difference implementation of the gradient of the log probability 
    density."""

    npar = dcov.shape[0]

    g = []
    for i in range(npar):
        m_plus = m + dm[i] * delta
        m_minus = m - dm[i] * delta
        cov_plus = cov + dcov[i] * delta
        cov_minus = cov - dcov[i] * delta

        fp = logp(x, m_plus, cov_plus)
        fm = logp(x, m_minus, cov_minus)

        g.append((fp-fm) / (2 * delta))

    return np.array(g)


def num_d2logp(x, m, cov, dm, dcov, d2m, d2cov, delta=1e-10):
    """Finite-difference implementation of the Hessian of the log probability 
    density."""

    npar = dcov.shape[0]

    h = []
    for i in range(npar):
        m_plus = m + dm[i] * delta
        m_minus = m - dm[i] * delta
        cov_plus = cov + dcov[i] * delta
        cov_minus = cov - dcov[i] * delta
        dm_plus = dm + d2m[i] * delta
        dm_minus = dm - d2m[i] * delta
        dcov_plus = dcov + d2cov[i] * delta
        dcov_minus = dcov - d2cov[i] * delta

        fp = dlogp(x, m_plus, cov_plus, dm_plus, dcov_plus)
        fm = dlogp(x, m_minus, cov_minus, dm_minus, dcov_minus)

        h.append((fp-fm) / (2 * delta))

    return np.array(h)


def random_d(sz):
    """Random covariance matrix, mean, and sample."""
    mat1 = 2 * np.random.rand(sz, sz) - 1
    msq1 = mat1 @ mat1.T
    
    v = 2 * np.random.rand(sz) - 1
    v1 = 2 * np.random.rand(sz) - 1

    return v, v1, msq1  # x, m, cov


def random_d1(sz, npar):
    """Random matrices for testing formulas using 1st derivatives."""

    mat2 = 2 * np.random.rand(npar, sz, sz) - 1
    msq2 = np.einsum('ijk, ilk -> ijl', mat2, mat2)
    v2 = 2 * np.random.rand(npar, sz) - 1

    return random_d(sz) + (v2, msq2)  # x, m, cov, dm, dcov


def random_d2(sz, npar):
    """Random matrices for testing formulas using 2nd derivatives."""

    mat3 = 2 * np.random.rand(npar, npar, sz, sz) - 1
    msq3 = np.einsum('ijkl, ijrl -> ijkr', mat3, mat3)
    msq3 = msq3.transpose(1, 0, 2, 3) + msq3  # Symmetrizes the Hessian of m

    v3 = 2 * np.random.rand(npar, npar, sz) - 1
    v3 = v3.transpose(1, 0, 2) + v3  # Symmetrizes the Hessian of cov

    return random_d1(sz, npar) + (v3, msq3)  # x, m, cov, dm, dcov, d2m, d2cov


def test_logp():
    tol = 1e-7  # The actual errors should be in 1e-8 range or below

    v, v1, msq1 = random_d(200)
    llk = logp(v, v1, msq1)
    ref_llk = logp_(v, v1, msq1)
    ref_llk2 = mvn.logpdf(v, v1, msq1)

    assert np.abs((llk - ref_llk)/ref_llk) < tol
    assert np.abs((llk - ref_llk2)/ref_llk2) < tol

    v, v1, msq1 = random_d(20)
    llk = logp(v, v1, msq1)
    ref_llk = logp_(v, v1, msq1)
    ref_llk2 = mvn.logpdf(v, v1, msq1)

    assert np.abs((llk - ref_llk)/ref_llk) < tol
    assert np.abs((llk - ref_llk2)/ref_llk2) < tol

    v, v1, msq1 = random_d(41)
    llk = logp(v, v1, msq1)
    ref_llk = logp_(v, v1, msq1)
    ref_llk2 = mvn.logpdf(v, v1, msq1)

    assert np.abs((llk - ref_llk)/ref_llk) < tol
    assert np.abs((llk - ref_llk2)/ref_llk2) < tol

    v, v1, msq1 = random_d(400)
    llk = logp(v, v1, msq1)
    ref_llk = logp_(v, v1, msq1)
    ref_llk2 = mvn.logpdf(v, v1, msq1)

    assert np.abs((llk - ref_llk)/ref_llk) < tol
    assert np.abs((llk - ref_llk2)/ref_llk2) < tol


def test_logp_lstsq():
    # Tests logp_lstsq with non-singular matrices. The singular case is covered 
    # by test_normal.

    tol = 1e-7

    v, v1, msq1 = random_d(41)
    llk = logp_lstsq(v, v1, msq1)
    ref_llk = mvn.logpdf(v, v1, msq1)

    assert np.abs((llk - ref_llk)/ref_llk) < tol
    assert llk.shape == tuple()

    v_, v1, msq1 = random_d(41)
    vs = [v, v_]
    llk = logp_lstsq(vs, v1, msq1)
    ref_llk = mvn.logpdf(vs, v1, msq1)
    assert np.max(np.abs((llk - ref_llk)/ref_llk)) < tol
    assert llk.shape == (2,)


def test_dlogp():
    num_tol = 1e-3
    ref_tol = 1e-7

    v, v1, msq1, v2, msq2 = random_d1(200, 10)
    g = dlogp(v, v1, msq1, v2, msq2)
    num_g = num_dlogp(v, v1, msq1, v2, msq2, delta=1e-9)
    ref_g = dlogp_(v, v1, msq1, v2, msq2)

    assert np.abs((g - num_g)/num_g).max() < num_tol
    assert np.abs((g - ref_g)/ref_g).max() < ref_tol

    v, v1, msq1, v2, msq2 = random_d1(20, 3)
    g = dlogp(v, v1, msq1, v2, msq2)
    num_g = num_dlogp(v, v1, msq1, v2, msq2, delta=1e-9)
    ref_g = dlogp_(v, v1, msq1, v2, msq2)

    assert np.abs((g - num_g)/num_g).max() < num_tol
    assert np.abs((g - ref_g)/ref_g).max() < ref_tol

    v, v1, msq1, v2, msq2 = random_d1(40, 100)
    g = dlogp(v, v1, msq1, v2, msq2)
    num_g = num_dlogp(v, v1, msq1, v2, msq2, delta=1e-9)
    ref_g = dlogp_(v, v1, msq1, v2, msq2)

    assert np.abs((g - num_g)/num_g).max() < num_tol
    assert np.abs((g - ref_g)/ref_g).max() < ref_tol

    v, v1, msq1, v2, msq2 = random_d1(401, 1)
    g = dlogp(v, v1, msq1, v2, msq2)
    num_g = num_dlogp(v, v1, msq1, v2, msq2, delta=1e-9)
    ref_g = dlogp_(v, v1, msq1, v2, msq2)

    assert np.abs((g - num_g)/num_g).max() < num_tol
    assert np.abs((g - ref_g)/ref_g).max() < ref_tol


def test_d2logp():
    num_tol = 1e-4  # The actual errors are typically around or below 1e-5
    ref_tol = 1e-7

    v, v1, msq, v2, msq2, v3, msq3 = random_d2(200, 10)
    h = d2logp(v, v1, msq, v2, msq2, v3, msq3)
    num_h = num_d2logp(v, v1, msq, v2, msq2, v3, msq3, delta=1e-10)
    ref_h = d2logp_(v, v1, msq, v2, msq2, v3, msq3)
    
    assert np.abs((h - num_h)/num_h).max() < num_tol
    assert np.abs((h - ref_h)/ref_h).max() < ref_tol

    v, v1, msq, v2, msq2, v3, msq3 = random_d2(20, 3)
    h = d2logp(v, v1, msq, v2, msq2, v3, msq3)
    num_h = num_d2logp(v, v1, msq, v2, msq2, v3, msq3, delta=1e-10)
    ref_h = d2logp_(v, v1, msq, v2, msq2, v3, msq3)
    
    assert np.abs((h - num_h)/num_h).max() < num_tol
    assert np.abs((h - ref_h)/ref_h).max() < ref_tol

    v, v1, msq, v2, msq2, v3, msq3 = random_d2(40, 100)
    h = d2logp(v, v1, msq, v2, msq2, v3, msq3)
    num_h = num_d2logp(v, v1, msq, v2, msq2, v3, msq3, delta=1e-10)
    ref_h = d2logp_(v, v1, msq, v2, msq2, v3, msq3)
    
    assert np.abs((h - num_h)/num_h).max() < num_tol
    assert np.abs((h - ref_h)/ref_h).max() < ref_tol

    v, v1, msq, v2, msq2, v3, msq3 = random_d2(400, 1)
    h = d2logp(v, v1, msq, v2, msq2, v3, msq3)
    num_h = num_d2logp(v, v1, msq, v2, msq2, v3, msq3, delta=1e-10)
    ref_h = d2logp_(v, v1, msq, v2, msq2, v3, msq3)
    
    assert np.abs((h - num_h)/num_h).max() < num_tol
    assert np.abs((h - ref_h)/ref_h).max() < ref_tol


def test_fisher():
    # Test via random sampling based on the formula
    # FI[i, j] = <dlogp/dtheta_i * dlogp/dtheta_j>

    _, v1, msq1, v2, msq2 = random_d1(20, 5)
    
    xi = normal(v1, msq1)
    ns = 10**3
    samples = xi.sample(ns)

    dllk = np.array([dlogp(s, v1, msq1, v2, msq2) for s in samples])
    fi = fisher(msq1, v2, msq2)

    assert np.mean(np.abs((fi - dllk.T @ dllk / ns) / np.abs(fi))) < 0.2


def test_logp_batch():
    # Validation of the log likelihood calculation, batch version.

    nc = np.log(1/np.sqrt(2 * np.pi))  # Normalization constant.
    
    # Scalar variables
    xi = normal()
    m, cov = xi.mean(), xi.cov()
    assert logp(0, m, cov) == nc
    assert (logp([0], m, cov) == np.array([nc])).all()
    assert (logp([0, 0], m, cov) == np.array([nc, nc])).all()
    
    with pytest.raises(ValueError): 
        logp([[0], [0]], m, cov)
    
    assert logp(2, m, cov) == -4/2 + nc
    assert (logp([0, 1.1], m, cov) == [nc, -1.1**2/2 + nc]).all()

    with pytest.raises(ValueError):
        logp([[0, 1]], m, cov)

    xi = normal(0.9, 3.3)
    m, cov = xi.mean(), xi.cov()
    assert logp(2, m, cov) == (-(2-0.9)**2/(2 * 3.3)
                                     + np.log(1/np.sqrt(2 * np.pi * 3.3)))

    # Vector variables
    xi = normal(0.9, 3.3, size=2)
    m, cov = xi.mean(), xi.cov()

    res = (-(2-0.9)**2/(2 * 3.3)-(1-0.9)**2/(2 * 3.3) 
           + 2 * np.log(1/np.sqrt(2 * np.pi * 3.3)))
    
    assert logp([2, 1], m, cov) == res
    
    res = [-(3.2-0.9)**2/(2 * 3.3)-(1.2-0.9)**2/(2 * 3.3) 
           + 2 * np.log(1/np.sqrt(2 * np.pi * 3.3)), 
           -(-1-0.9)**2/(2 * 3.3)-(-2.2-0.9)**2/(2 * 3.3) 
           + 2 * np.log(1/np.sqrt(2 * np.pi * 3.3))]

    assert (logp([[3.2, 1.2], [-1., -2.2]], m, cov) == np.array(res)).all()

    xi = normal(0.9, 3.3, size=2)
    m, cov = xi.mean(), xi.cov()
    with pytest.raises(ValueError):
        logp(0, m, cov)
    with pytest.raises(ValueError):
        logp([0, 0, 0], m, cov)
    with pytest.raises(ValueError):
        logp([[0], [0]], m, cov)
    with pytest.raises(ValueError):
        logp([[0, 0, 0]], m, cov)

    # Degenerate cases.

    # Deterministic variables.
    xi = hstack([normal(), 1])
    m, cov = xi.mean(), xi.cov()
    assert logp([0, 1.1], m, cov) == float("-inf")
    assert (logp([[0, 1.1]], m, cov) == np.array([float("-inf")])).all()
    assert logp([0, 1.], m, cov) == nc
    assert (logp([[0, 1], [1.1, 1], [0, 2]], m, cov) == 
            [nc, -(1.1)**2/(2) + nc, float("-inf")]).all()
    
    # Degenerate covariance matrix. 
    xi1 = normal()
    xi2 = 0 * normal()
    xi12 = hstack([xi1, xi2])
    m, cov = xi12.mean(), xi12.cov()
    assert logp([1.2, 0], m, cov) == -(1.2)**2/(2) + nc
    assert logp([1.2, 0.1], m, cov) == float("-inf")
    assert (logp([[1, 0.1]], m, cov) == np.array([float("-inf")])).all()
    assert (logp([[1, 0.1], [1.2, 0]], m, cov) == 
            [float("-inf"), -(1.2)**2/(2) + nc]).all()
    
    # Integrals of the probability density
    xi = normal(0, 3.3)
    m, cov = xi.mean(), xi.cov()
    npt = 200000
    ls = np.linspace(-10, 10, npt)
    err = np.abs(1 - np.sum(np.exp(logp(ls, m, cov))) * (20)/ npt)
    assert err < 6e-6  # should be 5.03694e-06

    xi = normal(0, [[2.1, 0.5], [0.5, 1.3]])
    m, cov = xi.mean(), xi.cov()
    npt = 1000
    ls = np.linspace(-7, 7, npt)
    points = [(x, y) for x in ls for y in ls]
    err = np.abs(1 - np.sum(np.exp(logp(points, m, cov))) * ((14)/ npt)**2)
    assert err < 2.5e-3  # should be 0.00200