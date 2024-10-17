from importlib import import_module
from functools import reduce
from operator import mul
from warnings import warn

import numpy as np
from numpy.linalg import LinAlgError
from numpy.exceptions import AxisError

from . import normal_
from .normal_ import (Normal, complete, lift, match_, complete_tensordot_axes,
                      validate_logp_samples, print_)
from .func import ConditionError
from .external import einsubs


def iid(x, n=1, axis=0):
    """Creates a sparse array of independent identically distributed 
    copies of ``x`` stacked together along ``axis``.
    
    Args:
        x (random variable): 
            The variable whose distribution is to be copied.
        n (int): 
            The number of copies to be made.
        axis (int): 
            The axis in the final array along which the copies are stacked.

    Returns:
        A sparse normal random variable whose elements along ``axis`` are 
        statistically independent.
    """

    y = lift(SparseNormal, x).icopy()
    
    axis = _normalize_axis(axis, y.ndim + 1)
    sh1 = y.shape[:axis] + (1,) + y.shape[axis:]
    sh2 = y.shape[:axis] + (n,) + y.shape[axis:]

    iaxid = y._iaxid[:axis] + (y._niax + 1,) + y._iaxid[axis:]
    return _finalize(y.reshape(sh1).broadcast_to(sh2), iaxid)


