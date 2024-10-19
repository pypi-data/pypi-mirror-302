from typing import Tuple, Optional, Union, List, Callable, Sequence, Dict

import numpy as np

from . import _ops as math, reshaped_numpy, reshaped_native, reshaped_tensor
from . import extrapolation as extrapolation
from ._magic_ops import stack, rename_dims, concat, variable_values, tree_map
from ._ops import choose_backend_t
from ._shape import Shape, channel, batch, spatial, DimFilter, parse_dim_order, shape, instance, dual, auto, non_batch
from ._tensors import Tensor, wrap, tensor
from .extrapolation import Extrapolation
from .magic import PhiTreeNode
from ..backend import choose_backend
from ..backend._dtype import DType


def vec(name: Union[str, Shape] = 'vector', *sequence, tuple_dim=spatial('sequence'), list_dim=instance('sequence'), **components) -> Tensor:
    """
    Lay out the given values along a channel dimension without converting them to the current backend.

    Args:
        name: Dimension name.
        *sequence: Component values that will also be used as item names.
            If specified, `components` must be empty.
        **components: Values by component name.
            If specified, no additional positional arguments must be given.
        tuple_dim: Dimension for `tuple` values passed as components, e.g. `vec(x=(0, 1), ...)`
        list_dim: Dimension for `list` values passed as components, e.g. `vec(x=[0, 1], ...)`

    Returns:
        `Tensor`

    Examples:
        >>> vec(x=1, y=0, z=-1)
        (x=1, y=0, z=-1)

        >>> vec(x=1., z=0)
        (x=1.000, z=0.000)

        >>> vec(x=tensor([1, 2, 3], instance('particles')), y=0)
        (x=1, y=0); (x=2, y=0); (x=3, y=0) (particlesⁱ=3, vectorᶜ=x,y)

        >>> vec(x=0, y=[0, 1])
        (x=0, y=0); (x=0, y=1) (vectorᶜ=x,y, sequenceⁱ=2)

        >>> vec(x=0, y=(0, 1))
        (x=0, y=0); (x=0, y=1) (sequenceˢ=2, vectorᶜ=x,y)
    """
    dim = auto(name, channel)
    assert isinstance(dim, Shape), f"name must be a str or Shape but got '{type(name)}'"
    if sequence:
        assert not components, "vec() must be given either positional or keyword arguments but not both"
        if len(sequence) == 1 and isinstance(sequence[0], (tuple, list)):
            sequence = sequence[0]
        dim = dim.with_size([str(v) for v in sequence])
        return wrap(sequence, dim)
    else:
        def wrap_sequence(value):
            if isinstance(value, tuple):
                return wrap(value, tuple_dim)
            elif isinstance(value, list):
                return wrap(value, list_dim)
            else:
                return value
        components = {n: wrap_sequence(v) for n, v in components.items()}
        if not components:
            return wrap([], dim)
        return stack(components, dim, expand_values=True)


def const_vec(value: Union[float, Tensor], dim: Union[Shape, tuple, list, str]):
    """
    Creates a single-dimension tensor with all values equal to `value`.
    `value` is not converted to the default backend, even when it is a Python primitive.

    Args:
        value: Value for filling the vector.
        dim: Either single-dimension non-spatial Shape or `Shape` consisting of any number of spatial dimensions.
            In the latter case, a new channel dimension named `'vector'` will be created from the spatial shape.

    Returns:
        `Tensor`
    """
    if isinstance(dim, Shape):
        if dim.spatial:
            assert not dim.non_spatial, f"When creating a vector given spatial dimensions, the shape may only contain spatial dimensions but got {dim}"
            shape = channel(vector=dim.names)
        else:
            assert dim.rank == 1, f"Cannot create vector from {dim}"
            shape = dim
    else:
        dims = parse_dim_order(dim)
        shape = channel(vector=dims)
    return wrap([value] * shape.size, shape)


def vec_length(vec: Tensor, vec_dim: DimFilter = channel, eps: Union[float, Tensor] = None):
    """
    Computes the vector length of `vec`.

    Args:
        eps: Minimum vector length. Use to avoid `inf` gradients for zero-length vectors.
    """
    if vec.dtype.kind == complex:
        vec = stack([vec.real, vec.imag], channel('_ReIm'))
    squared = vec_squared(vec, vec_dim)
    if eps is not None:
        squared = math.maximum(squared, eps)
    return math.sqrt(squared)


def vec_squared(vec: Tensor, vec_dim: DimFilter = channel):
    """ Computes the squared length of `vec`. If `vec_dim` is None, the combined channel dimensions of `vec` are interpreted as a vector. """
    return math.sum_(vec ** 2, dim=vec_dim)


def vec_normalize(vec: Tensor, vec_dim: DimFilter = channel, epsilon=None, allow_infinite=False):
    """
    Normalizes the vectors in `vec`. If `vec_dim` is None, the combined channel dimensions of `vec` are interpreted as a vector.

    Args:
        vec: `Tensor` to normalize.
        vec_dim: Dimensions to normalize over. By default, all channel dimensions are used to compute the vector length.
        epsilon: (Optional) Zero-length threshold. Vectors shorter than this length yield the unit vector (1, 0, 0, ...).
            If not specified, the zero-vector yields `NaN` as it cannot be normalized.
        allow_infinite: Allow infinite components in vectors. These vectors will then only points towards the infinite components.
    """
    if allow_infinite:  # replace inf by 1, finite by 0
        is_infinite = ~math.is_finite(vec)
        inf_mask = is_infinite & ~math.is_nan(vec)
        vec = math.where(math.any_(is_infinite, channel), inf_mask, vec)
    if epsilon is None:
        return vec / vec_length(vec, vec_dim=vec_dim)
    length = vec_length(vec, vec_dim=vec_dim, eps=epsilon**2 * .99)
    unit_vec = wrap([1] + [0] * (channel(vec).volume - 1), channel(vec))
    return math.where(abs(length) <= epsilon, unit_vec, vec / length)


def clip_length(vec: Tensor, min_len=0, max_len=1, vec_dim: DimFilter = channel, eps: Union[float, Tensor] = None):
    """
    Clips the length of a vector to the interval `[min_len, max_len]` while keeping the direction.
    Zero-vectors remain zero-vectors.

    Args:
        vec: `Tensor`
        min_len: Lower clipping threshold.
        max_len: Upper clipping threshold.
        vec_dim: Dimensions to compute the length over. By default, all channel dimensions are used to compute the vector length.
        eps: Minimum vector length. Use to avoid `inf` gradients for zero-length vectors.

    Returns:
        `Tensor` with same shape as `vec`.
    """
    length = vec_length(vec, vec_dim, eps)
    new_length = math.clip(length, min_len, max_len)
    return vec * math.safe_div(new_length, length)


