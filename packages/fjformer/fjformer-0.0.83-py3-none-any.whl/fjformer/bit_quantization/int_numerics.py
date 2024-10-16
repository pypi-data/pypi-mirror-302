# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Numerics for int8, int4, binary and other integer types."""

from typing import Any, Optional
from fjformer.bit_quantization import stochastic_rounding
from fjformer.bit_quantization import numerics
import flax.struct
from jax import lax
import jax.numpy as jnp


class IntNumerics(numerics.QNumerics, flax.struct.PyTreeNode):
	"""Numerics for int8, int4, binary, etc."""

	bits: int
	preserve_zero: bool
	preserve_max_val: bool
	clip: bool
	clip_gradient: bool
	round: bool
	noise_fn: Optional[stochastic_rounding.NoiseFn]
	dtype: Optional[Any] = None

	def get_edge_of_last_int_bucket(self):
		ret = 2.0 ** (self.bits - 1)
		if self.preserve_zero:
			# Lose one bucket.
			ret -= 0.5
		return ret

	def get_center_of_last_int_bucket(self):
		return self.get_edge_of_last_int_bucket() - 0.5

	def abs_val_mapped_to(self):
		if self.preserve_max_val:
			return self.get_center_of_last_int_bucket()
		else:
			return self.get_edge_of_last_int_bucket()

	def _get_fwd_clip_bound(self):
		# If we are not rounding, we just clip to bucket edges.
		fwd_clip_bound = self.get_edge_of_last_int_bucket()
		# If, after clip, we are rounding, we need to make sure that
		# we won't round values at the clip_bound away to the
		# non-existing bucket.
		if self.round:
			# Reducing fwd_clip_bound by any value in (0.0, 1.0) is correct.
			fwd_clip_bound -= 0.5
		return fwd_clip_bound

	def get_dtype(self):
		return self.dtype

	def fwd(self, x, context):
		"""Forward pass."""
		assert self.bits <= 22, "Too many bits, float32 has less precision."
		# Maybe noise
		if self.noise_fn:
			assert context.key is not None, (
				"noise_fn is set, requestic stochastic rounding, but RNG was not "
				"passed in Context.key"
			)
			x = (x + self.noise_fn(x.shape, context.key)).astype(x.dtype)

		if self.clip:
			fwd_clip_bound = self._get_fwd_clip_bound()
			x = jnp.clip(x, -fwd_clip_bound, fwd_clip_bound)

		# Maybe round
		if self.round:
			round_to_halves = not self.preserve_zero
			if round_to_halves:
				x = jnp.floor(x) + 0.5
			else:
				x = lax.round(x, lax.RoundingMethod.TO_NEAREST_EVEN)

		return x

	def vjp_fwd(self, x, context):
		res = (x,)
		return self.fwd(x, context), res

	def vjp_bwd(self, res, grad):
		# Gradient of the clip function.
		# For boundary values we will have full gradient.
		# When using abs(max(x)) scaling, x is always in the interior, and the
		# gradient clip is always 1. So, we can always set clip_gradient to false.
		# However, other types of scaling may result in x being outside (i.e., there
		# is clipping). In that case it may be desirable to make the gradient zero.
		ret = grad
		if self.clip_gradient:
			(x,) = res
			clip_bound = self._get_fwd_clip_bound()
			ret *= (-clip_bound <= x) * (x <= clip_bound)
		return (ret, None)
