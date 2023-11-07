import pytest
import copy

from MatchedMap import MatchedMap

NAMES: list[str] = [
    'oak',
    'elm',
    'pine',
    'spruce',
    'mahogany',
    'birch',
    'juniper',
    'beech',
    'poplar',
    'fir',
    'baobab',
]


def test_MatchedMap_() -> None:
    """ ... """
    mapper: MatchedMap = MatchedMap(NAMES)
    matched_map: dict[str, str] = mapper.generate_matched_map()

    keys: list[str] = list(matched_map.keys())
    vals: list[str] = list(matched_map.values())

    assert len(set(NAMES)) == len(set(keys)) == len(set(vals))

    for k, v in matched_map.items():
        # Should not be assigned to itself
        assert matched_map[k] != k

        # Should not be reciprocal
        assert matched_map[v] != k


def test_MatchedMap_reciprocal() -> None:
    """ ... """
    recip_names: list[str] = copy.deepcopy(NAMES)

    if len(recip_names) % 2 == 0:
        # Ensure error condition (non-even number of recip_names)
        recip_names.append('odd')
    
    with pytest.raises(ValueError):
        mapper: MatchedMap = MatchedMap(recip_names)
        mapper.match_to_reciprocal = True
        matched_map: dict[str, str] = mapper.generate_matched_map()

    # Get to an even number of recip_names
    recip_names.pop()

    mapper: MatchedMap = MatchedMap(recip_names)
    mapper.match_to_reciprocal = True
    matched_map: dict[str, str] = mapper.generate_matched_map()

    keys: list[str] = list(matched_map.keys())
    vals: list[str] = list(matched_map.values())

    assert len(set(recip_names)) == len(set(keys)) == len(set(vals))

    # Should be reciprocal
    for k, v in matched_map.items():
        assert matched_map[v] == k


def test_MatchedMap_forbidden() -> None:
    """ ... """
    # Set up forbidden matches
    forbid_mapper: MatchedMap = MatchedMap(NAMES)
    forbidden: dict[str, str] = forbid_mapper.generate_matched_map()

    mapper: MatchedMap = MatchedMap(NAMES)
    mapper.set_forbidden_matches(forbidden)
    matched_map: dict[str, str] = mapper.generate_matched_map()

    keys: list[str] = list(matched_map.keys())
    vals: list[str] = list(matched_map.values())

    assert len(set(NAMES)) == len(set(keys)) == len(set(vals))

    for k in matched_map.keys():
        assert matched_map[k] != forbidden[k]


def test_MatchedMap_invalid_forbidden() -> None:
    """ ... """
    # Set up forbidden matches
    forbid_mapper: MatchedMap = MatchedMap(NAMES)
    forbidden: dict[str, str] = forbid_mapper.generate_matched_map()

    #  Make sure the forbidden dict is invalid (i.e., contains extra names)
    forbidden['aspen'] = 'oak'

    mapper: MatchedMap = MatchedMap(NAMES)

    with pytest.raises(ValueError):
        mapper.set_forbidden_matches(forbidden)