def cross_product(vec1: Tensor, vec2: Tensor) -> Tensor:
    """
    Computes the cross product of two vectors in 2D.

    Args:
        vec1: `Tensor` with a single channel dimension called `'vector'`
        vec2: `Tensor` with a single channel dimension called `'vector'`

    Returns:
        `Tensor`
    """
    vec1 = math.tensor(vec1)
    vec2 = math.tensor(vec2)
    spatial_rank = vec1.vector.size if 'vector' in vec1.shape else vec2.vector.size
    if spatial_rank == 2:  # Curl in 2D
        assert vec2.vector.exists
        if vec1.vector.exists:
            v1_x, v1_y = vec1.vector
            v2_x, v2_y = vec2.vector
            return v1_x * v2_y - v1_y * v2_x
        else:
            v2_x, v2_y = vec2.vector
            return vec1 * math.stack_tensors([-v2_y, v2_x], channel(vec2))
    elif spatial_rank == 3:  # Curl in 3D
        assert vec1.vector.exists and vec2.vector.exists, f"Both vectors must have a 'vector' dimension but got shapes {vec1.shape}, {vec2.shape}"
        v1_x, v1_y, v1_z = vec1.vector
        v2_x, v2_y, v2_z = vec2.vector
        return math.stack([
            v1_y * v2_z - v1_z * v2_y,
            v1_z * v2_x - v1_x * v2_z,
            v1_x * v2_y - v1_y * v2_x,
        ], vec1.shape['vector'])
    else:
        raise AssertionError(f'dims = {spatial_rank}. Vector product not available in > 3 dimensions')


def rotate_vector(vector: math.Tensor, angle: Optional[Union[float, math.Tensor]], invert=False) -> Tensor:
    """
    Rotates `vector` around the origin.

    Args:
        vector: n-dimensional vector with exactly one channel dimension
        angle: Euler angle(s) or rotation matrix.
            `None` is interpreted as no rotation.
        invert: Whether to apply the inverse rotation.

    Returns:
        Rotated vector as `Tensor`
    """
    assert 'vector' in vector.shape, f"vector must have exactly a channel dimension named 'vector'"
    if angle is None:
        return vector
    matrix = rotation_matrix(angle, matrix_dim=channel(vector))
    if invert:
        matrix = rename_dims(matrix, '~vector,vector', math.concat_shapes(channel('vector'), dual('vector')))
    assert matrix.vector.dual.size == vector.vector.size, f"Rotation matrix from {angle.shape} is {matrix.vector.dual.size}D but vector {vector.shape} is {vector.vector.size}D."
    return matrix @ vector


def rotation_matrix(x: Union[float, math.Tensor], matrix_dim=channel('vector')):
    """
    Create a 2D or 3D rotation matrix from the corresponding angle(s).

    Args:
        x:
            2D: scalar angle
            3D: Either vector pointing along the rotation axis with rotation angle as length or Euler angles.
            Euler angles need to be laid out along a `angle` channel dimension with dimension names listing the spatial dimensions.
            E.g. a 90° rotation about the z-axis is represented by `vec('angles', x=0, y=0, z=PI/2)`.
            If a rotation matrix is passed for `angle`, it is returned without modification.
        matrix_dim: Matrix dimension for 2D rotations. In 3D, the channel dimension of angle is used.

    Returns:
        Matrix containing `matrix_dim` in primal and dual form as well as all non-channel dimensions of `x`.
    """
    if isinstance(x, Tensor) and '~vector' in x.shape and 'vector' in x.shape.channel and x.shape.get_size('~vector') == x.shape.get_size('vector'):
        return x  # already a rotation matrix
    elif 'angle' in shape(x) and shape(x).get_size('angle') == 3:  # 3D Euler angles
        assert channel(x).rank == 1 and channel(x).size == 3, f"x for 3D rotations needs to be a 3-vector but got {x}"
        s1, s2, s3 = math.sin(x).angle  # x, y, z
        c1, c2, c3 = math.cos(x).angle
        matrix_dim = matrix_dim.with_size(shape(x).get_item_names('angle'))
        return wrap([[c3 * c2, c3 * s2 * s1 - s3 * c1, c3 * s2 * c1 + s3 * s1],
                     [s3 * c2, s3 * s2 * s1 + c3 * c1, s3 * s2 * c1 - c3 * s1],
                     [-s2, c2 * s1, c2 * c1]], matrix_dim, matrix_dim.as_dual())  # Rz * Ry * Rx  (1. rotate about X by first angle)
    elif 'vector' in shape(x) and shape(x).get_size('vector') == 3:  # 3D axis + x
        angle = vec_length(x)
        s, c = math.sin(angle), math.cos(angle)
        t = 1 - c
        k1, k2, k3 = vec_normalize(x, epsilon=1e-12).vector
        matrix_dim = matrix_dim.with_size(shape(x).get_item_names('vector'))
        return wrap([[c + k1**2 * t, k1 * k2 * t - k3 * s, k1 * k3 * t + k2 * s],
                     [k2 * k1 * t + k3 * s, c + k2**2 * t, k2 * k3 * t - k1 * s],
                     [k3 * k1 * t - k2 * s, k3 * k2 * t + k1 * s, c + k3**2 * t]], matrix_dim, matrix_dim.as_dual())
    else:  # 2D rotation
        sin = wrap(math.sin(x))
        cos = wrap(math.cos(x))
        return wrap([[cos, -sin], [sin, cos]], matrix_dim, matrix_dim.as_dual())