class SparseNormal(Normal):
    """Array of block-independent normal random variables."""

    __slots__ = ("_iaxid",)  
    # iaxid is a tuple of the length ndim indicating the axes along which 
    # the random variables at different indices are independent of each other. 
    # It contains integer ids at positions corresponding to the independence 
    # axes, and ``None``s at the positions corresponding to regular axes.

    _mod = import_module(__name__)

    def __init__(self, a, b, lat=None):
        super().__init__(a, b, lat)
        self._iaxid = (None,) * b.ndim
    
    @property
    def delta(self):
        return _finalize(super().delta, self._iaxid)
    
    @property
    def real(self):
        return _finalize(super().real, self._iaxid)
    
    @property
    def imag(self):
        return _finalize(super().imag, self._iaxid)
    
    @property
    def iaxes(self):
        """Ordered sequence of axes along which the array elements 
        are independent from each other."""
        return tuple([i for i, b in enumerate(self._iaxid) if b])
    
    @property
    def _niax(self):
        return len(self._iaxid) - self._iaxid.count(None)
    
    def __array__(self, dtype=np.object_, copy=False):
        # The application of default numpy.array() to a sparse variable 
        # can silently return an empty array of numeric type, because sparse 
        # variables cannot be iterated over along their independence axes. 

        # ``dtype`` and ``copy`` are for compatibility with array API.
        
        return np.fromiter([self], dtype).reshape(tuple())
    
    def __repr__(self):
        return print_(self, extra_attrs=("iaxes",))
    
    def __neg__(self):
        return _finalize(super().__neg__(), self._iaxid)

    def __add__(self, other):
        iaxid = _validate_iaxid([self, other])
        return _finalize(super().__add__(other), iaxid)

    def __mul__(self, other):
        iaxid = _validate_iaxid([self, other])
        return _finalize(super().__mul__(other), iaxid)

    def __truediv__(self, other):
        iaxid = _validate_iaxid([self, other])
        return _finalize(super().__truediv__(other), iaxid)

    def __rtruediv__(self, other):
        iaxid = _validate_iaxid([self, other])
        return _finalize(super().__rtruediv__(other), iaxid)

    def __matmul__(self, other):
        try:
            other, isnumeric = match_(self.__class__, other)
        except TypeError:
            return NotImplemented

        if not isnumeric:
            return self @ other.b + self.b @ other.delta
        
        x = super().__matmul__(other)
        
        if self._iaxid[-1]:
            raise ValueError("Matrix multiplication contracting over "
                             "independence axes is not supported. Axis "
                             f"{self.ndim - 1} of operand 1 is contracted.")

        if other.ndim == 1:
            iaxid = self._iaxid[:-1]
        else:
            iaxid = self._iaxid

        if x.ndim > self.ndim:  # Accounts for broadcasting.
            iaxid = (None,) * (x.ndim - self.ndim) + iaxid

        return _finalize(x, iaxid)

    def __rmatmul__(self, other):
        try:
            other, isnumeric = match_(self.__class__, other)
        except TypeError:
            return NotImplemented

        if not isnumeric:
            return self @ other.b + self.b @ other.delta
        
        x = super().__rmatmul__(other)
        
        if self.ndim == 1:
            op_axis = 0
        else:
            op_axis = self.ndim - 2

        if self._iaxid[op_axis]:
            raise ValueError("Matrix multiplication contracting over "
                             "independence axes is not supported. "
                             f"Axis {op_axis} of operand 2 is contracted.")

        iaxid = self._iaxid

        if other.ndim == 1:
            iaxid = tuple([b for i, b in enumerate(iaxid) if i != op_axis])
        
        if x.ndim > self.ndim:  # Accounts for broadcasting.
            iaxid = (None,) * (x.ndim - self.ndim) + iaxid

        return _finalize(x, iaxid)
    
    def __pow__(self, other):
        iaxid = _validate_iaxid([self, other])
        return _finalize(super().__pow__(other), iaxid)

    def __rpow__(self, other):
        iaxid = _validate_iaxid([self, other])
        return _finalize(super().__rpow__(other), iaxid)
    
    def __getitem__(self, key):
        iaxid = _item_iaxid(self, key)
        return _finalize(super().__getitem__(key), iaxid)
    
    def __setitem__(self, key, value):
        value, isnumeric = match_(self.__class__, value)

        if not isnumeric:
            iaxid = _item_iaxid(self, key)
            val_iaxid = (None,) * (len(iaxid) - value.ndim) + value._iaxid
            
            if val_iaxid != iaxid:
                raise ValueError("The independence axes of the indexing result "
                                 "do not match those of the assigned value.")
            
            # Deterministic values can skip this check, 
            # as their axes are always compatible.
        
        super().__setitem__(key, value)

    def conjugate(self):
        return _finalize(super().conjugate(), self._iaxid)
    
    def cumsum(self, axis):
        """Computes the cumulative sum of the elements.

        Args:
            axis (int): 
                Axis along which the cumulative sum is computed. 
                ``None`` values are not supported.

        Returns:
            A new sparse normal variable representing the result of 
            the cumulative summation with the same dimensions as the input.
        """

        if axis is None:
            # For regular arrays, None is the default value. For sparse arrays, 
            # it is not supported because these arrays usually 
            # cannot be flattened.
            raise ValueError("None value for the axis is not supported.")
        
        axis = _normalize_axis(axis, self.ndim)
        if self._iaxid[axis]:
            raise ValueError("The computation of cumulative sums along "
                             "independence axes is not supported.")

        return _finalize(super().cumsum(axis), self._iaxid)
    
    def diagonal(self, offset=0, axis1=0, axis2=1):
        [axis1, axis2] = _normalize_axes([axis1, axis2], self.ndim)

        if self._iaxid[axis1] or self._iaxid[axis2]:
            raise ValueError("Taking diagonals along independence axes "
                             "is not supported.")
        s = {axis1, axis2}
        iaxid = (tuple([idx for i, idx in enumerate(self._iaxid) if i not in s]) 
                 + (None,))
        return _finalize(super().diagonal(offset, axis1, axis2), iaxid)

    def flatten(self, order="C"):
        if not any(self._iaxid):  # This covers the case of self.ndim == 0.
            return _finalize(super().flatten(order=order), (None,))
        
        if self.ndim == 1:
            return _finalize(super().flatten(order=order), self._iaxid)
        
        # Checks if all dimensions except maybe one are <= 1.
        max_sz = max(self.shape)
        max_dim = self.shape.index(max_sz)
        if all(x <= 1 for i, x in enumerate(self.shape) if i != max_dim):
            iaxid = (self._iaxid[max_dim],)
            return _finalize(super().flatten(order=order), iaxid)
        
        raise ValueError("Sparse normal variables can only be flattened if "
                         "all their dimensions except maybe one have size <=1, "
                         "or they have no independence axes.")
    
    def moveaxis(self, source, destination):
        source = _normalize_axis(source, self.ndim)
        destination = _normalize_axis(destination, self.ndim)
        
        iaxid = list(self._iaxid)
        iaxid.insert(destination, iaxid.pop(source))
        iaxid = tuple(iaxid)

        return _finalize(super().moveaxis(source, destination), iaxid)
    
    def ravel(self, order="C"):
        if not any(self._iaxid):  # This covers the case of self.ndim == 0.
            return _finalize(super().ravel(order=order), (None,))
        
        if self.ndim == 1:
            return _finalize(super().ravel(order=order), self._iaxid)
        
        # Checks if all dimensions except maybe one are <= 1.
        max_sz = max(self.shape)
        max_dim = self.shape.index(max_sz)
        if all(x <= 1 for i, x in enumerate(self.shape) if i != max_dim):
            iaxid = (self._iaxid[max_dim],)
            return _finalize(super().ravel(order=order), iaxid)
        
        raise ValueError("Sparse normal variables can only be flattened if "
                         "all their dimensions except maybe one have size <=1, "
                         "or they have no independence axes.")

    def reshape(self, newshape, order="C"):
        x = super().reshape(newshape, order)  
        # Reshapes the map before the axes check to yield a meaningful 
        # error message if the old and the new shapes are inconsistent.

        newshape = x.shape  # Replaces '-1' if it was in newshape.

        if x.size == 0:
            # The transformation of independence axes for zero-size variables 
            # cannot be determined unambiguously. By our convention,
            # the result of such transformation has no independence axes.
            return _finalize(x, (None,) * x.ndim)

        new_dim = 0

        new_cnt = 1
        old_cnt = 1

        iaxid = [None] * len(newshape)
        for i, n in enumerate(self.shape):
            if self._iaxid[i]:
                if n != 1:
                    # Skips all trivial dimensions first.
                    while new_dim < len(newshape) and newshape[new_dim] == 1:
                        new_dim += 1

                if (new_dim < len(newshape) and newshape[new_dim] == n 
                    and new_cnt == old_cnt):
                    
                    iaxid[new_dim] = self._iaxid[i]
                else:
                    raise ValueError("Reshaping that affects independence axes "
                                     f"is not supported. Axis {i} is affected "
                                     "by the requested shape transformation "
                                     f"{self.shape} -> {newshape}.")
                old_cnt *= n
                new_cnt *= newshape[new_dim]
                new_dim += 1
            else:
                old_cnt *= n

                while new_cnt < old_cnt:
                    new_cnt *= newshape[new_dim]
                    new_dim += 1
        
        iaxid = tuple(iaxid)
        return _finalize(x, iaxid)
    
    def squeeze(self, axis=None):
        if axis is None:
            axis = tuple([i for i, s in enumerate(self.shape) if s == 1])
        elif isinstance(axis, int):
            axis = (axis,)

        axis = _normalize_axes(axis, self.ndim)
        iaxid = tuple([b for i, b in enumerate(self._iaxid) if i not in axis])
        return _finalize(super().squeeze(axis), iaxid)

    def sum(self, axis, keepdims=False):
        """Computes the sum of all elements of the variable along an axis 
        or axes.

        Args:
            axis (int, tuple of int): 
                Axis or axes along which to sum the elements. 
                ``None`` is not supported.
            keepdims (bool):
                If ``True``, the reduced axes are retained in the output 
                as dimensions with size one. This enables the result 
                to broadcast against the input array.

        Returns:
            A new sparse normal variable representing the result of 
            the summation. The output variable has the same dimensions as 
            the input, except the summation axes are removed unless 
            ``keepdims`` is ``True``.
        """

        if not isinstance(axis, int) and not isinstance(axis, tuple):
            raise ValueError("`axis` must be an integer or "
                             "a tuple of integers.")
            # None, the default value for non-sparse arrays, is not supported,
            # because in the typical case the variable has at least one 
            # independence axis that cannot be contracted.

        sum_axes = _normalize_axes(axis, self.ndim)

        if any(self._iaxid[ax] for ax in sum_axes):
            raise ValueError("The computation of sums along "
                             "independence axes is not supported.")
        if keepdims:
            iaxid = self._iaxid
        else:
            iaxid = tuple([b for i, b in enumerate(self._iaxid) 
                           if i not in sum_axes])

        return _finalize(super().sum(axis, keepdims), iaxid)

    def transpose(self, axes=None):
        if axes is None:
            iaxid = self._iaxid[::-1]
        else:
            iaxid = tuple([self._iaxid[ax] for ax in axes])

        return _finalize(super().transpose(axes), iaxid)
    
    def trace(self, offset=0, axis1=0, axis2=1):
        [axis1, axis2] = _normalize_axes([axis1, axis2], self.ndim)

        if self._iaxid[axis1] or self._iaxid[axis2]:
            raise ValueError("Traces along independence axes "
                             "are not supported.")
        s = {axis1, axis2}
        iaxid = tuple([b for i, b in enumerate(self._iaxid) if i not in s])
        return _finalize(super().trace(offset, axis1, axis2), iaxid)
    
    def split(self, indices_or_sections, axis=0):
        axis = _normalize_axis(axis, self.ndim)

        if self._iaxid[axis]:
            raise ValueError("Splitting along independence axes "
                             "is not supported.")
        
        xs = super().split(indices_or_sections, axis)
        return [_finalize(x, self._iaxid) for x in xs]
    
    def broadcast_to(self, shape):
        iaxid = (None,) * (len(shape) - self.ndim) + self._iaxid
        return _finalize(super().broadcast_to(shape), iaxid)

    def icopy(self):
        return _finalize(super().icopy(), self._iaxid)

    def condition(self, observations):
        """Conditioning operation. Applicable between variables having the same 
        numbers and sizes of independence axes.
        
        Args:
            observations (SparseNormal or dict):
                A single sparse normal variable or a dictionary
                of observations of the format 
                ``{variable: value, ...}``, where the variables are 
                sparse normal variables, and the values are numeric 
                constants or sparse normal variables. A single sparse normal 
                variable is equavalent to ``{variable: 0}``.
        
        Returns:
            Conditional sparse normal variable with the same shape as 
            the original variable.

        Raises:
            ConditionError: If conditions are degenerate.
        """

        if isinstance(observations, dict):
            obs = [lift(SparseNormal, k-v) for k, v in observations.items()]
        else:
            obs = [lift(SparseNormal, observations)]

        niax = self._niax  # A shorthand.

        # Moves the sparse axes first, reordering them in increasing order,
        # and flattens the dense subspaces.

        s_sparse_ax = [i for i, b in enumerate(self._iaxid) if b]
        s_dense_ax = [i for i, b in enumerate(self._iaxid) if not b]
        dense_sz = reduce(mul, [self.shape[i] for i in s_dense_ax], 1)

        self_fl = self.transpose(tuple(s_sparse_ax + s_dense_ax))
        self_fl = self_fl.reshape(self_fl.shape[:niax] + (dense_sz,))

        mismatch_w_msg = ("Conditions with different numbers or sizes of "
                          "independence axes compared to `self` are ignored. "
                          "The consistency of such conditions is not checked.")
        obs_flat = []
        iax_ord = [i for i in self._iaxid if i]
        for c in obs:
            if c._niax != niax:
                warn(mismatch_w_msg, SparseConditionWarning)
                continue

            sparse_ax = [c._iaxid.index(i) for i in iax_ord]
            dense_ax = [i for i, b in enumerate(c._iaxid) if not b]
            dense_sz = reduce(mul, [c.shape[i] for i in dense_ax], 1)
            
            c = c.transpose(tuple(sparse_ax + dense_ax))
            c = c.reshape(c.shape[:niax] + (dense_sz,))

            if c.shape[:niax] != self_fl.shape[:niax]:
                warn(mismatch_w_msg, SparseConditionWarning)
                continue

            if c.iscomplex:
                obs_flat.extend([c.real, c.imag])
            else:
                obs_flat.append(c)

        if not obs_flat:
            return self

        # Combines the observations in one and completes them w.r.t. self.
        cond = concatenate(SparseNormal, obs_flat, axis=-1)
        lat, [av, ac] = complete([self_fl, cond])

        t_ax = tuple(range(1, niax+1)) + (0, -1)

        av = av.transpose(t_ax)
        mv = self_fl.mean()
        if self.iscomplex:
            av = np.concatenate([av.real, av.imag], axis=-1)
            mv = np.concatenate([mv.real, mv.imag], axis=-1)

        ac = ac.transpose(t_ax)
        mc = cond.mean()

        # The calculation of the conditional map and mean.

        q, r = np.linalg.qr(ac, mode="reduced")

        # If there are zero diagonal elements in the triangular matrix, 
        # some colums of ``ac`` are linearly dependent.
        dia_r = np.abs(np.diagonal(r, axis1=-1, axis2=-2))
        tol = np.finfo(r.dtype).eps
        if (dia_r < (tol * np.max(dia_r))).any():
            raise ConditionError("Degenerate conditions are not supported "
                                 "for sparse varaibles.")

        t_ax = tuple(range(niax)) + (-1, -2)

        try:
            es = np.linalg.solve(r.transpose(t_ax), -mc[..., None]).squeeze(-1)
        except LinAlgError as e:
            raise ConditionError(str(e))
        
        aproj = q.transpose(t_ax) @ av

        cond_a = av - q @ aproj
        cond_m = mv + np.einsum("...i, ...ij -> ...j", es, aproj)

        # Transposing and shaping back.

        t_ax = (-2,) + tuple(range(niax)) + (-1,)
        cond_a = cond_a.transpose(t_ax)

        if self.iscomplex:
            # Converting back to complex.
            n = cond_m.shape[-1] // 2
            cond_a = cond_a[..., :n] + 1j * cond_a[..., n:]
            cond_m = cond_m[..., :n] + 1j * cond_m[..., n:]

        fcv = SparseNormal(cond_a, cond_m, lat)

        dense_sh = tuple([n for n, i in zip(self.shape, self._iaxid) if not i])
        fcv = fcv.reshape(fcv.shape[:niax] + dense_sh)
        t_ax = tuple([i[0] for i in sorted(enumerate(s_sparse_ax + s_dense_ax), 
                                           key=lambda x:x[1])])

        return _finalize(fcv.transpose(t_ax), self._iaxid)

    def cov(self):
        """Covariance, generalizing ``<outer((x-<x>), (x-<x>)^H)>``, 
        where ``H`` denotes conjugate transposition, and ``<...>`` is 
        the expectation value of ``...``.

        Returns:
            An array with the dimension number equal to the doubled 
            number of the regular dimensions of the variable, plus 
            the undoubled number of its sparse (independence) dimensions. 
            In the returned array, the regular dimensions 
            go first in the order they appear in the variable shape, 
            and the independence dimensions are appended at the end.
            The resulting structure is the same as the structure produced 
            by repeated applications of `np.diagonal` over all the 
            independence dimensions of the full-sized covariance matrix ``c``,
            ``c[ijk... lmn...] = <(x[ijk..] - <x>)(x[lmn..] - <x>)*>``, 
            where ``ijk...`` and ``lmn...`` are indices that run over 
            the elements of the variable (here ``x``), 
            and ``*`` denotes complex conjugation.

        Examples:
            >>> v = iid(normal(size=(3,)), 4)
            >>> v.shape
            (4, 3)
            >>> v.cov().shape
            (3, 3, 4)

            >>> v = iid(normal(size=(3, 2)), 4)
            >>> v = iid(v, 5)
            >>> v.shape
            (5, 4, 3, 2)
            >>> v.cov().shape
            (3, 2, 3, 2, 5, 4)
        """

        symb = [einsubs.get_symbol(i) for i in range(2 * self.ndim + 1)]
        elem_symb = symb[0]
        out_symb = symb[1:]

        in_symb1 = out_symb[:self.ndim]
        in_symb2 = out_symb[self.ndim:]

        for i in self.iaxes:
            out_symb.remove(in_symb2[i])
            out_symb.remove(in_symb1[i])
            out_symb.append(in_symb1[i])

            in_symb2[i] = in_symb1[i]
        
        # Adds the symbol for the summation over the latent variables.
        in_symb1.insert(0, elem_symb)
        in_symb2.insert(0, elem_symb)

        subs = f"{''.join(in_symb1)},{''.join(in_symb2)}->{''.join(out_symb)}"
        return np.einsum(subs, self.a, self.a.conj())

    def sample(self, n=None):
        if n is None:
            nsh = tuple()
        else:
            nsh = (n,)

        iaxsh = [m for m, b in zip(self.shape, self._iaxid) if b]
        r = np.random.normal(size=(*nsh, *iaxsh, self.a.shape[0]))

        symb = [einsubs.get_symbol(i) for i in range(self.ndim + 1 + len(nsh))]
        
        elem_symb = symb[0]
        out_symb = symb[1:]

        in_symb1 = out_symb[:len(nsh)]
        in_symb2 = out_symb[len(nsh):]

        in_symb1.extend(in_symb2[i] for i in self.iaxes)
        in_symb1.append(elem_symb)

        in_symb2.insert(0, elem_symb)

        subs = f"{''.join(in_symb1)},{''.join(in_symb2)}->{''.join(out_symb)}"
        return np.einsum(subs, r, self.a) + self.mean()
        

    def logp(self, x):
        delta_x = x - self.mean()
        validate_logp_samples(self, delta_x)

        if self.iscomplex:
            delta_x = np.stack([delta_x.real, delta_x.imag], axis=-1)
            self = stack(SparseNormal, [self.real, self.imag], axis=-1)
        elif np.iscomplexobj(delta_x):
            # Casts to real with a warning.
            delta_x = delta_x.astype(delta_x.real.dtype)

        niax = self._niax
        
        if self.ndim == niax:
            # Scalar dense subspace.

            sigmasq = np.einsum("i..., i... -> ...", self.a, self.a)
            llk = -0.5 * (delta_x**2 / sigmasq + np.log(2 * np.pi * sigmasq))
            return np.sum(llk, axis=tuple(range(-self.ndim, 0)))
        
        # In the remaining, the dimensionality of the dense subspace is >= 1.

        batch_dim = delta_x.ndim - self.ndim
        if not batch_dim:
            delta_x = delta_x[None, ...]

        nsamples = len(delta_x)

        # Moves the sparse axes to the beginning and the batch axis to the end.
        sparse_ax = [i + 1 for i, b in enumerate(self._iaxid) if b]
        dense_ax = [i + 1 for i, b in enumerate(self._iaxid) if not b]

        delta_x = delta_x.transpose(tuple(sparse_ax + dense_ax + [0]))

        # Covariance with the sparse axes first.
        cov = self.cov()
        t = tuple(range(cov.ndim))        
        cov = cov.transpose(t[cov.ndim - niax:] + t[:cov.ndim - niax])

        # Flattens the dense subspace.
        dense_sh = [n for n, i in zip(self.shape, self._iaxid) if not i]
        dense_sz = reduce(mul, dense_sh, 1)

        cov = cov.reshape(cov.shape[:niax] + (dense_sz, dense_sz))

        new_x_sh = delta_x.shape[:niax] + (dense_sz,) + (nsamples,)
        delta_x = delta_x.reshape(new_x_sh)

        ltr = np.linalg.cholesky(cov)
        z = np.linalg.solve(ltr, delta_x)

        if not batch_dim:
            z = z.squeeze(-1)
        
        sparse_sz = self.size // dense_sz
        rank = cov.shape[-1] * sparse_sz  # The rank is full.
        log_sqrt_det = np.sum(np.log(np.diagonal(ltr, axis1=-1, axis2=-2)))
        norm = 0.5 * np.log(2 * np.pi) * rank + log_sqrt_det

        idx = "".join([einsubs.get_symbol(i) for i in range(niax + 1)])
        return -0.5 * np.einsum(f"{idx}..., {idx}... -> ...", z, z) - norm


