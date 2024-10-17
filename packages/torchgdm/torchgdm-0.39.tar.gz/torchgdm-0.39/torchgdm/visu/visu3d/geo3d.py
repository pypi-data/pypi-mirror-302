# encoding=utf-8
"""
3D visualization tools for geometries
"""
# %%
import copy
import warnings

import torch

from torchgdm.constants import COLORS_DEFAULT
from torchgdm.tools.misc import to_np
from torchgdm import tools



def _plot_structure_discretized(
    struct,
    scale=1.0,
    color="auto",
    show_grid=True,
    legend=True,
    alpha=1.0,
    show="auto",
    pl=None,
):
    import numpy as np
    import pyvista as pv

    # get mesh positions and step sizes, cut in multi-materials
    pos = to_np(struct.positions)
    step = to_np(struct.step)

    if type(show) == str:
        if show.lower() == "auto" and pl is None:
            show = True
        else:
            False

    if color == "auto":
        colors = COLORS_DEFAULT
        diff_mat_names = [s.__name__ for s in struct.materials]
        mat_names = np.array(diff_mat_names)

        different_materials = np.unique(mat_names)

        mat_pos_subset_idx = []
        for pos_single_mat in different_materials:
            mat_pos_subset_idx.append(
                np.arange(len(mat_names))[mat_names == pos_single_mat]
            )
    else:
        different_materials = [""]
        mat_pos_subset_idx = [np.arange(len(pos))]  # all pos
        colors = [color]

    # the actual plot
    mesh_list = []
    for i_s, pos_idx in enumerate(mat_pos_subset_idx):
        pos_mat = pos[pos_idx]
        steplist_mat = step[pos_idx]

        pts = pv.PolyData(pos_mat)
        pts["steps"] = steplist_mat
        pts.set_active_scalars("steps")

        mesh_list.append(
            pts.glyph(geom=pv.Cube(), scale="steps", factor=scale, orient=False)
        )

    if pl is None:
        pl = pv.Plotter()

    for i_s, mesh in enumerate(mesh_list):
        label = different_materials[i_s]
        pl.add_mesh(
            mesh,
            color=colors[i_s],
            show_edges=show_grid,
            edge_color="black",
            line_width=0.5,
            opacity=alpha,
            edge_opacity=alpha,
            label=label,
        )

    if legend and len(different_materials) > 0:
        pl.add_legend(bcolor="w", face=None)

    if show:
        pl.show()

    return mesh_list

def _plot_structure_eff_pola(
    struct,
    scale=1.0,
    center_marker_scale=10,
    color="auto",
    theta_resolution=20,
    phi_resolution=20,
    sphere_style="wireframe",
    meshcolor="lightblue",
    alpha=0.1,
    alpha_grid=0.05,
    show="auto",
    pl=None,
    legend=False,
):
    from torchgdm import tools
    import numpy as np
    import pyvista as pv

    if type(show) == str:
        if show.lower() == "auto" and pl is None:
            show = True
        else:
            show = False

    if color == "auto":
        color = COLORS_DEFAULT[0]

    pos_a = to_np(struct.positions)
    enclosing_radius = to_np(struct.step)

    # create the actual plot: iterate over polarizabilities
    mesh_circ_list = []
    mesh_center_list = []
    mesh_fullgeo_list = []
    for i, pos in enumerate(pos_a):
        r = enclosing_radius[i]
        _geo = struct.full_geometries[i]
        pos_mesh = to_np(_geo)
        step_mesh = (
            to_np(tools.geometry.get_step_from_geometry(_geo))
        )

        # plot enclosing sphere
        enclose_sphere = pv.Sphere(
            r + step_mesh / 2,
            pos,
            theta_resolution=theta_resolution,
            phi_resolution=phi_resolution,
        )
        mesh_circ_list.append(enclose_sphere)

        # center pos. "marker" sphere
        mesh_center_list.append(pv.Sphere(center_marker_scale, pos))

        # full geometry mesh
        pts = pv.PolyData(pos_mesh)
        pts["steps"] = np.ones(len(pos_mesh)) * step_mesh
        pts.set_active_scalars("steps")

        mesh_fullgeo_list.append(
            pts.glyph(geom=pv.Cube(), scale="steps", factor=scale, orient=False)
        )

    if pl is None:
        pl = pv.Plotter()

    for i_s, mesh in enumerate(mesh_circ_list):
        pl.add_mesh(
            mesh,
            color=color,
            show_edges=False,
            line_width=0.5,
            edge_opacity=alpha,
            opacity=alpha,
            style=sphere_style,
        )

    for i_s, mesh in enumerate(mesh_center_list):
        pl.add_mesh(mesh, color="k")

    for i_s, mesh in enumerate(mesh_fullgeo_list):
        pl.add_mesh(
            mesh,
            color=meshcolor,
            show_edges=True,
            edge_color="black",
            line_width=0.5,
            opacity=alpha_grid,
            edge_opacity=alpha_grid * 0.1,
        )

    if show:
        pl.show()

    return mesh_circ_list, mesh_center_list, mesh_fullgeo_list


