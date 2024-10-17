# encoding=utf-8
# %%
import unittest

import torch

import torchgdm as tg


class TestGlobalScalingInvariance(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing global scaling invariance...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        self.scale_factors = [1.0, 1.5]

        # --- setup a test case
        # - materials
        self.mat_struct = tg.materials.MatConstant(eps=16)
        self.mat_env = tg.materials.MatConstant(eps=1.33)
        # - environment
        self.env = tg.env.freespace_3d.EnvHomogeneous3D(
            env_material=self.mat_env
        )

        # - illumination field(s)
        self.plane_wave = tg.env.freespace_3d.PlaneWave(e0p=0.7, e0s=-0.5)

    def test_calculate_E_H(self):
        for device in self.devices:
            Q_sc = []
            Q_ex = []
            for scale in self.scale_factors:

                # scale wavelengths
                wavelengths = torch.linspace(550.0, 750.0, 3) * scale

                # scale geometry
                step = 20 * scale
                structure = tg.struct.StructDiscretizedCubic3D(
                    tg.struct.volume.cube(l=150 * scale / step), step, self.mat_struct
                )
                cs_geo = tg.tools.geometry.get_geometric_cross_section(structure)

                # - define and run simulation
                sim = tg.Simulation(
                    structures=[structure],
                    illumination_fields=[self.plane_wave],
                    environment=self.env,
                    wavelengths=wavelengths,
                    device=device,
                )
                sim.run(verbose=False, progress_bar=False)
                cs_results = tg.tools.batch.calc_spectrum(
                    sim, tg.postproc.crosssect.total, progress_bar=False
                )
                Q_sc.append(cs_results["scs"] / cs_geo)
                Q_ex.append(cs_results["ecs"] / cs_geo)

            torch.testing.assert_close(Q_sc[0], Q_sc[1], rtol=1e-3, atol=0.01)
            torch.testing.assert_close(Q_ex[0], Q_ex[1], rtol=1e-3, atol=0.01)
            if self.verbose:
                print("  - {}: scaling test passed.".format(device))


# %%
if __name__ == "__main__":
    print("testing global scaling invariance...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