def _finalize(x, iaxid):
    """Assigns ``iaxid`` to ``x`` and return ``x``. The function is used for 
    converting fully-correlated normal variables that have no independence axes 
    to true sparse normal variables."""

    if x is NotImplemented:
        return NotImplemented

    if not isinstance(iaxid, tuple):
            raise ValueError("iaxid must be a tuple, while now it is "
                             f"of type {type(iaxid)}.")
        
    if len(iaxid) != x.ndim:
        raise ValueError(f"The size of iaxid ({len(iaxid)}) does not match "
                         f"the dimension number of the variable ({x.ndim}).")
    
    if not all([i is None or i for i in iaxid]):
        raise ValueError("iaxid can contain only Nones and integers "
                         f"greater than zero, while now it is {iaxid}.")

    x._iaxid = iaxid
    return x


def _normalize_axis(axis, ndim):
    """Ensures that the axis index is positive and within the array dimension.

    Returns:
        Normalized axis index.
    
    Raises:
        AxisError: 
            If the axis is out of range.
    """

    axis = axis.__index__()

    if axis < -ndim or axis > ndim - 1:
        raise AxisError(f"Axis {axis} is out of bounds "
                        f"for an array of dimension {ndim}.")
    if axis < 0:
        axis = ndim + axis

    return axis


