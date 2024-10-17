# -*- coding: utf-8 -*-
"""volume discretization structure class
"""
import warnings

import torch

from torchgdm.constants import (
    DTYPE_FLOAT,
    DTYPE_COMPLEX,
    COLORS_DEFAULT,
)
from torchgdm.tools.misc import get_default_device
from torchgdm.struct.base_classes import StructBase
from torchgdm.tools.geometry import get_step_from_geometry
from torchgdm.tools.geometry import rotation_y
from torchgdm.tools.misc import ptp


class StructDiscretized2D(StructBase):
    """base class 2D surface discretized structure with infinite axis

    Defines the 2D surface discretization, its polarizabilities and self-terms
    """

    __name__ = "2D discretized structure"

    def __init__(
        self,
        positions: torch.Tensor,
        materials,
        step=None,
        device: torch.device = None,
        **kwargs
    ):
        """2D discretized structure

        Args:
            positions (torch.Tensor): meshpoint positions (3D, but all y values must be zero)
            materials (material class, or list of them): material of structure. If list, define the material of each meshpoint.
            step (float, optional): nominal stepsize. If not provided, infer automatically from geometry. Defaults to None.
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).

        Raises:
            ValueError: No mesh points at y=0, Invalid material config
        """
        super().__init__(device=device, **kwargs)
        self.mesh = "2D"

        self.positions = torch.as_tensor(
            positions, dtype=DTYPE_FLOAT, device=self.device
        )
        if torch.count_nonzero(self.positions[..., 1]) > 0:
            warnings.warn("2D structure. Remove all positions with y!=0.")
            self.positions = self.positions[self.positions[..., 1] != 0]
            if len(self.positions) == 0:
                raise ValueError("No mesh positions at y=0. Please check geometry.")

        self.r0 = self.get_center_of_mass()  # center of gravity

        if step is None:
            step_scalar = get_step_from_geometry(self.positions)
        else:
            step_scalar = step

        # step for every meshcell, for consistency with other struct classes
        self.step = step_scalar * torch.ones(
            len(self.positions), dtype=DTYPE_FLOAT, device=self.device
        )

        self.radiative_correction = False  # not implemented
        self.mesh_normalization_factor = torch.as_tensor(
            1, dtype=DTYPE_FLOAT, device=self.device
        )  # square mesh

        # material of each meshpoint
        if hasattr(materials, "__iter__"):
            if len(materials) != len(self.positions):
                raise ValueError(
                    "Either a global material needs to be given or "
                    + "each meshpoint needs a defined material. "
                    + "But meshpoint list and materials list are of different lengths."
                )
            self.materials = materials
        else:
            self.materials = [materials for i in self.positions]

        self.zeros = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )

        # discretized, made from natural material: only electric response
        self.evaluation_terms = ["E"]  # possible terms 'E' and 'H'

    def __repr__(self, verbose=False):
        """description about structure"""
        out_str = ""
        out_str += "------ discretized 2D nano-object -------"
        out_str += "\n" + " mesh type:              {}".format(self.mesh)
        out_str += "\n" + " nr. of meshpoints:      {}".format(len(self.positions))
        out_str += "\n" + " nominal stepsizes (nm): {}".format(
            [float(f) for f in torch.unique(self.step)]
        )
        out_str += "\n" + " material:               {}".format(
            [m.__name__ for m in set(self.materials)]
        )
        bnds = ptp(self.positions, dim=0)
        out_str += "\n" + " size & position (Y-axis is infinite):"
        out_str += "\n" + "     X-extension          :   {:.1f} (nm)".format(bnds[0])
        out_str += "\n" + "     Z-extension          :   {:.1f} (nm)".format(bnds[2])
        out_str += "\n" + "     center of mass (x,z) : ({:.1f}, {:.1f})".format(
            self.r0[0], self.r0[2]
        )

        return out_str

    def set_device(self, device):
        """move all tensors of the class to device"""
        super().set_device(device)

        self.zeros = self.zeros.to(device)
        self.step = self.step.to(device)
        self.r0 = self.r0.to(device)
        self.mesh_normalization_factor = self.mesh_normalization_factor.to(device)

        for mat in self.materials:
            mat.set_device(device)

    # --- self-terms
    def get_selfterm_pE(self, wavelength: float, environment) -> torch.Tensor:
        """return list of 'EE' self-term tensors (3x3) at each meshpoint

        Args:
            wavelength (float): in nm
            environment (environment class): 2D environement class

        Returns:
            torch.Tensor: pE self term tensor
        """
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=self.positions
        )
        # cast env permittivity to real, because hankel only support real args
        eps_env = torch.as_tensor(eps_env, dtype=DTYPE_COMPLEX, device=self.device).real

        k0 = 2 * torch.pi / wavelength
        k02 = k0**2

        if self.mesh_normalization_factor == 0:
            norm_xz = 0
            norm_y = 0
        else:
            from torchgdm.tools.special import H1n

            S = self.step**2
            k0_y = environment.get_k0_y(wavelength)

            kr2 = torch.as_tensor(
                eps_env * k02 - k0_y**2, dtype=DTYPE_FLOAT, device=self.device
            )
            kr = torch.sqrt(kr2)

            h11 = H1n(1, kr * self.step / torch.pi**0.5)
            norm01 = self.step / torch.pi**0.5 * h11 / kr + 2j / (torch.pi * kr**2)

            norm_xz_nonrad = -1 * self.mesh_normalization_factor / (2.0 * S * eps_env)
            norm_xz_rad = 1j * torch.pi * (2 * k02 - kr2 / eps_env) * norm01 / (4 * S)

            norm_y_nonrad = 0
            norm_y_rad = 1j * torch.pi * (k02 - k0_y**2 / eps_env) * norm01 / (2 * S)

            norm_xz = 4.0 * torch.pi * (norm_xz_nonrad + norm_xz_rad)
            norm_y = 4.0 * torch.pi * (norm_y_nonrad + norm_y_rad)

        self_terms_pE = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )
        self_terms_pE[:, 0, 0] = norm_xz
        self_terms_pE[:, 1, 1] = norm_y
        self_terms_pE[:, 2, 2] = norm_xz

        return self_terms_pE

    # --- polarizabilities
    def get_polarizability_pE(self, wavelength: float, environment) -> torch.Tensor:
        """return list of EE polarizability tensors (3x3) at each meshpoint

        Args:
            wavelength (float): in nm
            environment (environment class): 2D environement class

        Returns:
            torch.Tensor: pE polarizability tensor
        """
        eps_env = environment.get_environment_permittivity_scalar(
            wavelength, r_probe=self.positions
        )
        eps_env_tensor = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )
        eps_env_tensor[:, 0, 0] = eps_env
        eps_env_tensor[:, 1, 1] = eps_env
        eps_env_tensor[:, 2, 2] = eps_env

        eps_geo = torch.zeros(
            (len(self.positions), 3, 3), dtype=DTYPE_COMPLEX, device=self.device
        )
        for i, mat in enumerate(self.materials):
            eps_geo[i] = mat.get_epsilon(wavelength)

        S_cell_norm = self.step**2 / float(self.mesh_normalization_factor)

        # --- polarizability
        alpha_pE = (
            (eps_geo - eps_env_tensor)
            * S_cell_norm.unsqueeze(1).unsqueeze(1)
            / (4.0 * torch.pi)
        )

        return alpha_pE

    def convert_to_effective_polarizability_pair(
        self, environment, wavelengths, test_accuracy=False, **kwargs
    ):
        raise NotImplementedError("Not yet implemented!")
        # from torchgdm.postproc.multipole import extract_effective_polarizability
        # from torchgdm.struct import StructEffPola3D

        # alpha = extract_effective_polarizability(
        #     struct=self, environment=environment, wavelengths=wavelengths, **kwargs
        # )
        # struct_aeff = StructEffPola3D(
        #     positions=torch.stack([self.r0]),
        #     alpha_dicts=[alpha],
        #     environment=environment,
        #     device=self.device,
        # )

        # if test_accuracy:
        #     from torchgdm.postproc.multipole import (
        #         test_effective_polarizability_accuracy,
        #     )

        #     test_effective_polarizability_accuracy(struct_aeff, self)

        # return struct_aeff

    # --- plotting
    def plot(self, **kwargs):
        """plot the structure in XZ plane (2D)"""
        from torchgdm.visu import visu2d

        kwargs["projection"] = "xz"
        im = visu2d.geo2d._plot_structure_discretized(self, **kwargs)
        return im

    def plot_contour(self, **kwargs):
        """plot the structure contour in XZ plane (2D)"""
        from torchgdm.visu import visu2d

        kwargs["projection"] = "xz"
        im = visu2d.geo2d._plot_contour_discretized(self, **kwargs)
        return im

    def plot3d(self, **kwargs):
        """plot the structure in 3D"""
        from torchgdm.visu import visu3d

        warnings.warn(
            "Visualizing a 2D model in 3D will show only meshpoints in the 'XZ' plane."
        )

        return visu3d.geo3d._plot_structure_discretized(self, **kwargs)

    # --- geometry operations
    def rotate(
        self,
        alpha: float,
        center: torch.Tensor = torch.as_tensor([0.0, 0.0, 0.0]),
        axis: str = "y",
    ):
        """rotate the structure

        Args:
            alpha (float): rotation angle (in rad)
            center (torch.Tensor, optional): center of rotation axis. Defaults to torch.as_tensor([0.0, 0.0, 0.0]).
            axis (str, optional): rotation axis. Defaults to "y".

        Raises:
            ValueError: only "y" axis supported in 2D

        Returns:
            :class:`StructDiscretized2D`: copy of structure with rotated geometry
        """
        _struct_rotated = self.copy()
        center = center.to(dtype=DTYPE_FLOAT, device=self.device)

        if axis.lower() == "y":
            rot = rotation_y(alpha, device=self.device)
        else:
            raise ValueError(
                "Only rotation axis 'y' supported in 2D (infinite axis).".format(axis)
            )

        if len(_struct_rotated.positions) > 1:
            _struct_rotated.positions = torch.matmul(
                _struct_rotated.positions - (center + self.r0), rot
            ) + (center + self.r0)
        else:
            warnings.warn("Single meshpoint found, ignore rotation.")

        return _struct_rotated


