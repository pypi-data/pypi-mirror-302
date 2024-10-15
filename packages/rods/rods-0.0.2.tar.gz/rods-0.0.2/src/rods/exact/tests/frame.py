import os
import sys

cwd = os.getcwd()
folder = os.path.basename(cwd)
while folder != "beam":
    cwd = os.path.dirname(cwd)
    folder = os.path.basename(cwd)
    if len(cwd) == 0:
        print("Root directory was not found. Try inserting the path manually with 'sys.path.insert(0, absolute_path_to_root)'")
        sys.exit()
print("Root directory:", cwd)
sys.path.insert(0, cwd)

import functools
import numpy as np
#from system import StaticAnalysis
from domain import StaticAnalysis
import mesh
import postprocessing as postproc


def Frame():
    """
    In this example, a right angle frame is bent by an out-of-plane force.
    """

    mat = {
        'area':              1000.0,
        'elastic_modulus':   1000.0,
        'shear_modulus':     1000.0,
        'inertia_primary':   1.0,
        'inertia_secondary': 1.0,
        'inertia_torsion':   1.0,
#       'density':           10.0,
    }

    points = np.array([[0.,  0., 10.],
                       [0.,  0.,  0.],
                       [0., 10., 10.]])

    nodes, elements = mesh.n_point_mesh(
            points, n_elements=[1,1], order=2, material=mat, reference_vector=(0,1,1)
    )

    # hard-code Arho for this specific example
    # for ele in elements:
    #     ele.prop.Arho = 1.0

    system = StaticAnalysis(nodes, elements)
    system.time_step = 0.25
    system.final_time = 1.0
#   system.solver_type = 'dynamic'
#   system.max_number_of_time_steps = 250

    long, tran, vert = range(3)
    sect, elev, plan = range(3,6)
    def user_force_load(self):
        n_nodes = self.get_number_of_nodes()
        Q = np.zeros((6, n_nodes))
        if self.current_time <= 1:
#           Q[tran,-1] = 50 * self.current_time
#           Q[2,2] = 50 * self.current_time
#           Q[elev,-1] = 50 * self.current_time
            Q[tran,-1] = 50 * self.current_time
#           Q[tran,-2] =-20 * self.current_time
#       elif 1 < self.current_time and self.current_time < 2:
#           Q[1,2] = 50 - 50 * (self.current_time - 1)
        return Q

    system.degrees_of_freedom[-1][:6,0] = False  # [current time, dof 0 through 5, node 0]
    system.force_load = functools.partial(user_force_load, system)

    return system

def main():
    frame = Frame()
    frame.solve()
    ax = None

    ax = postproc.line_plot(frame, (-2,12), (-7,7), (-2,12), 0, ax=ax, label=True, no_show=True)
    for i in range(1,len(frame.time)):
        ax = postproc.line_plot(frame, (-2,12), (-7,7), (-2,12), i, ax=ax, no_show=True)
    postproc.plt.show()

if __name__ == "__main__":
    main()