def _normalize_axes(axes, ndim):
    """Ensures that the axes indices are positive, within the array dimension,
    and without duplicates.

    Returns:
        Tuple: positive axes indices.
    
    Raises:
        AxisError:
            If one of the axes is out of range.
        ValueError:
            If there are duplicates among the axes.
    """

    # Essentially repeats the code of numpy's normalize_axis_tuple,
    # which does not seem to be part of the public API.

    if type(axes) not in (tuple, list):
        try:
            axes = [axes.__index__()]
        except TypeError:
            pass

    axes = tuple([_normalize_axis(ax, ndim) for ax in axes])

    if len(set(axes)) != len(axes):
        raise ValueError('Axes cannot repeat.')
    
    return axes


def _validate_iaxid(seq):
    """Checks that the independence axes of the sparse normal arrays in ``seq``
    are compatible.
    
    Returns:
        ``iaxid`` of the final shape for the broadcasted arrays.
    """

    seq = [x if hasattr(x, "_iaxid") else lift(SparseNormal, x) for x in seq]
    ndim = max(x.ndim for x in seq)

    # The set of iaxes excluding those of deterministic variables.
    iaxids = set((None,) * (ndim - x.ndim) + x._iaxid 
                 for x in seq if x.nlat != 0)

    if len(iaxids) == 0:
        return (None,) * ndim
    if len(iaxids) == 1:
        return iaxids.pop()
    
    # len > 1, which means that not all independence axes are identical.
    # This is not permitted. To raise an error, the following code determines 
    # if the problem is the number, location, or order of the axes.

    msg = ("Combining sparse normal variables requires them to have "
           "the same numbers of independence axes at the same "
           "positions in the shape and in the same order.")

    ns = set((len(ids) - ids.count(None)) for ids in iaxids)
    if len(ns) > 1:
        valstr = ": " + ", ".join(str(n) for n in ns)
        raise ValueError("Mismatching numbers of independence axes "
                         f"in the operands{valstr}. {msg}")

    get_iax_numbers = lambda ids: tuple([i for i, b in enumerate(ids) if b])
    locs = set(get_iax_numbers(ids) for ids in iaxids)
    if len(locs) > 1:
        valstr = ": " + ", ".join(str(loc) for loc in locs)
        raise ValueError("Incompatible locations of the independence axes "
                         f"of the operands{valstr}. {msg}")

    orders = set(tuple([ax for ax in ids if ax is not None]) for ids in iaxids)
    valstr = ": " + ", ".join(str(order) for order in orders)
    raise ValueError("Incompatible orders of the independence axes "
                     f"of the operands{valstr}. {msg}")
    

