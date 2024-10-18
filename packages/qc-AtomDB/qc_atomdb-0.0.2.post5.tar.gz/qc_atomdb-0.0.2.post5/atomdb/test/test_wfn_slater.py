# -*- coding: utf-8 -*-
# AtomDB is an extended periodic table database containing experimental
# and/or computational information on stable ground state
# and/or excited states of neutral and charged atomic species.
#
# Copyright (C) 2014-2015 The AtomDB Development Team
#
# This file is part of AtomDB.
#
# AtomDB is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# AtomDB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --
#

from importlib_resources import files

import os

import pytest

import numpy as np

from numpy.testing import assert_almost_equal

from atomdb import load


# get test data path
TEST_DATAPATH = files("atomdb.test.data")
TEST_DATAPATH = os.fspath(TEST_DATAPATH._paths[0])


@pytest.mark.parametrize(
    "atom, mult, answer",
    [
        ("He", 1, -2.861679996),
        ("Be", 1, -14.573023167),
        ("Ag", 2, -5197.698467674),
        ("Ne", 1, -128.547098079),
    ],
)
def test_slater_energy_especies(atom, mult, answer):
    # load species and check energy
    sp = load(atom, 0, mult, dataset="slater", datapath=TEST_DATAPATH)
    assert_almost_equal(sp.energy, answer, decimal=6)


@pytest.mark.parametrize(
    "atom, charge, mult, answer, tol",
    [
        ("He", 0, 1, 2.861679997, 5),
        ("Be", 0, 1, 14.573023130, 5),
        ("B", 0, 2, 24.529060725, 5),
        ("Cl", 0, 2, 459.482072308, 3),
        ("Ag", 0, 2, 5197.698468984, 2),
        ("C", 1, 2, 37.292223758, 5),
        ("C", -1, 4, 37.708843614, 5),
    ],
)
def test_slater_positive_definite_kinetic_energy(atom, charge, mult, answer, tol):
    # load atomic and density data
    sp = load(atom, charge, mult, dataset="slater", datapath=TEST_DATAPATH)
    # get KED computed on an equally distant radial grid
    grid = sp._data.rs
    energ = sp._data.ked_tot
    integral = np.trapz(energ, grid)
    assert_almost_equal(integral, answer, decimal=tol)
    # check interpolated density
    spline = sp.ked_func(spin="t")
    assert np.allclose(spline(grid), energ, atol=1e-6)


@pytest.mark.parametrize(
    "atom, mult, num_elect", [("H", 2, 1.0), ("Be", 1, 4.0), ("C", 3, 6.0), ("Ne", 1, 10.0)]
)
def test_slater_atomic_density(atom, mult, num_elect):
    # load Be atomic and density data
    sp = load(atom, 0, mult, dataset="slater", datapath=TEST_DATAPATH)

    # get radial grid points, total density, and its spline interpolation
    grid = sp._data.rs
    dens = sp._data.dens_tot
    spline = sp.dens_func(spin="t")

    # check shape of density and radial grid
    assert dens.shape == grid.shape

    # check density integrates to the number of electrons
    assert_almost_equal(4 * np.pi * np.trapz(grid**2 * dens, grid), num_elect, decimal=3)

    # check interpolated density values compared to reference values
    assert np.allclose(spline(grid), dens, atol=1e-6)


@pytest.mark.parametrize(
    "atom, charge, mult, num_elect", [("H", -1, 1, 2.0), ("C", -1, 4, 7.0), ("C", 1, 2, 5.0)]
)
def test_slater_atomic_density_ions(atom, charge, mult, num_elect):
    # load atomic and density data
    sp = load(atom, charge, mult, dataset="slater", datapath=TEST_DATAPATH)

    # get radial grid points, total density, and its spline interpolation
    grid = sp._data.rs
    dens = sp._data.dens_tot
    spline = sp.dens_func(spin="t")

    # check shape of density and radial grid
    assert dens.shape == grid.shape

    # check density integrates to the number of electrons
    assert_almost_equal(4 * np.pi * np.trapz(grid**2 * dens, grid), num_elect, decimal=3)

    # check interpolated density values compared to reference values
    assert np.allclose(spline(grid), dens, atol=1e-6)