def rotation_angles(rot: Tensor):
    """
    Compute the scalar x in 2D or the Euler angles in 3D from a given rotation matrix.
    This function returns one valid solution but often, there are multiple solutions.

    Args:
        rot: Rotation matrix as created by `phi.math.rotation_matrix()`.
            Must have exactly one channel and one dual dimension with equally-ordered elements.

    Returns:
        Scalar x in 2D, Euler angles
    """
    assert channel(rot).rank == 1 and dual(rot).rank == 1, f"Rotation matrix must have one channel and one dual dimension but got {rot.shape}"
    if channel(rot).size == 2:
        cos = rot[{channel: 0, dual: 0}]
        sin = rot[{channel: 1, dual: 0}]
        return math.arctan(sin, divide_by=cos)
    elif channel(rot).size == 3:
        a2 = -math.arcsin(rot[{channel: 2, dual: 0}])  # ToDo handle [2, 0] == 1 (i.e. cos_theta == 0)
        cos2 = math.cos(a2)
        a1 = math.arctan(rot[{channel: 2, dual: 1}] / cos2, divide_by=rot[{channel: 2, dual: 2}] / cos2)
        a3 = math.arctan(rot[{channel: 1, dual: 0}] / cos2, divide_by=rot[{channel: 0, dual: 0}] / cos2)
        regular_sol = stack([a1, a2, a3], channel(angle=channel(rot).item_names[0]))
        # --- pole case cos(theta) == 1 ---
        a3_pole = 0  # unconstrained
        bottom_pole = rot[{channel: 2, dual: 0}] < 0
        a2_pole = math.where(bottom_pole, 1.57079632679, -1.57079632679)
        a1_pole = math.where(bottom_pole, math.arctan(rot[{channel: 0, dual: 1}], divide_by=rot[{channel: 0, dual: 2}]), math.arctan(-rot[{channel: 0, dual: 1}], divide_by=-rot[{channel: 0, dual: 2}]))
        pole_sol = stack([a1_pole, a2_pole, a3_pole], channel(regular_sol))
        return math.where(abs(rot[{channel: 2, dual: 0}]) >= 1, pole_sol, regular_sol)
    else:
        raise ValueError(f"")


def dim_mask(all_dims: Union[Shape, tuple, list], dims: DimFilter, mask_dim=channel('vector')) -> Tensor:
    """
    Creates a masked vector with 1 elements for `dims` and 0 for all other dimensions in `all_dims`.

    Args:
        all_dims: All dimensions for which the vector should have an entry.
        dims: Dimensions marked as 1.
        mask_dim: Dimension of the masked vector. Item names are assigned automatically.

    Returns:
        `Tensor`
    """
    assert isinstance(all_dims, (Shape, tuple, list)), f"all_dims must be a tuple or Shape but got {type(all_dims)}"
    assert isinstance(mask_dim, Shape) and mask_dim.rank == 1, f"mask_dim must be a single-dimension Shape but got {mask_dim}"
    if isinstance(all_dims, (tuple, list)):
        all_dims = spatial(*all_dims)
    dims = all_dims.only(dims)
    mask = [1 if dim in dims else 0 for dim in all_dims]
    mask_dim = mask_dim.with_size(all_dims.names)
    return wrap(mask, mask_dim)


def normalize_to(target: Tensor, source: Union[float, Tensor], epsilon=1e-5):
    """
    Multiplies the target so that its sum matches the source.

    Args:
        target: `Tensor`
        source: `Tensor` or constant
        epsilon: Small number to prevent division by zero.

    Returns:
        Normalized tensor of the same shape as target
    """
    target_total = math.sum_(target)
    denominator = math.maximum(target_total, epsilon) if epsilon is not None else target_total
    source_total = math.sum_(source)
    return target * (source_total / denominator)


def l1_loss(x, reduce: DimFilter = math.non_batch) -> Tensor:
    """
    Computes *∑<sub>i</sub> ||x<sub>i</sub>||<sub>1</sub>*, summing over all non-batch dimensions.

    Args:
        x: `Tensor` or `phiml.math.magic.PhiTreeNode` or 0D or 1D native tensor.
            For `phiml.math.magic.PhiTreeNode` objects, only value the sum over all value attributes is computed.
        reduce: Dimensions to reduce as `DimFilter`.

    Returns:
        loss: `Tensor`
    """
    if isinstance(x, Tensor):
        return math.sum_(abs(x), reduce)
    elif isinstance(x, PhiTreeNode):
        return sum([l1_loss(getattr(x, a), reduce) for a in variable_values(x)])
    else:
        try:
            backend = math.choose_backend(x)
            shape = backend.staticshape(x)
            if len(shape) == 0:
                return abs(x)
            elif len(shape) == 1:
                return backend.sum(abs(x))
            else:
                raise ValueError("l2_loss is only defined for 0D and 1D native tensors. For higher-dimensional data, use Φ-ML tensors.")
        except math.NoBackendFound:
            raise ValueError(x)


def l2_loss(x, reduce: DimFilter = math.non_batch) -> Tensor:
    """
    Computes *∑<sub>i</sub> ||x<sub>i</sub>||<sub>2</sub><sup>2</sup> / 2*, summing over all non-batch dimensions.

    Args:
        x: `Tensor` or `phiml.math.magic.PhiTreeNode` or 0D or 1D native tensor.
            For `phiml.math.magic.PhiTreeNode` objects, only value the sum over all value attributes is computed.
        reduce: Dimensions to reduce as `DimFilter`.

    Returns:
        loss: `Tensor`
    """
    if isinstance(x, Tensor):
        if x.dtype.kind == complex:
            x = abs(x)
        return math.sum_(x ** 2, reduce) * 0.5
    elif isinstance(x, PhiTreeNode):
        return sum([l2_loss(getattr(x, a), reduce) for a in variable_values(x)])
    else:
        try:
            backend = math.choose_backend(x)
            shape = backend.staticshape(x)
            if len(shape) == 0:
                return x ** 2 * 0.5
            elif len(shape) == 1:
                return backend.sum(x ** 2) * 0.5
            else:
                raise ValueError("l2_loss is only defined for 0D and 1D native tensors. For higher-dimensional data, use Φ-ML tensors.")
        except math.NoBackendFound:
            raise ValueError(x)


def frequency_loss(x,
                   frequency_falloff: float = 100,
                   threshold=1e-5,
                   ignore_mean=False,
                   n=2) -> Tensor:
    """
    Penalizes the squared `values` in frequency (Fourier) space.
    Lower frequencies are weighted more strongly then higher frequencies, depending on `frequency_falloff`.

    Args:
        x: `Tensor` or `phiml.math.magic.PhiTreeNode` Values to penalize, typically `actual - target`.
        frequency_falloff: Large values put more emphasis on lower frequencies, 1.0 weights all frequencies equally.
            *Note*: The total loss is not normalized. Varying the value will result in losses of different magnitudes.
        threshold: Frequency amplitudes below this value are ignored.
            Setting this to zero may cause infinities or NaN values during backpropagation.
        ignore_mean: If `True`, does not penalize the mean value (frequency=0 component).

    Returns:
      Scalar loss value
    """
    assert n in (1, 2)
    if isinstance(x, Tensor):
        if ignore_mean:
            x -= math.mean(x, x.shape.non_batch)
        k_squared = vec_squared(math.fftfreq(x.shape.spatial))
        weights = math.exp(-0.5 * k_squared * frequency_falloff ** 2)

        diff_fft = abs_square(math.fft(x) * weights)
        diff_fft = math.sqrt(math.maximum(diff_fft, threshold))
        return l2_loss(diff_fft) if n == 2 else l1_loss(diff_fft)
    elif isinstance(x, PhiTreeNode):
        losses = [frequency_loss(getattr(x, a), frequency_falloff, threshold, ignore_mean, n) for a in variable_values(x)]
        return sum(losses)
    else:
        raise ValueError(x)