def _item_iaxid(x, key):
    """Validates the key and calculates iaxid for the result of the indexing 
    of ``x`` with ``key``.
    
    Args:
        x: 
            Sparse normal variable.
        key: 
            Numpy-syntax array indexing key. Independence axes can only 
            be indexed by full slices ``:`` (explicit or implicit via ellipsis). 
        
    Returns:
        A tuple of iaxids for the indexing result.
    """

    if not isinstance(key, tuple):
        key = (key,)
    
    out_axs = []  # out_axs[i] is the number of the i-th output axis 
                  # in the input shape.
    idx = []  # idx[i] is the index used for the i-th input axis.

    has_ellipsis = False
    used_dim = 0

    for k in key:
        if isinstance(k, int):
            used_dim += 1
            continue

        if isinstance(k, slice):
            idx.append(k)
            out_axs.append(used_dim)
            used_dim += 1
            continue
        
        if k is Ellipsis:
            if has_ellipsis:
                raise IndexError("An index can only have a single "
                                 "ellipsis ('...').")
            
            has_ellipsis = True
            ep_in = used_dim       # ellipsis position in the input
            ep_out = len(out_axs)  # ellipsis position in the output
            continue

        if k is np.newaxis:
            idx.append(None)
            out_axs.append(None)
            continue

        # Advanced indices (int and bool arrays) are not implemented. 

        raise IndexError("Only integers, slices (':'), ellipsis ('...'), "
                         "numpy.newaxis ('None') are valid indices.")
    
    # Checks if any input dimensions remain unconsumed.
    delta = x.ndim - used_dim
    if delta > 0:
        if has_ellipsis:
            for i in range(ep_out, len(out_axs)):
                if out_axs[i] is not None:
                    out_axs[i] += delta

            out_axs[ep_out: ep_out] = range(ep_in, ep_in + delta)
            idx[ep_out: ep_out] = (slice(None) for _ in range(delta))
        else:
            out_axs.extend(range(used_dim, used_dim + delta))
            idx.extend(slice(None) for _ in range(delta))
    elif delta < 0:
        raise IndexError(f"Too many indices: the array is {x.ndim}-dimensional,"
                         f" but {used_dim} indices were given.")
    
    for i, b in enumerate(x._iaxid):
        if i not in out_axs:
            oi = -1
        else:
            oi = out_axs.index(i)
        
        if b and (oi == -1 or idx[oi] != slice(None)):
            raise IndexError("Only full slices (':') and ellipses ('...') "
                             "are valid indices for independence axes. "
                             f"Axis {i} is indexed with an invalid key.")
    
    # Returns iaxid for the indexing result.
    return tuple([None if ax is None else x._iaxid[ax] for ax in out_axs])
    

