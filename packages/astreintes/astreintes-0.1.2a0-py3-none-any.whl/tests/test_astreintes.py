import numpy as np
import astreintes.calculs


def test_n_astreintes():
    np.testing.assert_array_equal(np.array([9, 9, 9, 9, 8, 8]), astreintes.calculs._repartition(p=np.ones(6) * 100))

    np.testing.assert_array_equal(
        np.array([8, 9, 9, 9, 8, 9]),
        astreintes.calculs._repartition(p=np.array([0.99, 1, 1, 1, 1, 1.03]) * 100),
    )

    np.testing.assert_array_equal(
        np.array([13, 10, 10, 10, 9]),
        astreintes.calculs._repartition(np.array([4, 1, 1, 1, 1]) * 100),
    )

    np.testing.assert_array_equal(
        np.array([16, 36]),
        astreintes.calculs._repartition(np.array([2, 3]), max_astreintes=np.array([2, 5]) * 8),
    )


def test_assign():
    a = astreintes.calculs._assignation(np.array([26, 26]), seed=1234)
    np.testing.assert_array_equal(a, (np.arange(52) + 1) % 2)


def test_planning_sites():
    # colonnes sites, lignes rails

    def validate_planning(planning, n):
        assert np.all(np.bincount(planning.flatten()) == 52)
        for i in range(n):
            np.testing.assert_array_equal(np.sum(planning == i, axis=0), 1)
        assert not np.any(planning == -1)

    counts = np.array([[22, 15, 15], [13, 20, 19], [17, 17, 18]])
    validate_planning(astreintes.calculs._planning_sites(counts), n=3)

    counts = np.array([[39, 13], [13, 39]])
    validate_planning(astreintes.calculs._planning_sites(counts), n=2)