def abs_square(complex_values: Union[Tensor, complex]) -> Tensor:
    """
    Squared magnitude of complex values.

    Args:
      complex_values: complex `Tensor`

    Returns:
        Tensor: real valued magnitude squared

    """
    return math.imag(complex_values) ** 2 + math.real(complex_values) ** 2


# Divergence

# def divergence(tensor, dx=1, difference='central', padding='constant', dimensions=None):
#     """
#     Computes the spatial divergence of a vector channel from finite differences.
#
#     :param tensor: vector field; tensor of shape (batch size, spatial dimensions..., spatial rank)
#     :param dx: distance between adjacent grid points (default 1)
#     :param difference: type of difference, one of ('forward', 'central') (default 'forward')
#     :return: tensor of shape (batch size, spatial dimensions..., 1)
#     """
#     assert difference in ('central', 'forward', 'backward'), difference
#     rank = spatial_rank(tensor)
#     if difference == 'forward':
#         return _divergence_nd(tensor, padding, (0, 1), dims) / dx ** rank  # TODO why dx^rank?
#     elif difference == 'backward':
#         return _divergence_nd(tensor, padding, (-1, 0), dims) / dx ** rank
#     else:
#         return _divergence_nd(tensor, padding, (-1, 1), dims) / (2 * dx) ** rank
#
#
# def _divergence_nd(x_, padding, relative_shifts, dims=None):
#     x = tensor(x_)
#     assert x.shape.channel.rank == 1
#     dims = dims if dims is not None else x.shape.spatial.names
#     x = math.pad(x, {axis: (-relative_shifts[0], relative_shifts[1]) for axis in dims}, mode=padding)
#     components = []
#     for dimension in dims:
#         dim_index_in_spatial = x.shape.spatial.reset_indices().index(dimension)
#         lower, upper = _multi_roll(x, dimension, relative_shifts, diminish_others=(-relative_shifts[0], relative_shifts[1]), names=dims, base_selection={0: rank - dimension - 1})
#         components.append(upper - lower)
#     return math.sum_(components, 0)


def shift(x: Tensor,
          offsets: Sequence[int],
          dims: DimFilter = math.spatial,
          padding: Union[Extrapolation, float, Tensor, str, None] = extrapolation.BOUNDARY,
          stack_dim: Union[Shape, str, None] = channel('shift'),
          extend_bounds=0,
          padding_kwargs: dict = None) -> List[Tensor]:
    """
    Shift the tensor `x` by a fixed offset, using `padding` for edge values.

    This is similar to `numpy.roll()` but with major differences:

    * Values shifted in from the boundary are defined by `padding`.
    * Positive offsets represent negative shifts.
    * Support for multi-dimensional shifts

    See Also:
        `index_shift`, `neighbor_reduce`.

    Args:
        x: Input grid-like `Tensor`.
        offsets: `tuple` listing shifts to compute, each must be an `int`. One `Tensor` will be returned for each entry.
        dims: Dimensions along which to shift, defaults to all *spatial* dims of `x`.
        padding: Padding to be performed at the boundary so that the shifted versions have the same size as `x`.
            Must be one of the following: `Extrapolation`, `Tensor` or number for constant extrapolation, name of extrapolation as `str`.
            Can be set to `None` to disable padding. Then the result tensors will be smaller than `x`.
        stack_dim: Dimension along which the components corresponding to each dim in `dims` should be stacked.
            This can be set to `None` only if `dims` is a single dimension.
        extend_bounds: Number of cells by which to pad the tensors in addition to the number required to maintain the size of `x`.
            Can only be used with a valid `padding`.
        padding_kwargs: Additional keyword arguments to be passed to `phiml.math.pad()`.

    Returns:
        `list` of shifted tensors. The number of return tensors is equal to the number of `offsets`.
    """
    if dims is None:
        raise ValueError("dims=None is not supported anymore.")
    dims = x.shape.only(dims, reorder=True).names
    if stack_dim is None:
        assert len(dims) == 1
    x = wrap(x)
    pad_lower = max(0, -min(offsets))
    pad_upper = max(0, max(offsets))
    if padding is not None:
        x = math.pad(x, {axis: (pad_lower + extend_bounds, pad_upper + extend_bounds) for axis in dims}, mode=padding, **(padding_kwargs or {}))
    if extend_bounds:
        assert padding is not None
    offset_tensors = []
    for offset in offsets:
        components = {}
        for dimension in dims:
            if padding is not None:
                slices = {dim: slice(pad_lower + offset, (-pad_upper + offset) or None) if dim == dimension else slice(pad_lower, -pad_upper or None) for dim in dims}
            else:
                slices = {dim: slice(pad_lower + offset, (-pad_upper + offset) or None) if dim == dimension else slice(None, None) for dim in dims}
            components[dimension] = x[slices]
        offset_tensors.append(stack(components, stack_dim) if stack_dim is not None else next(iter(components.values())))
    return offset_tensors


def index_shift(x: Tensor, offsets: Sequence[Union[int, Tensor]], padding: Union[Extrapolation, float, Tensor, str, None] = None) -> List[Tensor]:
    """
    Returns shifted versions of `x` according to `offsets` where each offset is an `int` vector indexing some dimensions of `x`.

    See Also:
        `shift`, `neighbor_reduce`.

    Args:
        x: Input grid-like `Tensor`.
        offsets: Sequence of offset vectors. Each offset is an `int` vector indexing some dimensions of `x`.
            Offsets can have different subsets of the dimensions of `x`. Missing dimensions count as 0.
            The value `0` can also be passed as a zero-shift.
        padding: Padding to be performed at the boundary so that the shifted versions have the same size as `x`.
            Must be one of the following: `Extrapolation`, `Tensor` or number for constant extrapolation, name of extrapolation as `str`.
            Can be set to `None` to disable padding. Then the result tensors will be smaller than `x`.

    Returns:
        `list` of shifted tensors. The number of return tensors is equal to the number of `offsets`.
    """
    _, widths_list, min_by_dim, max_by_dim = join_index_offsets(offsets, negate=True)
    if padding is not None:
        pad_lower = {d: max(0, -m) for d, m in min_by_dim.items()}
        pad_upper = {d: max(0, m) for d, m in max_by_dim.items()}
        widths = {d: (pad_lower[d], pad_upper[d]) for d in pad_lower.keys()}
        x = math.pad(x, widths, mode=padding)
    return [math.pad(x, w, extrapolation.NONE) for w in widths_list]


