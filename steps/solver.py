# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# STEPS - STochastic Engine for Pathway Simulation
# Copyright (C) 2007-2009 Okinawa Institute of Science and Technology, Japan.
# Copyright (C) 2003-2006 University of Antwerp, Belgium.
#
# See the file AUTHORS for details.
#
# This file is part of STEPS.
#
# STEPS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# STEPS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#  Last Changed Rev:  $Rev$
#  Last Changed Date: $Date$
#  Last Changed By:   $Author$

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# This file is the user-interface file for all solver objects.
# All objects are directly derived from the corresponding swig objects.
# All objects are owned by Python.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
 
"""
Implementation of simulation solvers. 

Each solver is a partial or full implementation of the STEPS solver API.
At the moment STEPS implements three different solvers. 

The steps.solver.Wmrk4 class implements a well-mixed, deterministic solver 
based on the Runge–Kutta method. 

The steps.solver.Wmdirect class implements a stochastic, well-mixed solver 
based on Gillespie's Direct SSA Method. 

The steps.solver.Tetexact class implements a stochastic reaction-diffusion 
solver, based on Gillespie's Direct SSA Method extended for diffusive fluxes 
between tetrahedral elements in complex geometries.

"""
from . import steps_swig
import _steps_swig
import cPickle

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Well-mixed RK4
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Wmrk4(steps_swig.Wmrk4) :
    def __init__(self, model, geom, rng): 
        """
        Construction::
        
            sim = steps.solver.Wmrk4(model, geom, rng)
            
        Create a well-mixed RK4 simulation solver.
            
        Arguments: 
            * steps.model.Model model
            * steps.geom.Geom geom
            * steps.rng.RNG rng
        """
        this = _steps_swig.new_Wmrk4(model, geom, rng)
        try: self.this.append(this)
        except: self.this = this
        self.thisown = True
        self.cp_prefix = ""
        self.model = model
        self.geom = geom
        
    def setCheckPointPrefix(self, prefix):
        """
        Setup checkpointing file prefix including path.
        
        Arguments:
            string prefix path prefix for checkpoint files.
        """
        self.cp_prefix = prefix
        
    def run(self, end_time, cp_interval = 0.0):
        """
        Run the simulation until end_time, 
        automatically checkpoint at each cp_interval.
        """
        
        if cp_interval > 0:
            while _steps_swig.API_getTime(self) + cp_interval < end_time:
                _steps_swig.API_advance(self, cp_interval)
                filename = "%s%e.wmrk4_cp" % (self.cp_prefix, _steps_swig.API_getTime(self))
                print "Checkpointing -> ", filename
                _steps_swig.API_checkpoint(self, filename)
            _steps_swig.API_run(self, end_time)
            filename = "%s%e.wmrk4_cp" % (self.cp_prefix, _steps_swig.API_getTime(self))
            print "Checkpointing -> ", filename
            _steps_swig.API_checkpoint(self, filename)
        else:
            _steps_swig.API_run(self, end_time)
        
    def advance(self, advance_time, cp_interval = 0.0):
        """
        Advance the simulation for advance_time, 
        automatically checkpoint at each cp_interval.
        """
        
        end_time = _steps_swig.API_getTime(self) + advance_time
        if cp_interval > 0:
            while _steps_swig.API_getTime(self) + cp_interval < end_time:
                _steps_swig.API_advance(self, cp_interval)
                filename = "%s%e.wmrk4_cp" % (self.cp_prefix, _steps_swig.API_getTime(self))
                print "Checkpointing -> ", filename
                _steps_swig.API_checkpoint(self, filename)
            _steps_swig.API_run(self, end_time)
            filename = "%s%e.wmrk4_cp" % (self.cp_prefix, _steps_swig.API_getTime(self))
            print "Checkpointing -> ", filename
            _steps_swig.API_checkpoint(self, filename)
        else:
            _steps_swig.API_run(self, end_time)
            

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Well-mixed Direct SSA
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Wmdirect(steps_swig.Wmdirect) :
    def __init__(self, model, geom, rng): 
        """
        Construction::
        
            sim = steps.solver.Wmdirect(model, geom, rng)
            
        Create a well-mixed Direct SSA simulation solver.
            
        Arguments: 
            * steps.model.Model model
            * steps.geom.Geom geom
            * steps.rng.RNG rng
        """
        this = _steps_swig.new_Wmdirect(model, geom, rng)
        try: self.this.append(this)
        except: self.this = this
        self.thisown = True
        self.cp_prefix = ""
        self.model = model
        self.geom = geom

    def setCheckPointPrefix(self, prefix):
        """
        Setup checkpointing file prefix including path.
        
        Arguments:
            string prefix path prefix for checkpoint files.
        """
        self.cp_prefix = prefix
        
    def run(self, end_time, cp_interval = 0.0):
        """
        Run the simulation until end_time, 
        automatically checkpoint at each cp_interval.
        """
        
        if cp_interval > 0:
            while _steps_swig.API_getTime(self) + cp_interval < end_time:
                _steps_swig.API_advance(self, cp_interval)
                filename = "%s%e.wmrk4_cp" % (self.cp_prefix, _steps_swig.API_getTime(self))
                print "Checkpointing -> ", filename
                _steps_swig.API_checkpoint(self, filename)
            _steps_swig.API_run(self, end_time)
            filename = "%s%e.wmrk4_cp" % (self.cp_prefix, _steps_swig.API_getTime(self))
            print "Checkpointing -> ", filename
            _steps_swig.API_checkpoint(self, filename)
        else:
            _steps_swig.API_run(self, end_time)
        
    def advance(self, advance_time, cp_interval = 0.0):
        """
        Advance the simulation for advance_time, 
        automatically checkpoint at each cp_interval.
        """
        
        end_time = _steps_swig.API_getTime(self) + advance_time
        if cp_interval > 0:
            while _steps_swig.API_getTime(self) + cp_interval < end_time:
                _steps_swig.API_advance(self, cp_interval)
                filename = "%s%e.wmdirect_cp" % (self.cp_prefix, _steps_swig.API_getTime(self))
                print "Checkpointing -> ", filename
                _steps_swig.API_checkpoint(self, filename)
            _steps_swig.API_run(self, end_time)
            filename = "%s%e.wmdirect_cp" % (self.cp_prefix, _steps_swig.API_getTime(self))
            print "Checkpointing -> ", filename
            _steps_swig.API_checkpoint(self, filename)
        else:
            _steps_swig.API_run(self, end_time)
            
        
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Tetrahedral Direct SSA
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #        
class Tetexact(steps_swig.Tetexact) :  
    def __init__(self, model, geom, rng): 
        """
        Construction::
        
            sim = steps.solver.Tetexact(model, mesh, rng)
            
        Create a tetrahedral mesh-based Direct SSA simulation solver.
            
        Arguments: 
            * steps.model.Model model
            * steps.geom.Tetmesh mesh
            * steps.rng.RNG rng
        """
        
        this = _steps_swig.new_Tetexact(model, geom, rng)
        try: self.this.append(this)
        except: self.this = this
        self.thisown = True
        self.cp_prefix = ""
        self.model = model
        self.geom = geom
        
        
    def setCheckPointPrefix(self, prefix):
        """
        Setup checkpointing file prefix including path.
        
        Arguments:
            string prefix path prefix for checkpoint files.
        """
        self.cp_prefix = prefix
        
    def run(self, end_time, cp_interval = 0.0):
        """
        Run the simulation until end_time, automatic checkpoint for every cp_interval.
        """
        if cp_interval > 0.0:
            while (end_time - _steps_swig.API_getTime(self)) > cp_interval:
                _steps_swig.API_advance(self, cp_interval)
                self.checkpoint()
            _steps_swig.API_run(self, end_time)
            self.checkpoint()
        else:
            _steps_swig.API_run(self, end_time)
    
    def advance(self, advance_time, cp_interval = 0.0):
        """
        Avdance the simulation for advance_time, automatic checkpoint for every cp_interval.
        """
        if cp_interval > 0.0:
            remain = advance_time
            while remain > cp_interval:
                _steps_swig.API_advance(self, cp_interval)
                self.checkpoint()
                remain -= cp_interval
            _steps_swig.API_advance(self, remain)
            self.checkpoint()
        else:
            _steps_swig.API_advance(self, advance_time)        
    
    
    def getFile(self, name):
        if name == None:
            filename = "%s%e%s" % (self.cp_prefix, _steps_swig.API_getTime(self), ".checkpoint")
            print "\ncheckpointing -> ", filename
            output = file(filename, "wb")
        else:
            print "checkpointing -> ", name
            output = file(name, "wb")
        return output
        
    def checkpoint(self, filename = None):
        """
        Checkpoint state to filename.
        """
        output = self.getFile(filename)

        specs = self.model.getAllSpecs()
        ntets = self.geom.ntets
        ntris = self.geom.ntris
        
        # checkpoint general info
        info = {}
        info["Solver"] = "Tetexact"
        info["SimTime"] = _steps_swig.API_getTime(self)
        info["SimNSteps"] = _steps_swig.API_getNSteps(self)
        info["NTets"] = ntets
        info["NTris"] = ntris
        spec_ids = []
        for spec in specs:
            spec_ids.append(spec.id)
        info["Specs"] = spec_ids
        cPickle.dump(info,output)
        
        # checkpoint tet info
        for t in range(ntets):
            if self.geom.getTetComp(t) == None:
                continue
            scan = {}
            scan["DataType"] = "Tet"
            scan["DataID"] = t
            specs_dist = {}
            for spec in specs:
                spec_count = _steps_swig.API_getTetCount(self, t, spec.id)
                specs_dist[spec.id] = spec_count
            scan["SpecsDist"] = specs_dist
            cPickle.dump(scan, output)
        
        # checkpoint tri info    
        for t in range(ntris):
            if self.geom.getTriPatch(t) == None:
                continue
            scan = {}
            scan["DataType"] = "Tri"
            scan["DataID"] = t
            specs_dist = {}
            for spec in specs:
                spec_count = _steps_swig.API_getTriCount(self, t, spec.id)
                specs_dist[spec.id] = spec_count
            scan["SpecsDist"] = specs_dist
            cPickle.dump(scan, output)
            
        print "Done."
        
    def restore(self, file):
        """
        Restore simulation state from checkpoint file
        """
        input = open(file, 'rb')
        if input == None:
            print "Unable to load checkpoint file."
            return
        
        print "\nRestoring data from %s:" %(file)
        print "Checking general info..."
        info = cPickle.load(input)
        if info["Solver"] != "Tetexact":
            print "Solver mismatch: this checkpoint file requires a %s solver." % (info["Solver"])
            return
        if info["NTets"] != self.geom.ntets:
            print "Tet number mismatch: %i (file) -- % i (mesh)." (info["NTets"], self.geom.ntets)
            return
        if info["NTris"] != self.geom.ntris:
            print "Tri number mismatch: %i (file) -- % i (mesh)." (info["NTris"], self.geom.ntris)
            return
        model_specs = self.model.getAllSpecs()
        model_spec_ids = []
        for spec in model_specs:
            model_spec_ids.append(spec.id)
        
        spec_diff = set(info["Specs"]) ^ set(model_spec_ids)
        if len(spec_diff) != 0:
            print "Model mismatch:"
            print "Species in file:"
            print info["Specs"]
            print "Species in model:"
            print model_spec_ids
            return
            
        print "Solver: %s, Sim Time: %e, Sim Steps: %i\nNTets: %i, NTris: %i" % (info["Solver"], info["SimTime"],
            info["SimNSteps"], info["NTets"], info["NTris"])
        
        print "\nSpecies:"
        print info["Specs"]
        
        _steps_swig.API_setTime(self, info["SimTime"])
        _steps_swig.API_setNSteps(self, info["SimNSteps"])
        
        print "\nRestoring Data..."
        while(True):
            try:
                data = cPickle.load(input)
                if data["DataType"] == "Tet":
                    t = data["DataID"]
                    specs_dist = data["SpecsDist"]
                    for spec in specs_dist.keys():
                        _steps_swig.API_setTetCount(self, t, spec, specs_dist[spec])
                elif data["DataType"] == "Tri":
                    t = data["DataID"]
                    specs_dist = data["SpecsDist"]
                    for spec in specs_dist.keys():
                        _steps_swig.API_setTriCount(self, t, spec, specs_dist[spec])
            except EOFError:
                break
        
        print "Done.\n"
        