def cov(x, y):
    """The sparse implementation of the covariance between two variables."""

    def find_det_dense_shape(v, d):
        # Tries resolving what the independence axes of the deterministic 
        # variable ``d`` could be based on the shape and the independence axes 
        # of the sparse variable ``v``. If the resolution is ambiguous 
        # or fails, the function throws an error.

        sparse_shape_v = [s for b, s in zip(v._iaxid, v.shape) if b]
        dense_shape_d = list(d.shape)

        for s in set(sparse_shape_v):
            cnt_v = sparse_shape_v.count(s)
            cnt_d = dense_shape_d.count(s)

            if cnt_d == cnt_v:
                for _ in range(cnt_d):
                    dense_shape_d.remove(s)
            elif cnt_d == 0:
                iax = v.shape.index(s)
                raise ValueError("The shape of the deterministic variable "
                                 f"{d.shape} does not contain a dimension "
                                 f"of size {s} that can correspond to the "
                                 f"independence axis {iax} of the sparse "
                                 f"normal variable with the shape {v.shape}.")
            elif cnt_d < cnt_v:
                raise ValueError("The shape of the deterministic variable "
                                 f"{d.shape} does not contain {cnt_v} "
                                 f"dimensions of size {s} to match the "
                                 "independence axes of the sparse "
                                 f"normal variable with the shape {v.shape}.")
            else:
                # cnt_d > cnt_v
                raise ValueError("The shape of the deterministic variable "
                                 f"{d.shape} contains too many dimensions "
                                 f"of size {s}, which makes their "
                                 "correspondence with the independence axes "
                                 "of the sparse normal variable ambiguous.")
        return dense_shape_d

    if x.nlat == 0 and y.nlat == 0:
        # It is not allowed for both inputs to be deterministic 
        # because the independence axes cannot be determined.

        # This case should never be reached under normal circumstances, 
        # because two constants are dispatched to the dense 
        # implementation of covariance.
        raise ValueError
    
    # If one of x and y is deterministic, a zero result is returned.

    if x.nlat == 0:
        dense_shape_y = [s for b, s in zip(y._iaxid, y.shape) if not b]
        sparse_shape = [s for b, s in zip(y._iaxid, y.shape) if b]
        dense_shape_x = find_det_dense_shape(y, x)

        res_shape = tuple(dense_shape_x + dense_shape_y + sparse_shape)
        dt = np.result_type(x.a, y.a)
        return np.zeros(res_shape, dtype=dt)

    if y.nlat == 0:
        dense_shape_x = [s for b, s in zip(x._iaxid, x.shape) if not b]
        sparse_shape = [s for b, s in zip(x._iaxid, x.shape) if b]
        dense_shape_y = find_det_dense_shape(x, y)

        res_shape = tuple(dense_shape_x + dense_shape_y + sparse_shape)
        dt = np.result_type(x.a, y.a)
        return np.zeros(res_shape, dtype=dt)
    
    # The default case, when both variables are non-deterministic.

    iax_ord_x = [i for i in x._iaxid if i is not None]
    iax_ord_y = [i for i in y._iaxid if i is not None]

    if len(iax_ord_x) != len(iax_ord_y):
        raise ValueError("The numbers of the independence axes "
                         "must coincide for the two operands. "
                         f"Now operand 1 has {len(iax_ord_x)} axes, "
                         f"while operand 2 has {len(iax_ord_y)}.")
    
    if iax_ord_x != iax_ord_y:
        raise ValueError("The orders of the independence axes "
                         "must coincide for the two operands. "
                         f"Now operand 1 has the order {iax_ord_x}, "
                         f"while operand 2 has the order {iax_ord_y}.")

    symb = [einsubs.get_symbol(i) for i in range(x.ndim + y.ndim + 1)]
    elem_symb = symb[0]
    out_symb = symb[1:]

    in_symb1 = out_symb[:x.ndim]
    in_symb2 = out_symb[x.ndim:]

    for i, j in zip(x.iaxes, y.iaxes):
        out_symb.remove(in_symb2[j])
        out_symb.remove(in_symb1[i])
        out_symb.append(in_symb1[i])

        in_symb2[j] = in_symb1[i]
    
    # Adds the symbol for the summation over the latent variables.
    in_symb1.insert(0, elem_symb)
    in_symb2.insert(0, elem_symb)
    
    subs = f"{''.join(in_symb1)},{''.join(in_symb2)}->{''.join(out_symb)}"
    _, [ax, ay] = complete([x, y])
    return np.einsum(subs, ax, ay.conj())