def join_index_offsets(offsets: Sequence[Union[int, Tensor]], negate=False):
    assert offsets, f"At least one offset mut be provided."
    assert all((isinstance(o, int) and o == 0) or (channel(o) and channel(o).item_names[0]) for o in offsets)
    dims = tuple(set().union(*[channel(o).item_names[0] for o in offsets if channel(o)]))
    offsets = [vec(**{d: o[d] if not isinstance(o, int) and d in channel(o).item_names[0] else 0 for d in dims}) for o in offsets]
    min_by_dim = {d: min([int(o[d]) for o in offsets]) for d in dims}
    max_by_dim = {d: max([int(o[d]) for o in offsets]) for d in dims}
    neg = -1 if negate else 1
    result = [{d: (int(o[d] - min_by_dim[d]) * neg, int(max_by_dim[d] - o[d]) * neg) for d in dims} for o in offsets]
    return offsets, result, min_by_dim, max_by_dim


def index_shift_widths(offsets: Sequence[Union[int, Tensor]]) -> List[Dict[str, Tuple[int, int]]]:
    _, widths_list, _, _ = join_index_offsets(offsets, negate=False)
    return widths_list


def neighbor_reduce(reduce_fun: Callable, grid: Tensor, dims: DimFilter = spatial, padding: Union[Extrapolation, float, Tensor, str, None] = None, padding_kwargs: dict = None) -> Tensor:
    """
    Computes the sum/mean/min/max/prod/etc. of two neighboring values along each dimension in `dim`.
    The result tensor has one entry less than `grid` in each averaged dimension unless `padding` is specified.

    With two `dims`, computes the mean of 4 values, in 3D, the mean of 8 values.

    Args:
        reduce_fun: Reduction function, such as `sum`, `mean`, `max`, `min`, `prod`.
        grid: Values to reduce.
        dims: Dimensions along which neighbors should be reduced.
        padding: Padding at the upper edges of `grid` along `dims'. If not `None`, the result tensor will have the same shape as `grid`.
        padding_kwargs: Additional keyword arguments to be passed to `phiml.math.pad()`.

    Returns:
        `Tensor`
    """
    result = grid
    dims = grid.shape.only(dims)
    for dim in dims:
        l, r = shift(result, (0, 1), dim, padding, None, padding_kwargs=padding_kwargs)
        lr = stack([l, r], batch('_reduce'))
        result = reduce_fun(lr, '_reduce')
    return result


def neighbor_mean(grid: Tensor, dims: DimFilter = spatial, padding: Union[Extrapolation, float, Tensor, str, None] = None) -> Tensor:
    """`neighbor_reduce` with `reduce_fun` set to `phiml.math.mean`."""
    return neighbor_reduce(math.mean, grid, dims, padding)


def neighbor_sum(grid: Tensor, dims: DimFilter = spatial, padding: Union[Extrapolation, float, Tensor, str, None] = None) -> Tensor:
    """`neighbor_reduce` with `reduce_fun` set to `phiml.math.sum`."""
    return neighbor_reduce(math.sum_, grid, dims, padding)


def neighbor_max(grid: Tensor, dims: DimFilter = spatial, padding: Union[Extrapolation, float, Tensor, str, None] = None) -> Tensor:
    """`neighbor_reduce` with `reduce_fun` set to `phiml.math.max`."""
    return neighbor_reduce(math.max_, grid, dims, padding)


def neighbor_min(grid: Tensor, dims: DimFilter = spatial, padding: Union[Extrapolation, float, Tensor, str, None] = None) -> Tensor:
    """`neighbor_reduce` with `reduce_fun` set to `phiml.math.min`."""
    return neighbor_reduce(math.min_, grid, dims, padding)


def at_neighbor_where(reduce_fun: Callable, values, key_grid: Tensor, dims: DimFilter = spatial, padding: Union[Extrapolation, float, Tensor, str, None] = None, offsets=(0, 1), diagonal=True, padding_kwargs: dict = None) -> Tensor:
    """
    Computes the mean of two neighboring values along each dimension in `dim`.
    The result tensor has one entry less than `grid` in each averaged dimension unless `padding` is specified.

    With two `dims`, computes the mean of 4 values, in 3D, the mean of 8 values.

    Args:
        reduce_fun: Reduction function, such as `at_max`, `at_min`.
        values: Values to look up and return.
        key_grid: Values to compare.
        dims: Dimensions along which neighbors should be averaged.
        padding: Padding at the upper edges of `grid` along `dims'. If not `None`, the result tensor will have the same shape as `grid`.
        offsets: Relative neighbor indices as `int`. `0` refers to self, negative values to earlier (left) neighbors and positive values to later (right) neighbors.
        diagonal: If `True`, performs sequential reductions along each axis, determining the minimum value along each axis independently.
            If the values of `key_grid` depend on `values`, this can lead to undesired behavior.
        padding_kwargs: Additional keyword arguments to be passed to `phiml.math.pad()`.

    Returns:
        `Tensor`
    """
    result = key_grid
    dims = key_grid.shape.only(dims)
    if diagonal:
        for dim in dims:
            lr = stack(shift(result, offsets, dim, padding, None, padding_kwargs=padding_kwargs), batch('_reduce'))
            values = tree_map(lambda t: stack(shift(t, offsets, dim, padding, None, padding_kwargs=padding_kwargs), batch('_reduce')), values)
            result, values = reduce_fun([lr, values], lr, '_reduce')
    else:
        lr = concat(shift(result, offsets, dims, padding, channel('_reduce'), padding_kwargs=padding_kwargs), '_reduce')
        values = tree_map(lambda t: concat(shift(t, offsets, dims, padding, channel('_reduce'), padding_kwargs=padding_kwargs), '_reduce'), values)
        result, values = reduce_fun([lr, values], lr, '_reduce')
    return values