@pytest.mark.xfail(reason="Test using old data of interpolated splines.")
@pytest.mark.parametrize(
    "atom, charge, mult", [("H", 0, 2), ("Be", 0, 1), ("Cl", 0, 2), ("Ne", 0, 1)]
)
def test_slater_atomic_density_gradient(atom, charge, mult):
    # load atomic and density data and get density derivative evaluated on a radial grid
    sp = load(atom, charge, mult, dataset="slater", datapath=TEST_DATAPATH)
    grid = sp._data.rs
    spline = sp.d_dens_func(spin="t")
    gradient = spline(grid)

    # get reference values from Slater wfn raw files
    id = f"{str(sp.atnum).zfill(3)}_q{str(charge).zfill(3)}_m{mult:02d}"
    fname = f"{id}_slater_gradient.npy"
    answer = np.load(f"{TEST_DATAPATH}/slater/db/{fname}")

    # check shape of arrays and array elements
    assert gradient.shape == answer.shape

    # check interpolated density gradient values compared to reference values
    assert np.allclose(gradient, answer, rtol=1e-3)


@pytest.mark.xfail(reason="Test using old data of interpolated splines.")
def test_slater_h_anion_density_splines():
    # load H^- atomic and density data and  get density evaluated on an equally
    # distant radial grid: np.arange(0.0, 15.0, 0.00001)
    charge = -1
    mult = 1
    sp = load("H", charge, mult, dataset="slater", datapath=TEST_DATAPATH)
    grid = sp._data.rs
    dens = sp._data.dens_tot
    # check interpolated densities
    spline_dens = sp.dens_func(spin="t")
    assert np.allclose(spline_dens(grid), dens, atol=1e-6)
    # check interpolated kinetic energy density
    spline = sp.ked_func(spin="t")
    assert np.allclose(spline(grid), sp._data.ked_tot, atol=1e-6)

    # load reference values for gradient
    id = f"{str(sp.atnum).zfill(3)}_q{str(charge).zfill(3)}_m{mult:02d}"
    fname = f"{id}_slater_gradient.npy"
    gradient = np.load(f"{TEST_DATAPATH}/slater/db/{fname}")

    # check interpolated density gradient vs reference values
    spline = sp.d_dens_func(spin="t")
    assert np.allclose(spline(grid), gradient, atol=1e-6)

    # check density spline second derivative vs derivative of reference gradient values
    # FIXME: second derivative has high error
    d2dens = np.gradient(gradient, sp.rs)
    spline = sp.dd_dens_func(spin="t")
    assert np.allclose(spline_dens(grid, deriv=2), d2dens, atol=1e-2)


@pytest.mark.parametrize(
    "atom, charge, mult", [("H", 0, 2), ("Be", 0, 1), ("Cl", 0, 2), ("Ne", 0, 1)]
)
def test_slater_density_gradient_spin(atom, charge, mult):
    # load atomic and density data and get density derivative evaluated on a radial grid
    sp = load(atom, charge, mult, dataset="slater", datapath=TEST_DATAPATH)
    grid = np.arange(1e-5, 15.0, 0.05)
    spline = sp.d_dens_func(spin="t")
    splinea = sp.d_dens_func(spin="a")
    splineb = sp.d_dens_func(spin="b")
    gradient_t = spline(grid)
    gradient_ab = splinea(grid) + splineb(grid)

    # check interpolated density gradient values compared to reference values
    assert np.allclose(gradient_t, gradient_ab, rtol=1e-3)


def test_slater_missing_attributes():
    # load He data
    sp = load("He", 0, 1, dataset="slater", datapath=TEST_DATAPATH)
    # check missing attributes default to None
    assert sp.mu is None
    assert sp.eta is None


def test_slater_orbitals_be():
    # Load Be data
    sp = load("Be", 0, 1, dataset="slater", datapath=TEST_DATAPATH)

    # check mo energy and occupation arrays
    # check array shapes
    assert len(sp._data.mo_energy_a) == 2
    assert len(sp._data.mo_energy_a) == len(sp._data.mo_energy_b)
    assert len(sp._data.mo_occs_a) == 2
    assert len(sp._data.mo_occs_a) == len(sp._data.mo_occs_b)
    # check array elements
    assert np.allclose(sp._data.mo_energy_a, np.array([-4.7326699, -0.3092695]), atol=1e-6)
    assert np.allclose(sp._data.mo_energy_b, np.array([-4.7326699, -0.3092695]), atol=1e-6)
    assert np.allclose(sp._data.mo_occs_a, np.array([1.0, 1.0]), atol=1e-6)
    assert np.allclose(sp._data.mo_occs_b, np.array([1.0, 1.0]), atol=1e-6)


