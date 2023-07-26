import pytest

import blender


class TestBlending:
    @pytest.fixture(scope="class")
    def config(self):
        return blender.BlendingConfig(algorithm=blender.BlendingType.W_TDI, params={"weights": [0.5, 0.5]})

    @pytest.mark.parametrize("list_a, list_b", [
        ([], []),
        (["A1"], []),
        ([], ["B1"]),
        (["A1", "A2", "A3"], ["B1", "B2", "B3"]),
        (["A1", "A2", "A3"], ["B1", "B2", "B3", "B4"]),
        (["A1", "A2", "A3", "A4"], ["B1", "B2", "B3"]),
    ])
    def test_weighted_interleave(self, list_a, list_b, config):
        result = blender.blend(list_a, list_b, config=config)
        assert set(result) == set(list_a + list_b)

    def test_source_ordering_is_preserved_after_blending(self, config):
        list_a = ["A1", "A2", "A3"]
        list_b = ["B1", "B2", "B3"]
        result = list(blender.blend(list_a, list_b, config=config))
        indexes_of_a = [result.index(item) for item in result if item in list_a]
        indexes_of_b = [result.index(item) for item in result if item in list_b]
        assert indexes_of_a == sorted(indexes_of_a)
        assert indexes_of_b == sorted(indexes_of_b)


class TestWeightedTdi:
    @pytest.fixture(scope="class")
    def weighted_tdi_class(self):
        return blender.BlendingType.W_TDI

    def test_zero_weighted_list(self, weighted_tdi_class):
        weighted_tdi = weighted_tdi_class(weights=[1.0, 0.0])
        list_a = ["A1", "A2", "A3"]
        list_b = ["B1", "B2", "B3"]
        result = list(weighted_tdi.blend(list_a, list_b))
        assert result == list_a

    def test_no_weights_provided(self, weighted_tdi_class):
        with pytest.raises(AssertionError):
            weighted_tdi_class(weights=[])

    def test_missing_weight(self, weighted_tdi_class):
        weighted_tdi = weighted_tdi_class(weights=[1.0])
        list_a = ["A1", "A2", "A3"]
        list_b = ["B1", "B2", "B3"]
        result = list(weighted_tdi.blend(list_a, list_b))
        assert result == list_a

    def test_missing_list(self, weighted_tdi_class):
        weighted_tdi = weighted_tdi_class(weights=[0.5, 0.3])
        list_a = ["A1", "A2", "A3"]
        result = list(weighted_tdi.blend(list_a))
        assert result == list_a