class StructDiscretizedSquare2D(StructDiscretized2D):
    """class for square surface discretized, infinitely long 2D structure

    Defines the square surface discretization, polarizabilities and self-terms
    """

    __name__ = "2D square lattice discretized structure class"

    def __init__(
        self,
        discretization_config,
        step,
        materials,
        device: torch.device = None,
        **kwargs
    ):
        """2D structure, discretized on a square lattice

        Infinite axis along Y

        Args:
            discretization_config (tuple): tuple of discretization condition function, and discretizer walk limits (as provided by the geometries generators)
            step (float, optional): nominal stepsize. If not provided, infer automatically from geometry. Defaults to None.
            materials (material class, or list of them): material of structure. If list, define the material of each meshpoint.
            device (torch.device, optional): Defaults to "cpu" (can be changed by :func:`torchgdm.use_cuda`).

        Raises:
            ValueError: No mesh points at y=0, Invalid material config
        """
        from torchgdm.struct.surface_2d import discretizer_square

        positions = discretizer_square(*discretization_config, step=step)

        super().__init__(positions, materials, step=step, device=device, **kwargs)

        self.mesh = "square (2D)"
        self.mesh_normalization_factor = torch.tensor(
            1.0, dtype=DTYPE_FLOAT, device=self.device
        )