class SparseConditionWarning(RuntimeWarning):
    """The warning issued when a condition is skipped during 
    the conditioning of a sparse variable."""
    pass


def concatenate(cls, arrays, axis=0):
    iaxid = _validate_iaxid(arrays)
    axis = _normalize_axis(axis, len(iaxid))
    
    if iaxid[axis]:
        raise ValueError("Concatenation along independence axes "
                         "is not allowed.")
    
    return _finalize(normal_.concatenate(cls, arrays, axis), iaxid)


def stack(cls, arrays, axis=0):
    iaxid = _validate_iaxid(arrays)
    axis = _normalize_axis(axis, len(iaxid) + 1)
    iaxid = iaxid[:axis] + (None,) + iaxid[axis:]
    return _finalize(normal_.stack(cls, arrays, axis), iaxid)


def solve(cls, x, y):
    if y._iaxid[0]:
        raise ValueError("Solutions along independence axes are not supported.")

    return _finalize(normal_.solve(cls, x, y), y._iaxid)


def asolve(cls, x, y):
    if y._iaxid[-1]:
        raise ValueError("Solutions along independence axes are not supported.")

    return _finalize(normal_.asolve(cls, x, y), y._iaxid)


def call_linearized(x, f, jmpf):
    return _finalize(normal_.call_linearized(x, f, jmpf), x._iaxid)


def fftfunc(cls, name, x, n, axis, norm):
    if x._iaxid[axis]:
        raise ValueError("Fourier transforms along independence axes "
                         f"({axis}) are not supported.")
    
    return _finalize(normal_.fftfunc(cls, name, x, n, axis, norm), x._iaxid)


def fftfunc_n(cls, name, x, s, axes, norm):
    if axes is None:
        ndim = x.ndim if s is None else len(s)
        axes = tuple(range(-ndim, 0))

    for axis in axes:
        if x._iaxid[axis]:
            raise ValueError("Fourier transforms along independence axes "
                             f"({axis}) are not supported.")
    
    return _finalize(normal_.fftfunc_n(cls, name, x, s, axes, norm), x._iaxid)