def at_max_neighbor(values, key_grid: Tensor, dims: DimFilter = spatial, padding: Union[Extrapolation, float, Tensor, str, None] = None, offsets=(0, 1), diagonal=True) -> Tensor:
    """
    Computes the min of neighboring values in `key_grid` along each dimension in `dims` and retrieves the corresponding values from `values`.

    Args:
        values: Values to look up and return. `Tensor` or tree structure.
        key_grid: Values to compare.
        dims: Dimensions along which neighbors should be averaged.
        padding: Padding at the upper edges of `grid` along `dims'. If not `None`, the result tensor will have the same shape as `grid`.
        offsets: Relative neighbor indices as `int`. `0` refers to self, negative values to earlier (left) neighbors and positive values to later (right) neighbors.
        diagonal: If `True`, performs sequential reductions along each axis, determining the minimum value along each axis independently.
            If the values of `key_grid` depend on `values` or their position in the grid, this can lead to undesired behavior.

    Returns:
        Tree or `Tensor` like values.
    """
    return at_neighbor_where(math.at_max, values, key_grid, dims, padding=padding, offsets=offsets, diagonal=diagonal)


def at_min_neighbor(values, key_grid: Tensor, dims: DimFilter = spatial, padding: Union[Extrapolation, float, Tensor, str, None] = None, offsets=(0, 1), diagonal=True) -> Tensor:
    """
    Computes the max of neighboring values in `key_grid` along each dimension in `dims` and retrieves the corresponding values from `values`.

    Args:
        values: Values to look up and return.
        key_grid: Values to compare.
        dims: Dimensions along which neighbors should be averaged.
        padding: Padding at the upper edges of `grid` along `dims'. If not `None`, the result tensor will have the same shape as `grid`.
        offsets: Relative neighbor indices as `int`. `0` refers to self, negative values to earlier (left) neighbors and positive values to later (right) neighbors.
        diagonal: If `True`, performs sequential reductions along each axis, determining the minimum value along each axis independently.
            If the values of `key_grid` depend on `values` or their position in the grid, this can lead to undesired behavior.

    Returns:
        Tree or `Tensor` like values.
    """
    return at_neighbor_where(math.at_min, values, key_grid, dims, padding=padding, offsets=offsets, diagonal=diagonal)



def masked_fill(values: Tensor, valid: Tensor, distance: int = 1) -> Tuple[Tensor, Tensor]:
    """
    Extrapolates the values of `values` which are marked by the nonzero values of `valid` for `distance` steps in all spatial directions.
    Overlapping extrapolated values get averaged. Extrapolation also includes diagonals.

    Args:
        values: Tensor which holds the values for extrapolation
        valid: Tensor with same size as `x` marking the values for extrapolation with nonzero values
        distance: Number of extrapolation steps

    Returns:
        values: Extrapolation result
        valid: mask marking all valid values after extrapolation
    """
    def binarize(x):
        return math.safe_div(x, x)
    distance = min(distance, max(values.shape.sizes))
    for _ in range(distance):
        valid = binarize(valid)
        valid_values = valid * values
        overlap = valid  # count how many values we are adding
        for dim in values.shape.spatial.names:
            values_l, values_r = shift(valid_values, (-1, 1), dims=dim, padding=extrapolation.ZERO)
            valid_values = math.sum_(values_l + values_r + valid_values, dim='shift')
            mask_l, mask_r = shift(overlap, (-1, 1), dims=dim, padding=extrapolation.ZERO)
            overlap = math.sum_(mask_l + mask_r + overlap, dim='shift')
        extp = math.safe_div(valid_values, overlap)  # take mean where extrapolated values overlap
        values = math.where(valid, values, math.where(binarize(overlap), extp, values))
        valid = overlap
    return values, binarize(valid)


def finite_fill(values: Tensor, dims: DimFilter = spatial, distance: int = 1, diagonal: bool = True, padding=extrapolation.BOUNDARY, padding_kwargs: dict = None) -> Tensor:
    """
    Fills non-finite (NaN, inf, -inf) values from nearby finite values.
    Extrapolates the finite values of `values` for `distance` steps along `dims`.
    Where multiple finite values could fill an invalid value, the average is computed.

    Args:
        values: Floating-point `Tensor`. All non-numeric values (`NaN`, `inf`, `-inf`) are interpreted as invalid.
        dims: Dimensions along which to fill invalid values from finite ones.
        distance: Number of extrapolation steps, each extrapolating one cell out.
        diagonal: Whether to extrapolate values to their diagonal neighbors per step.
        padding: Extrapolation of `values`. Determines whether to extrapolate from the edges as well.
        padding_kwargs: Additional keyword arguments to be passed to `phiml.math.pad()`.

    Returns:
        `Tensor` of same shape as `values`.
    """
    if diagonal:
        distance = min(distance, max(values.shape.sizes))
        dims = values.shape.only(dims)
        for _ in range(distance):
            valid = math.is_finite(values)
            valid_values = math.where(valid, values, 0)
            overlap = valid
            for dim in dims:
                values_l, values_r = shift(valid_values, (-1, 1), dims=dim, padding=padding, padding_kwargs=padding_kwargs)
                valid_values = math.sum_(values_l + values_r + valid_values, dim='shift')
                mask_l, mask_r = shift(overlap, (-1, 1), dims=dim, padding=padding, padding_kwargs=padding_kwargs)
                overlap = math.sum_(mask_l + mask_r + overlap, dim='shift')
            values = math.where(valid, values, valid_values / overlap)
    else:
        distance = min(distance, sum(values.shape.sizes))
        for _ in range(distance):
            neighbors = concat(shift(values, (-1, 1), dims, padding=padding, stack_dim=channel('neighbors'), padding_kwargs=padding_kwargs), 'neighbors')
            finite = math.is_finite(neighbors)
            avg_neighbors = math.sum_(math.where(finite, neighbors, 0), 'neighbors') / math.sum_(finite, 'neighbors')
            values = math.where(math.is_finite(values), values, avg_neighbors)
    return values


# Gradient