def test_slater_orbitals_ne():
    # Load Ne data
    sp = load("Ne", 0, 1, dataset="slater", datapath=TEST_DATAPATH)

    # check mo energy and occupation arrays
    # check array shapes
    assert len(sp._data.mo_energy_a) == 5
    assert len(sp._data.mo_energy_a) == len(sp._data.mo_energy_b)
    assert len(sp._data.mo_occs_a) == 5
    assert len(sp._data.mo_occs_a) == len(sp._data.mo_occs_b)
    # check array elements
    assert np.allclose(
        sp._data.mo_energy_a,
        np.array([-32.7724425, -1.9303907, -0.8504095, -0.8504095, -0.8504095]),
        atol=1e-6,
    )
    assert np.allclose(sp._data.mo_energy_a, sp._data.mo_energy_b, atol=1e-6)
    assert np.allclose(sp._data.mo_occs_a, np.array([1.0, 1.0, 1.0, 1.0, 1.0]), atol=1e-6)
    assert np.allclose(sp._data.mo_occs_a, sp._data.mo_occs_b, atol=1e-6)


def test_slater_orbitals_h():
    # Load H data
    sp = load("H", 0, 2, dataset="slater", datapath=TEST_DATAPATH)

    # check mo energy and occupation arrays
    # check array shapes
    assert len(sp._data.mo_energy_a) == 1
    assert len(sp._data.mo_energy_a) == len(sp._data.mo_energy_b)
    assert len(sp._data.mo_occs_a) == 1
    assert len(sp._data.mo_occs_a) == len(sp._data.mo_occs_b)
    # check array elements
    assert np.allclose(sp._data.mo_energy_a, np.array([-0.50]), atol=1e-6)
    assert np.allclose(sp._data.mo_energy_b, np.array([-0.50]), atol=1e-6)
    assert np.allclose(sp._data.mo_occs_a, np.array([1.0]), atol=1e-6)
    assert np.allclose(sp._data.mo_occs_b, np.array([0.0]), atol=1e-6)


def test_slater_orbitals_h_anion():
    # Load H data
    sp = load("H", -1, 1, dataset="slater", datapath=TEST_DATAPATH)

    # check mo energy and occupation arrays
    # check array shapes
    assert len(sp._data.mo_energy_a) == 1
    assert len(sp._data.mo_energy_a) == len(sp._data.mo_energy_b)
    assert len(sp._data.mo_occs_a) == 1
    assert len(sp._data.mo_occs_a) == len(sp._data.mo_occs_b)
    # check array elements
    assert np.allclose(sp._data.mo_energy_a, np.array([-0.0462224]), atol=1e-6)
    assert np.allclose(sp._data.mo_energy_b, np.array([-0.0462224]), atol=1e-6)
    assert np.allclose(sp._data.mo_occs_a, np.array([1.0]), atol=1e-6)
    assert np.allclose(sp._data.mo_occs_b, np.array([1.0]), atol=1e-6)


@pytest.mark.xfail(reason="Test for old version of Slater dataset code.")
def test_slater_orbitals_ag():
    # Load the Ag file.
    sp = load("Ag", 0, 2, dataset="slater", datapath=TEST_DATAPATH)

    # check mo energy and occupation arrays
    # check array shapes
    assert len(sp._data.mo_energy_a) == 10
    assert len(sp._data.mo_energy_a) == len(sp._data.mo_energy_b)
    assert len(sp._data.mo_occs_a) == 10
    assert len(sp._data.mo_occs_a) == len(sp._data.mo_occs_b)
    # check array elements
    energy = np.array(
        [
            -913.8355964,
            -134.8784068,
            -25.9178242,
            -4.0014988,
            -0.2199797,
            -125.1815809,
            -21.9454343,
            -2.6768201,
            -14.6782003,
            -0.5374007,
        ]
    )
    assert np.allclose(sp._data.mo_energy_a, energy, atol=1e-6)
    assert np.allclose(sp._data.mo_energy_b, energy, atol=1e-6)
    assert np.allclose(
        sp._data.mo_occs_a, np.array([1.0, 1.0, 1.0, 1.0, 1.0, 3.0, 3.0, 3.0, 5.0, 5.0]), atol=1e-6
    )
    assert np.allclose(
        sp._data.mo_occs_b, np.array([1.0, 1.0, 1.0, 1.0, 0.0, 3.0, 3.0, 3.0, 5.0, 5.0]), atol=1e-6
    )