def _check_independence(x, op_axes, n):
    """Checks that the operation axes are not independence axes of ``x``.
    ``n`` is the operand number, normally 1 or 2, as this function is 
    a helper for bilinear functions."""
    
    if any([x._iaxid[ax] for ax in op_axes]):
        raise ValueError("Bilinear operations contracting over "
                         "independence axes are not supported. "
                         f"Axes {op_axes} of operand {n} are contracted.")
    

def bilinearfunc(cls, name, x, y, args=tuple(), pargs=tuple()):
    x, x_is_numeric = match_(cls, x)
    y, y_is_numeric = match_(cls, y)

    if not x_is_numeric and not y_is_numeric:
        raise ValueError(f"{name} operation between two sparse normal "
                         "variables is not supported.")
    
    return normal_.bilinearfunc(cls, name, x, y, args, pargs)


def _einsum_out_iaxid(x, insubs, outsubs):
    """Calculates the indices of the independence axes for
    the output operand."""
    
    for i, c in enumerate(insubs):
        if x._iaxid[i] and c not in outsubs:
            raise ValueError(f"Contraction over an independence axis ({i}).")
        
    iaxid = x._iaxid + (None,)  # Augments with a default.  
    return tuple([iaxid[insubs.find(c)] for c in outsubs])


def einsum_1(cls, subs, x, y):
    # Converts the subscripts to an explicit form.
    (insu1, insu2), outsu = einsubs.parse(subs, (x.shape, y.shape))
    subs = f"{insu1},{insu2}->{outsu}"

    iaxid = _einsum_out_iaxid(x, insu1, outsu)
    return _finalize(normal_.einsum_1(cls, subs, x, y), iaxid)


def einsum_2(cls, subs, x, y):
    # Converts the subscripts to an explicit form.
    (insu1, insu2), outsu = einsubs.parse(subs, (x.shape, y.shape))
    subs = f"{insu1},{insu2}->{outsu}"

    iaxid = _einsum_out_iaxid(y, insu2, outsu)
    return _finalize(normal_.einsum_2(cls, subs, x, y), iaxid)


def inner_1(cls, x, y):
    if x.ndim == 0 or y.ndim == 0:
        return x * y
    
    op_axes = (-1,)
    _check_independence(x, op_axes, 1)

    iaxid = x._iaxid[:-1] + (None,) * (y.ndim - 1)
    return _finalize(normal_.inner_1(cls, x, y), iaxid)
    

def inner_2(cls, x, y):
    if x.ndim == 0 or y.ndim == 0:
        return x * y
    
    op_axes = (-1,)
    _check_independence(y, op_axes, 2)

    iaxid = (None,) * (x.ndim - 1) + y._iaxid[:-1]
    return _finalize(normal_.inner_2(cls, x, y), iaxid)


def dot_1(cls, x, y):
    if x.ndim == 0 or y.ndim == 0:
        return x * y
    
    op_axes = (-1,)
    _check_independence(x, op_axes, 1)

    iaxid = x._iaxid[:-1] + (None,) * (y.ndim - 1)
    return _finalize(normal_.dot_1(cls, x, y), iaxid)


def dot_2(cls, x, y):
    if x.ndim == 0 or y.ndim == 0:
        return x * y
    
    op_axes = (0,) if y.ndim == 1 else (-2,)
    _check_independence(y, op_axes, 2)

    iaxid = list(y._iaxid)
    iaxid.pop(op_axes[0])
    iaxid = (None,) * (x.ndim - 1) + tuple(iaxid)
    return _finalize(normal_.dot_2(cls, x, y), iaxid)


def outer_1(cls, x, y):
    x, y = x.ravel(), y.ravel()
    return _finalize(normal_.outer_1(cls, x, y), x._iaxid + (None,))


def outer_2(cls, x, y):
    x, y = x.ravel(), y.ravel()
    return _finalize(normal_.outer_2(cls, x, y), (None,) + y._iaxid)


def kron_1(cls, x, y):
    ndim = max(x.ndim, y.ndim)  # ndim of the result.
    iaxid = (None,) * (ndim - x.ndim) + x._iaxid
    return _finalize(normal_.kron_1(cls, x, y), iaxid)


def kron_2(cls, x, y):
    ndim = max(x.ndim, y.ndim)  # ndim of the result.
    iaxid = (None,) * (ndim - y.ndim) + y._iaxid
    return _finalize(normal_.kron_2(cls, x, y), iaxid)


def tensordot_1(cls, x, y, axes):
    axes1, axes2 = complete_tensordot_axes(axes)
    axes1 = _normalize_axes(axes1, x.ndim)
    _check_independence(x, axes1, 1)

    iaxid = tuple([b for i, b in enumerate(x._iaxid) if i not in axes1])
    iaxid = iaxid + (None,) * (y.ndim - len(axes2))
    return _finalize(normal_.tensordot_1(cls, x, y, (axes1, axes2)), iaxid)


def tensordot_2(cls, x, y, axes):
    axes1, axes2 = complete_tensordot_axes(axes)
    axes2 = _normalize_axes(axes2, y.ndim)
    _check_independence(y, axes2, 2)

    iaxid = tuple([b for i, b in enumerate(y._iaxid) if i not in axes2])
    iaxid = (None,) * (x.ndim - len(axes1)) + iaxid
    return _finalize(normal_.tensordot_2(cls, x, y, (axes1, axes2)), iaxid)