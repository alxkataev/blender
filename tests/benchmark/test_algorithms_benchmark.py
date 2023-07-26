import pytest

import blender


@pytest.mark.parametrize('n', [10, 100, 1000, 10000, 100000])
def test_weighted_tdi_benchmark(benchmark, n):
    gen = blender.blend(*[list(map(str, range(n))) for _ in range(2)],
                        config=blender.BlendingConfig(params={'weights': [0.5, 0.5]}))
    benchmark(list, gen)