def spatial_gradient(grid: Tensor,
                     dx: Union[float, Tensor] = 1,
                     difference: str = 'central',
                     padding: Union[Extrapolation, float, Tensor, str, None] = extrapolation.BOUNDARY,
                     dims: DimFilter = spatial,
                     stack_dim: Union[Shape, str, None] = channel('gradient'),
                     pad=0,
                     padding_kwargs: dict = None) -> Tensor:
    """
    Calculates the spatial_gradient of a scalar channel from finite differences.
    The spatial_gradient vectors are in reverse order, lowest dimension first.

    Args:
        grid: grid values
        dims: (Optional) Dimensions along which the spatial derivative will be computed. sequence of dimension names
        dx: Physical distance between grid points, `float` or `Tensor`.
            When passing a vector-valued `Tensor`, the dx values should be listed along `stack_dim`, matching `dims`.
        difference: type of difference, one of ('forward', 'backward', 'central') (default 'forward')
        padding: Padding mode.
            Must be one of the following: `Extrapolation`, `Tensor` or number for constant extrapolation, name of extrapolation as `str`.
        stack_dim: name of the new vector dimension listing the spatial_gradient w.r.t. the various axes
        pad: How many cells to extend the result compared to `grid`.
            This value is added to the internal padding. For non-trivial extrapolations, this gives the correct result while manual padding before or after this operation would not respect the boundary locations.
        padding_kwargs: Additional keyword arguments to be passed to `phiml.math.pad()`.

    Returns:
        `Tensor`
    """
    grid = wrap(grid)
    if stack_dim and stack_dim in grid.shape:
        assert grid.shape.only(stack_dim).size == 1, f"spatial_gradient() cannot list components along {stack_dim.name} because that dimension already exists on grid {grid}"
        grid = grid[{stack_dim.name: 0}]
    dims = grid.shape.only(dims)
    dx = wrap(dx)
    if dx.vector.exists:
        dx = dx.vector[dims]
        if dx.vector.size in (None, 1):
            dx = dx.vector[0]
    if difference.lower() == 'central':
        left, right = shift(grid, (-1, 1), dims, padding, stack_dim=stack_dim, extend_bounds=pad, padding_kwargs=padding_kwargs)
        return (right - left) / (dx * 2)
    elif difference.lower() == 'forward':
        left, right = shift(grid, (0, 1), dims, padding, stack_dim=stack_dim, extend_bounds=pad, padding_kwargs=padding_kwargs)
        return (right - left) / dx
    elif difference.lower() == 'backward':
        left, right = shift(grid, (-1, 0), dims, padding, stack_dim=stack_dim, extend_bounds=pad, padding_kwargs=padding_kwargs)
        return (right - left) / dx
    else:
        raise ValueError('Invalid difference type: {}. Can be CENTRAL or FORWARD'.format(difference))


# Laplace

def laplace(x: Tensor,
            dx: Union[Tensor, float] = 1,
            padding: Union[Extrapolation, float, Tensor, str, None] = extrapolation.BOUNDARY,
            dims: DimFilter = spatial,
            weights: Tensor = None,
            padding_kwargs: dict = None):
    """
    Spatial Laplace operator as defined for scalar fields.
    If a vector field is passed, the laplace is computed component-wise.

    Args:
        x: n-dimensional field of shape (batch, spacial dimensions..., components)
        dx: scalar or 1d tensor
        padding: Padding mode.
            Must be one of the following: `Extrapolation`, `Tensor` or number for constant extrapolation, name of extrapolation as `str`.
        dims: The second derivative along these dimensions is summed over
        weights: (Optional) Multiply the axis terms by these factors before summation.
            Must be a Tensor with a single channel dimension that lists all laplace dims by name.
        padding_kwargs: Additional keyword arguments to be passed to `phiml.math.pad()`.

    Returns:
        `phiml.math.Tensor` of same shape as `x`
    """
    if isinstance(dx, (tuple, list)):
        dx = wrap(dx, batch('_laplace'))
    elif isinstance(dx, Tensor) and dx.vector.exists:
        dx = rename_dims(dx, 'vector', batch('_laplace'))
    if isinstance(x, Extrapolation):
        return x.spatial_gradient()
    left, center, right = shift(wrap(x), (-1, 0, 1), dims, padding, stack_dim=batch('_laplace'), padding_kwargs=padding_kwargs)
    result = (left + right - 2 * center) / (dx ** 2)
    if weights is not None:
        dim_names = x.shape.only(dims).names
        if channel(weights):
            assert set(channel(weights).item_names[0]) >= set(dim_names), f"the channel dim of weights must contain all laplace dims {dim_names} but only has {channel(weights).item_names}"
            weights = rename_dims(weights, channel, batch('_laplace'))
        result *= weights
    result = math.sum_(result, '_laplace')
    return result


def fourier_laplace(grid: Tensor,
                    dx: Union[Tensor, Shape, float, list, tuple],
                    times: int = 1):
    """
    Applies the spatial laplace operator to the given tensor with periodic boundary conditions.
    
    *Note:* The results of `fourier_laplace` and `laplace` are close but not identical.
    
    This implementation computes the laplace operator in Fourier space.
    The result for periodic fields is exact, i.e. no numerical instabilities can occur, even for higher-order derivatives.

    Args:
      grid: tensor, assumed to have periodic boundary conditions
      dx: distance between grid points, tensor-like, scalar or vector
      times: number of times the laplace operator is applied. The computational cost is independent of this parameter.
      grid: Tensor: 
      dx: Tensor or Shape or float or list or tuple: 
      times: int:  (Default value = 1)

    Returns:
      tensor of same shape as `tensor`

    """
    frequencies = math.fft(math.to_complex(grid))
    k_squared = math.sum_(math.fftfreq(grid.shape) ** 2, 'vector')
    fft_laplace = -(2 * np.pi) ** 2 * k_squared
    result = math.real(math.ifft(frequencies * fft_laplace ** times))
    return math.cast(result / wrap(dx) ** 2, grid.dtype)


def fourier_poisson(grid: Tensor,
                    dx: Union[Tensor, Shape, float, list, tuple],
                    times: int = 1):
    """
    Inverse operation to `fourier_laplace`.

    Args:
      grid: Tensor: 
      dx: Tensor or Shape or float or list or tuple: 
      times: int:  (Default value = 1)

    Returns:

    """
    frequencies = math.fft(math.to_complex(grid))
    k_squared = math.sum_(math.fftfreq(grid.shape) ** 2, 'vector')
    fft_laplace = -(2 * np.pi) ** 2 * k_squared
    # fft_laplace.tensor[(0,) * math.ndims(k_squared)] = math.inf  # assume NumPy array to edit
    result = math.real(math.ifft(math.safe_div(frequencies, math.to_complex(fft_laplace ** times))))
    return math.cast(result * wrap(dx) ** 2, grid.dtype)


