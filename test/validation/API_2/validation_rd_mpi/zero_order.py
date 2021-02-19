########################################################################

# Stochastic degradation-diffusion process.

# AIMS: to verify if zero order reactions are inserted correctly to the SSA
# after bugfix https://github.com/CNS-OIST/HBP_STEPS/pull/146
# Note: 
# 1. This is not validated against analytical result, but 
# only check if the zero order reaction can be found through SSA search.
# Future improvement is needed.
# 2. sim.reset() should be avoided in this test
  
########################################################################

import steps.interface

from steps.model import *
from steps.geom import *
from steps.rng import *
from steps.sim import *

import math
import time

########################################################################

def get_model():
    mdl = Model()
    r = ReactionManager()
    with mdl:
        SA = Species.Create()
        volsys = VolumeSystem.Create()
        with volsys:
            None >r['R1']> SA
            r['R1'].K = 0.001
    return mdl

def get_geom():
    if __name__== "__main__":
        mesh_loc = "meshes/1x1x1.inp"
    else:
        mesh_loc = "validation_rd/meshes/1x1x1.inp"
    mesh = TetMesh.LoadAbaqus(mesh_loc, scale=1e-06)
    with mesh:
        comp = Compartment.Create(mesh.tets, 'volsys')
    return mesh

def get_solver(mdl, geom):
    r = RNG('r123', 1000, 1234)
    part = LinearMeshPartition(geom, MPI.nhosts, 1, 1)
    solver = Simulation('TetOpSplit', mdl, geom, r, MPI.EF_NONE, part)
    return solver

def validate(sim):
    sim.newRun()
    sim.run(1)
    count = sim.comp.SA.Count
    assert(count > 0)
    if __name__== "__main__" and MPI.rank == 0:
        print("Count: ", count)

def test_zeroorder_TetOpSplit():
    "Zero order reaction (TetOpSplit)"
    if __name__== "__main__" and MPI.rank == 0:
        print("Zero order reaction (TetOpSplit)")
    mdl = get_model()
    geom = get_geom()
    sim = get_solver(mdl, geom)
    validate(sim)

if __name__== "__main__":
  test_zeroorder_TetOpSplit()
