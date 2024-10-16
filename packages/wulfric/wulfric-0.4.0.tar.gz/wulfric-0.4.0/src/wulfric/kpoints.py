# Wulfric - Crystal, Lattice, Atoms, K-path.
# Copyright (C) 2023-2024 Andrey Rybakov
#
# e-mail: anry@uv.es, web: adrybakov.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from copy import deepcopy
from typing import Iterable

import numpy as np

from wulfric.geometry import absolute_to_relative

__all__ = ["Kpoints"]


class Kpoints:
    r"""
    K-point path.

    Parameters
    ----------
    b1 : (3,) array-like
        First reciprocal lattice vector :math:`\mathbf{b_1}`.
    b2 : (3,) array-like
        Second reciprocal lattice vector :math:`\mathbf{b_2}`.
    b3 : (3,) array-like
        Third reciprocal lattice vector :math:`\mathbf{b_3}`.
    coordinates : list, optional
        Coordinates are given in relative coordinates in reciprocal space.
    names: list, optional
        Names of the high symmetry points. Used for programming, not for plotting.
    labels : list, optional
        Dictionary of the high symmetry points labels for plotting.
        Has to have the same length as ``coordinates``.
    path : str, optional
        K points path.
    n : int
        Number of points between each pair of the high symmetry points
        (high symmetry points excluded).

    Attributes
    ----------
    b1 : (3,) :numpy:`ndarray`
        First reciprocal lattice vector :math:`\mathbf{b_1}`.
    b2 : (3,) :numpy:`ndarray`
        Second reciprocal lattice vector :math:`\mathbf{b_2}`.
    b3 : (3,) :numpy:`ndarray`
        Third reciprocal lattice vector :math:`\mathbf{b_3}`.
    hs_names : list
        Names of the high symmetry points. Used for programming, not for plotting.
    hs_coordinates : dict
        Dictionary of the high symmetry points coordinates.

        .. code-block:: python

            {"name": [k_a, k_b, k_c], ... }

    hs_labels : dict
        Dictionary of the high symmetry points labels for plotting.

        .. code-block:: python

            {"name": "label", ... }
    """

    def __init__(
        self, b1, b2, b3, coordinates=None, names=None, labels=None, path=None, n=100
    ) -> None:
        self.b1 = np.array(b1)
        self.b2 = np.array(b2)
        self.b3 = np.array(b3)

        if coordinates is None:
            coordinates = []

        # Fill names and labels with defaults
        if names is None:
            names = [f"K{i+1}" for i in range(len(coordinates))]
            if labels is None:
                labels = [f"K$_{i+1}$" for i in range(len(coordinates))]
        if labels is None:
            labels = [name for name in names]
        else:
            if len(labels) != len(coordinates):
                raise ValueError(
                    f"Amount of labels ({len(labels)}) does not match amount of points ({len(coordinates)})."
                )

        # Define high symmetry points attributes
        self.hs_coordinates = dict(
            [(names[i], np.array(coordinates[i])) for i in range(len(coordinates))]
        )
        self.hs_labels = dict([(names[i], labels[i]) for i in range(len(coordinates))])
        self.hs_names = names

        self._n = n

        self._path = None
        if path is None:
            path = "-".join(self.hs_names)
        self.path = path

    ################################################################################
    #                            High symmetry points                              #
    ################################################################################
    def add_hs_point(self, name, coordinates, label, relative=True):
        r"""
        Add high symmetry point.

        Parameters
        ----------
        name : str
            Name of the high symmetry point.
        coordinates : (3,) array-like
            Coordinates of the high symmetry point.
        label : str
            Label of the high symmetry point, ready to be plotted.
        relative : bool, optional
            Whether to interpret coordinates as relative or absolute.
        """

        if name in self.hs_names:
            raise ValueError(f"Point '{name}' already defined.")

        if not relative:
            coordinates = absolute_to_relative(
                coordinates, np.array([self.b1, self.b2, self.b3])
            )

        self.hs_names.append(name)
        self.hs_coordinates[name] = np.array(coordinates)
        self.hs_labels[name] = label

    def remove_hs_point(self, name):
        r"""
        Remove high symmetry point.

        Parameters
        ----------
        name : str
            Name of the high symmetry point.
        """

        if name in self.hs_names:
            self.hs_names.remove(name)
            del self.hs_coordinates[name]
            del self.hs_labels[name]

    ################################################################################
    #                                Path attributes                               #
    ################################################################################
    @property
    def path(self):
        r"""
        K points path.

        Returns
        -------
        path : list of list of str
            K points path. Each subpath is a list of the high symmetry points.
        """

        return self._path

    @path.setter
    def path(self, new_path):
        if isinstance(new_path, str):
            tmp_path = new_path.split("|")
            new_path = []
            for i in range(len(tmp_path)):
                subpath = tmp_path[i].split("-")
                # Each subpath has to contain at least two points.
                if len(subpath) != 1:
                    new_path.append(subpath)
        elif isinstance(new_path, Iterable):
            tmp_path = new_path
            new_path = []
            for subpath in tmp_path:
                if isinstance(subpath, str) and "-" in subpath:
                    subpath = subpath.split("-")
                    # Each subpath has to contain at least two points.
                    if len(subpath) != 1:
                        new_path.append(subpath)
                elif (
                    not isinstance(subpath, str)
                    and isinstance(subpath, Iterable)
                    and len(subpath) != 1
                ):
                    new_path.append(subpath)
                else:
                    new_path = [tmp_path]
                    break
        # Check if all points are defined.
        for subpath in new_path:
            for point in subpath:
                if point not in self.hs_names:
                    message = f"Point '{point}' is not defined. Defined points are:"
                    for defined_name in self.hs_names:
                        message += (
                            f"\n  {defined_name} : {self.hs_coordinates[defined_name]}"
                        )
                    raise ValueError(message)
        self._path = new_path

    @property
    def path_string(self):
        r"""
        K points path as a string.

        Returns
        -------
        path : str
        """

        result = ""
        for s_i, subpath in enumerate(self.path):
            for i, name in enumerate(subpath):
                if i != 0:
                    result += "-"
                result += name
            if s_i != len(self.path) - 1:
                result += "|"

        return result

    @property
    def n(self):
        r"""
        Amount of points between each pair of the high symmetry points
        (high symmetry points excluded).

        Returns
        -------
        n : int
        """

        return self._n

    @n.setter
    def n(self, new_n):
        if not isinstance(new_n, int):
            raise ValueError(
                f"n has to be integer. Given: {new_n}, type = {type(new_n)}"
            )
        self._n = new_n

    ################################################################################
    #                         Attributes for the axis ticks                        #
    ################################################################################
    @property
    def labels(self):
        r"""
        Labels of high symmetry points, ready to be plotted.

        For example for point "Gamma" it returns r"$\Gamma$".

        If there are two high symmetry points following one another in the path,
        it returns "X|Y" where X and Y are the labels of the two high symmetry points.

        Returns
        -------
        labels : list of str
            Labels, ready to be plotted. Same length as :py:attr:`.ticks`.
        """

        labels = []
        for s_i, subpath in enumerate(self.path):
            if s_i != 0:
                labels[-1] += "|" + self.hs_labels[subpath[0]]
            else:
                labels.append(self.hs_labels[subpath[0]])
            for name in subpath[1:]:
                labels.append(self.hs_labels[name])

        return labels

    def coordinates(self, relative=False):
        raise RuntimeError(
            "Kpoints.coordinates() was removed in v0.4.0. Use Kpoints.ticks() instead."
        )

    def ticks(self, relative=False):
        r"""
        Tick's positions of the high symmetry points, ready to be plotted.

        .. versionchanged:: 0.1.2 Renamed from ``coordinates``

        Parameters
        ----------
        relative : bool, optional
            Whether to use relative coordinates instead of the absolute ones.

        Returns
        -------
        ticks : :numpy:`ndarray`
            Tick's positions, ready to be plotted. Same length as :py:attr:`.labels`.
        """

        if relative:
            cell = np.eye(3)
        else:
            cell = np.array([self.b1, self.b2, self.b3])

        ticks = []
        for s_i, subpath in enumerate(self.path):
            if s_i == 0:
                ticks.append(0)
            for i, name in enumerate(subpath[1:]):
                ticks.append(
                    np.linalg.norm(
                        self.hs_coordinates[name] @ cell
                        - self.hs_coordinates[subpath[i]] @ cell
                    )
                    + ticks[-1]
                )

        return np.array(ticks)

    ################################################################################
    #                   Points of the path with intermediate ones                  #
    ################################################################################
    def points(self, relative=False):
        r"""
        Coordinates of all points with n points between each pair of the high
        symmetry points (high symmetry points excluded).

        Parameters
        ----------
        relative : bool, optional
            Whether to use relative coordinates instead of the absolute ones.

        Returns
        -------
        points : (N, 3) :numpy:`ndarray`
            Coordinates of all points.
        """

        if relative:
            cell = np.eye(3)
        else:
            cell = np.array([self.b1, self.b2, self.b3])

        points = None
        for subpath in self.path:
            for i in range(len(subpath) - 1):
                name = subpath[i]
                next_name = subpath[i + 1]
                new_points = np.linspace(
                    self.hs_coordinates[name] @ cell,
                    self.hs_coordinates[next_name] @ cell,
                    self._n + 2,
                )
                if points is None:
                    points = new_points
                else:
                    points = np.concatenate((points, new_points))
        return points

    # It can not just call for points and flatten them, because it has to treat "|" as a special case.
    def flatten_points(self, relative=False):
        r"""
        Flatten coordinates of all points with n points between each pair of the high
        symmetry points (high symmetry points excluded). Used to plot band structure, dispersion, etc.

        Parameters
        ----------
        relative : bool, optional
            Whether to use relative coordinates instead of the absolute ones.

        Returns
        -------
        flatten_points : (N, 3) :numpy:`ndarray`
            Flatten coordinates of all points.
        """

        if relative:
            cell = np.eye(3)
        else:
            cell = np.array([self.b1, self.b2, self.b3])

        flatten_points = None
        for s_i, subpath in enumerate(self.path):
            for i in range(len(subpath) - 1):
                name = subpath[i]
                next_name = subpath[i + 1]
                points = (
                    np.linspace(
                        self.hs_coordinates[name] @ cell,
                        self.hs_coordinates[next_name] @ cell,
                        self._n + 2,
                    )
                    - self.hs_coordinates[name] @ cell
                )
                delta = np.linalg.norm(points, axis=1)
                if s_i == 0 and i == 0:
                    flatten_points = delta
                else:
                    delta += flatten_points[-1]
                    flatten_points = np.concatenate((flatten_points, delta))
        return flatten_points

    ################################################################################
    #                                     Copy                                     #
    ################################################################################

    def copy(self):
        r"""
        Create a copy of the kpoints.

        .. versionadded:: 0.3.0

        Returns
        -------
        kpoints : :py:class:`.Kpoints`
            Copy of the kpoints.
        """

        deepcopy(self)

    ################################################################################
    #                                Human readables                               #
    ################################################################################

    def hs_table(self, decimals=8):
        r"""
        High symmetry points table.

        .. versionadded:: 0.3.1

        Parameters
        ----------
        decimals : int, optional
            Number of decimal places to round the coordinates.

        Returns
        -------
        table : str
            String with N+1 lines, where N is the amount of high symmetry points.
            Each line contains the name of the high symmetry point and its relative and
            absolute coordinates in a reciprocal space, i.e.::

                K1  0.0 0.0 0.0   0.0 0.0 0.0

            First line is a header::

                Name  rel_b1 rel_b2 rel_b3  k_x k_y k_z
        """

        d = decimals
        table = [
            (
                f"{'Name':4}  "
                + f"{'rel_b1':>{d+3}} "
                + f"{'rel_b2':>{d+3}} "
                + f"{'rel_b3':>{d+3}}  "
                + f"{'k_x':>{d+3}} "
                + f"{'k_y':>{d+3}} "
                + f"{'k_z':>{d+3}}"
            )
        ]
        for name in self.hs_names:
            relative = self.hs_coordinates[name]
            i = f"{relative[0]: {d+3}.{d}f}"
            j = f"{relative[1]: {d+3}.{d}f}"
            k = f"{relative[2]: {d+3}.{d}f}"
            absolute = self.hs_coordinates[name] @ np.array([self.b1, self.b2, self.b3])
            k_x = f"{absolute[0]: {d+3}.{d}f}"
            k_y = f"{absolute[1]: {d+3}.{d}f}"
            k_z = f"{absolute[2]: {d+3}.{d}f}"
            table.append(f"{name:4}  {i} {j} {k}  {k_x} {k_y} {k_z}")
        return "\n".join(table)