# Downsample / Upsample

def downsample2x(grid: Tensor,
                 padding: Extrapolation = extrapolation.BOUNDARY,
                 dims: DimFilter = spatial) -> Tensor:
    """
    Resamples a regular grid to half the number of spatial sample points per dimension.
    The grid values at the new points are determined via mean (linear interpolation).

    Args:
      grid: full size grid
      padding: grid extrapolation. Used to insert an additional value for odd spatial dims
      dims: dims along which down-sampling is applied. If None, down-sample along all spatial dims.
      grid: Tensor: 
      padding: Extrapolation:  (Default value = extrapolation.BOUNDARY)
      dims: tuple or None:  (Default value = None)

    Returns:
      half-size grid

    """
    dims = grid.shape.only(dims).names
    odd_dimensions = [dim for dim in dims if grid.shape.get_size(dim) % 2 != 0]
    grid = math.pad(grid, {dim: (0, 1) for dim in odd_dimensions}, padding)
    for dim in dims:
        grid = (grid[{dim: slice(1, None, 2)}] + grid[{dim: slice(0, None, 2)}]) / 2
    return grid


def upsample2x(grid: Tensor,
               padding: Extrapolation = extrapolation.BOUNDARY,
               dims: DimFilter = spatial,
               padding_kwargs: dict = None) -> Tensor:
    """
    Resamples a regular grid to double the number of spatial sample points per dimension.
    The grid values at the new points are determined via linear interpolation.

    Args:
        grid: half-size grid
        padding: grid extrapolation
        dims: dims along which up-sampling is applied. If None, up-sample along all spatial dims.
        grid: Tensor:
        padding: Extrapolation:  (Default value = extrapolation.BOUNDARY)
        dims: tuple or None:  (Default value = None)
        padding_kwargs: Additional keyword arguments to be passed to `phiml.math.pad()`.

    Returns:
      double-size grid

    """
    for dim in grid.shape.only(dims):
        left, center, right = shift(grid, (-1, 0, 1), dim.names, padding, None, padding_kwargs=padding_kwargs)
        interp_left = 0.25 * left + 0.75 * center
        interp_right = 0.75 * center + 0.25 * right
        stacked = math.stack_tensors([interp_left, interp_right], channel(_interleave='left,right'))
        grid = math.pack_dims(stacked, (dim.name, '_interleave'), dim)
    return grid


def sample_subgrid(grid: Tensor, start: Tensor, size: Shape) -> Tensor:
    """
    Samples a sub-grid from `grid` with equal distance between sampling points.
    The values at the new sample points are determined via linear interpolation.

    Args:
        grid: `Tensor` to be resampled. Values are assumed to be sampled at cell centers.
        start: Origin point of sub-grid within `grid`, measured in number of cells.
            Must have a single dimension called `vector`.
            Example: `start=(1, 0.5)` would slice off the first grid point in dim 1 and take the mean of neighbouring points in dim 2.
            The order of dims must be equal to `size` and `grid.shape.spatial`.
        size: Resolution of the sub-grid. Must not be larger than the resolution of `grid`.
            The order of dims must be equal to `start` and `grid.shape.spatial`.

    Returns:
      Sub-grid as `Tensor`
    """
    assert start.shape.names == ('vector',)
    assert grid.shape.spatial.names == size.names
    assert math.all_available(start), "Cannot perform sample_subgrid() during tracing, 'start' must be known."
    crop = {}
    for dim, d_start, d_size in zip(grid.shape.spatial.names, start, size.sizes):
        crop[dim] = slice(int(d_start), int(d_start) + d_size + (0 if d_start % 1 in (0, 1) else 1))
    grid = grid[crop]
    upper_weight = start % 1
    lower_weight = 1 - upper_weight
    for i, dim in enumerate(grid.shape.spatial.names):
        if upper_weight[i].native() not in (0, 1):
            lower, upper = shift(grid, (0, 1), [dim], padding=None, stack_dim=None)
            grid = upper * upper_weight[i] + lower * lower_weight[i]
    return grid


def find_closest(vectors: Tensor, query: Tensor, method='kd', index_dim=channel('index')):
    """
    Finds the closest vector to `query` from `vectors`.
    This is implemented using a k-d tree built from `vectors`.


    Args:
        vectors: Points to find.
        query: Target locations.
        method: One of the following:

            * `'dense'`: compute the pair-wise distances between all vectors and query points, then return the index of the smallest distance for each query point.
            * `'kd'` (default): Build a k-d tree from `vectors` and use it to query all points in `query`. The tree will be cached if this call is jit-compiled and `vectors` is constant.
        index_dim: Dimension along which components should be listed as `Shape`.
            Pass `None` to get 1D indices as scalars.

    Returns:
        Index tensor `idx` so that the closest points to `query` are `vectors[idx]`.
    """
    assert not dual(vectors), f"vectors cannot have dual dims"
    index_dim = None if index_dim is None else index_dim.with_size(non_batch(vectors).non_channel.names)
    if method == 'dense':
        dist = vec_squared(query - vectors)
        idx = math.argmin(dist, non_batch(vectors).non_channel)
        return rename_dims(idx, '_index', index_dim) if index_dim is not None else idx._index[0]
    # --- k-d tree ---
    from scipy.spatial import KDTree
    result = []
    for i in batch(vectors).meshgrid():
        query_i = query[i]
        native_query = reshaped_native(query_i, [..., channel])
        if vectors.available:
            kd_tree = KDTree(reshaped_numpy(vectors[i], [..., channel]))
            def perform_query(np_query):
                return kd_tree.query(np_query)[1]
            native_idx = query.default_backend.numpy_call(perform_query, (query_i.shape.non_channel.volume,), DType(int, 64), native_query)
        else:
            b = choose_backend_t(vectors, query)
            native_vectors = reshaped_native(vectors[i], [..., channel])
            def perform_query(np_vectors, np_query):
                return KDTree(np_vectors).query(np_query)[1]
            native_idx = b.numpy_call(perform_query, (query.shape.without(batch(vectors)).non_channel.volume,), DType(int, 64), native_vectors, native_query)
        native_multi_idx = choose_backend(native_idx).unravel_index(native_idx, vectors.shape.after_gather(i).non_channel.sizes)
        result.append(reshaped_tensor(native_multi_idx, [query_i.shape.non_channel, index_dim or math.EMPTY_SHAPE]))
    return stack(result, batch(vectors))