def structure(
    struct,
    color="fix",
    scale=1,
    legend=True,
    alpha=1,
    show="auto",
    pl=None,
    **kwargs,
):
    """plot structure in 2d, projected to e.g. the XY plane

    plot the structure `struct` as a scatter projection to a carthesian plane.
    Either from list of coordinates, or using a simulation definition as input.

    kwargs are passed to matplotlib's `scatter`

    Parameters
    ----------
    struct : list or :class:`.simulation.Simulation`
          either list of 3d coordinate tuples or simulation description object

    projection : str or list, default: 'auto'
        which 2D projection to plot: "auto", "XY", "YZ", "XZ"

    color : str or matplotlib color, default: "auto"
            optional list of colors (matplotlib compatible) to use for different substructures

    scale : float, default: 1
          symbol scaling. `scale`=1 means that mesh points are plotted according to their physical sizes in nm

    borders : float, default: 50
          additional space around plot in nm

    marker : str, default "s" (=squares)
          scatter symbols for plotting meshpoints. Convention of
          matplotlib's `scatter`

    lw : float, default 0.1
          line width around scatter symbols. Convention of matplotlib's `scatter`

    tit : str, default: ""
        title for plot (optional)

    colors_multimat : list, default: None
        optional list of colors (matplotlib compatible) to use for different materials

    legend : bool, default: True
        whether to add a legend if multi-material structure (requires auto-color enabled)

    ax : matplotlib `axes`, default: None (=create new)
           axes object (matplotlib) to plot into

    absscale : bool, default: False
          absolute or relative scaling. If True, override internal
          scaling calculation

    show : bool, default: True
          directly show plot

    Returns
    -------
    result returned by matplotlib's `scatter`

    """
    import pyvista as pv
    from torchgdm.simulation import SimulationBase, Simulation
    from torchgdm.struct.volume.pola import StructDiscretized3D
    from torchgdm.struct import StructEffPola3D

    if issubclass(type(struct), StructDiscretized3D):
        return _plot_structure_discretized(
            struct, color=colors[i_s], scale=scale, alpha=alpha, show=show, pl=pl, **kwargs
        )
    elif issubclass(type(struct), StructEffPola3D):
        return _plot_structure_eff_pola(
            struct, color=colors[i_s], scale=scale, alpha=alpha, show=show, pl=pl, **kwargs
        )
    elif issubclass(type(struct), Simulation) or issubclass(
        type(struct), SimulationBase
    ):
        # -- prep
        struct_list = struct.structures
        
        if type(show) == str:
            if show.lower() == "auto" and pl is None:
                show = True
            else:
                show = False

        if pl is None:
            pl = pv.Plotter()
        
        # -- colors for subsets with different materials
        if color == "fix":
            colors = COLORS_DEFAULT
        elif color == "auto":
            colors = ["auto"] * len(struct_list)
        else:
            colors = color

        # -- call all structure's plot functions
        for i_s, struct in enumerate(struct_list):
            struct.plot3d(color=colors[i_s], scale=scale, alpha=alpha, legend=legend, pl=pl, show=False)
        
        # -- finalize: config global plot
        if show:
            pl.show()
    
    else:
        raise ValueError("Unknown structure input")

        
