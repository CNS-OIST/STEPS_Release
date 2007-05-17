# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# STEPS - STochastic Engine for Pathway Simulation
# Copyright (C) 2005-2007 Stefan Wils. All rights reserved.
#
# $Id$
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


"""
Note:

We've currently decided to implement a lot of functionality in these Python
classes, because we believe that during real simulations (as opposed to
simple toy problem test cases) the bulk of time is spent in the computational
routines. The efficiency overhead generated by implementing so much in Python 
functions should therefore be small.

If it would turn out to be a real problem, we can use for instance template
programming to 'offshore' the fancy code in C++.
"""


import steps.error as serr


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class FuncCore(object):
    
    """This class implements the core functionality of a solver module.
    """
    
    
    def _rsf(self, funcname):
        """Resolve a function, specified by funcname, in the solver module.
        
        Returns:
            A pointer to the function.
        
        Raises:
            steps.error.SolverInterfaceError    
                If the function name cannot be resolved.
        """
        f = self._solver_module.__dict__.get(funcname)
        if f == None:
            raise serr.SolverCoreError, \
                'Function \'%s\' not available in solver \'%s\'' \
                % (funcname, self._solver_module.__name__)
        return f
    
    
    def __init__(self, solver_module, model, geom, rng):
        """Initialize class FuncCore.
        
        Arguments:
            solver_module
                A reference to the actual solver module (usually a SWIG
                generated module with the name ending in '_core'.
            model
                A valid steps.model.Model object, describing the kinetic
                properties of the simulation.
            geom
                A valid steps.geom.Geom object (or one of its derived
                objects), describing the geometry of the simulation.
            rng
                A steps.rng.RNG object. We decided to include this in 
                the core functionality, because even deterministic 
                solvers might need random numbers for some tasks.
            
        Raises:
            steps.error.SolverInterfaceError
                If something went wrong with communicating with the solver 
                core interface.
        """
        
        # Copy a refence to the solver core module.
        self._solver_module = solver_module
        
        # Resolve core module functions of the solver interface.
        #
        # TODO: maybe there's a less type-intensive way of doing this...
        # On the other hand, this code should not change too often, so
        # maybe it's not worth investing time in making this more 
        # sophisticated.
        self._siGetSolverName = self._rsf('siGetSolverName')
        self._siGetSolverDesc = self._rsf('siGetSolverDesc')
        self._siGetSolverAuthors = self._rsf('siGetSolverAuthors')
        self._siGetSolverEmail = self._rsf('siGetSolverEmail')
        self._siNewState = self._rsf('siNewState')
        self._siDelState = self._rsf('siDelState')
        self._siBeginStateDef = self._rsf('siBeginStateDef')
        self._siEndStateDef = self._rsf('siEndStateDef')
        self._siSetRNG = self._rsf('siSetRNG')
        self._siBeginVarDef = self._rsf('siBeginVarDef')
        self._siEndVarDef = self._rsf('siEndVarDef')
        self._siNewSpec = self._rsf('siNewSpec')
        self._siBeginReacDef = self._rsf('siBeginReacDef')
        self._siEndReacDef = self._rsf('siEndReacDef')
        self._siNewReac = self._rsf('siNewReac')
        self._siAddReacLHS = self._rsf('siAddReacLHS')
        self._siAddReacRHS = self._rsf('siAddReacRHS')
        self._siBeginCompDef = self._rsf('siBeginCompDef')
        self._siEndCompDef = self._rsf('siEndCompDef')
        self._siNewComp = self._rsf('siNewComp')
        self._siAddCompSpec = self._rsf('siAddCompSpec')
        self._siAddCompReac = self._rsf('siAddCompReac')
        self._siReset = self._rsf('siReset')
        self._siRun = self._rsf('siRun')
        self._siGetTime = self._rsf('siGetTime')
        self._siGetCompVol = self._rsf('siGetCompVol')
        self._siSetCompVol = self._rsf('siSetCompVol')
        self._siGetCompCount = self._rsf('siGetCompCount')
        self._siSetCompCount = self._rsf('siSetCompCount')
        self._siGetCompMass = self._rsf('siGetCompMass')
        self._siSetCompMass = self._rsf('siSetCompMass')
        self._siGetCompConc = self._rsf('siGetCompConc')
        self._siSetCompConc = self._rsf('siSetCompConc')
        self._siGetCompClamped = self._rsf('siGetCompClamped')
        self._siSetCompClamped = self._rsf('siSetCompClamped')
        self._siGetCompReacK = self._rsf('siGetCompReacK')
        self._siSetCompReacK = self._rsf('siSetCompReacK')
        self._siGetCompReacActive = self._rsf('siGetCompReacActive')
        self._siSetCompReacActive = self._rsf('siSetCompReacActive')

        # Now, attempt to create a state.
        self._state = self._siNewState()
        self._siSetRNG(self._state, rng)
        
        # Setup phase. Pass the model and geometric structure to the
        # the simulator, allow it to define a state.
        # TODO: re-organize this w.r.t. child class
        self._siBeginStateDef(self._state)
        
        # Setup species. 
        self._lut_specs = { }
        self._lut_specnames = { }
        self._setupVars(model)
        
        # Initialize: declare all reactions. 
        self._lut_reacs = { }
        self._lut_reacnames = { }
        self._setupReacs(model)
        
        # Initialize: declare all compartments.
        self._lut_comps = { }
        self._lut_compnames = { }
        self._setupComps(model, geom)
        
        # Finish the state definition, create actual state(?)
        # Get ready for simulation.
        # TODO: again, reorganize (think about mesh and stuff)
        self._siEndStateDef(self._state)
    
    
    def __del__(self):
        self._siDelState(self._state)
        self._state = None

    
    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    
    
    def _spec(self, spec):
        """Resolve a user-specified reference to a species into its 
        global index.
        
        This global index can be used for communicating with the solver 
        core. The method should not typically be called by users.
        
        However, because it's almost always called to work on a 
        user-specified value, it will still raise an ArgumentError 
        rather than a ProgramError when the species cannot be found.
        
        Arguments:
            spec
                A reference to the species: the global index or its name.
        
        Returns:
            The global index of the species.
            
        Raises:
            steps.error.ArgumentError
                The species cannot be resolved.
        """
        if isinstance(spec, basestring):
            spec = self._lut_specs[spec]
        if spec == None:
            raise serr.ArgumentError, 'Cannot find species.'
        return spec


    def _specName(self, spec_gidx):
        """Return the name of some species, given its global index.
        
        Raises:
            steps.error.ProgramError
                When the global index does not exist.
        """
        specname = self._lut_specnames[spec_gidx]
        if specname == None:
            raise serr.ProgramError, \
                'Cannot find species with gidx %d.' % spec_gidx
        return specname
        

    def _reac(self, reac):
        """Resolve a user-specified reference to a reaction into its 
        global index.
        
        This global index can be used for communicating with the solver 
        core. The method should not typically be called by users.
        
        However, because it's almost always called to work on a 
        user-specified value, it will still raise an ArgumentError 
        rather than a ProgramError when the reaction cannot be found.
        
        Arguments:
            spec
                A reference to the reaction: the global index or its name.
        
        Returns:
            The global index of the reaction.
            
        Raises:
            steps.error.ArgumentError
                The reaction cannot be resolved.
        """
        if isinstance(reac, basestring):
            reac = self._lut_reacs[reac]
        if reac == None:
            raise serr.ArgumentError, 'Cannot find reaction.'
        return reac


    def _reacName(self, reac_gidx):
        """Return the name of some reaction channel, given its global index.
        
        Raises:
            steps.error.ProgramError
                When the global index does not exist.
        """
        reacname = self._lut_reacnames[reac_gidx]
        if reacname == None:
            raise serr.ProgramError, \
                'Cannot find reaction with gidx %d.' % reac_gidx
        return reacname
        

    def _comp(self, comp):
        """Resolve a user-specified reference to a compartment into its 
        global index.
        
        This global index can be used for communicating with the solver 
        core. The method should not typically be called by users.
        
        However, because it's almost always called to work on a 
        user-specified value, it will still raise an ArgumentError 
        rather than a ProgramError when the compartment cannot be found.
        
        Arguments:
            spec
                A reference to the compartment: the global index or its name.
        
        Returns:
            The global index of the compartment.
        
        Raises:
            steps.error.ArgumentError
                The compartment cannot be resolved.
        """
        if isinstance(comp, basestring):
            comp = self._lut_comps[comp]
        if comp == None:
            raise serr.ArgumentError, 'Cannot find compartment.'
        return comp
        
    
    def _compName(self, comp_gidx):
        """Return the name of some compartment, given its global index.
        
        Raises:
            steps.error.ProgramError
                When the global index does not exist.
        """
        compname = self._lut_compnames[comp_gidx]
        if compname == None:
            raise serr.ProgramError, \
                'Cannot find compartment with gidx %d.' % comp_gidx
        return compname
    
    
    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    
    
    def _setupVars(self, model):
        """Add all field variables defined in the model to solver state.
        
        Raises:
            steps.error.SolverCoreError
                When the solver core module does something wrong.
        """
        self._siBeginVarDef(self._state)
        for s in model.getAllSpecies():
            sid = s.id
            sidx = self._siNewSpec(self._state, sid)
            if self._lut_specnames.has_key(sidx):
                raise serr.SolverCoreError, \
                    'When adding species \'%s\', solver ' + \
                    '\'%s\' returned global index %d, which is already ' + \
                    'used by species \'%s\'.' \
                    % ( sid, self.solvername, sidx, self._lut_specnames[sidx] )
            self._lut_specs[sid] = sidx
            self._lut_specnames[sidx] = sid
        self._siEndVarDef(self._state)
	
    
    def _setupReacs(self, model):
        """Add all reactions defined in the model to solver state.
        
        Raises:
            steps.error.SolverCoreError
                When the solver core module does something stoopid.
        """
        self._siBeginReacDef(self._state)
        for vsys in model.getAllVolsys():
            for reac in vsys.getAllReactions():
                # First, declare the reaction channel itself.
                rid = reac.id
                ridx = self._siNewReac(self._state, rid)
                if self._lut_reacnames.has_key(ridx):
                    raise serr.SolverCoreError, \
                        'When adding reaction \'%s\', solver ' + \
                        'module \'%s\' returned global index %d, which ' + \
                        'is already used by reaction \'%s\'.' \
                        % ( rid, self.solvername, \
                        ridx, self._lut_reacnames[ridx] )
                self._lut_reacs[rid] = ridx
                self._lut_reacnames[ridx] = rid
                
                # Then copy the stochiometry.
                for lhs in reac.lhs:
                    self._siAddReacLHS(self._state, \
                        ridx, self._spec(lhs.id))
                for rhs in reac.rhs:
                    self._siAddReacRHS(self._state, \
                        ridx, self._spec(rhs.id))
        self._siEndReacDef(self._state)
    
    
    def _setupComps(self, model, geom):
        """Add all compartments defined in the geometry to the solver 
        state. All volsys references in the compartments are resolved,
        by looking them up in the model.
        
        Arguments:
            model
                A valid steps.model.Model object.
            geom
                A valid steps.geom.Geom object; any reference to volume
                systems made in the geom object must be resolvable in
                the steps.model.Model object.
        
        Raises:
            steps.error.SolverCoreError
                When the solver core module does something wrong.
        """
        self._siBeginCompDef(self._state)
        for c in geom.getAllComps():
            # First, declare the compartment itself.
            cid = c.id
            cidx = self._siNewComp(self._state, cid)
            if self._lut_compnames.has_key(cidx):
                raise serr.SolverCoreError, \
                    'When adding compartment \'%s\', solver ' + \
                    '\'%s\' returned global index %d, which is already ' + \
                    'used by compartment \'%s\'.' \
                    % ( cid, self.solvername, cidx, self._lut_compnames[cidx] )
            self._lut_comps[cid] = cidx
            self._lut_compnames[cidx] = cid
                    
            # Loop over all volume systems, and resolve them.
            for vsys in c.volsys:
                # Find the Volsys object with the given name.
                vsys = model.getVolsys(vsys)
                for spec in vsys.getAllSpecies():
                    self._siAddCompSpec(self._state, \
                        cidx, self._spec(spec.id))
                for reac in vsys.getAllReactions():
                    self._siAddCompReac(self._state, \
                        cidx, self._reac(reac.id))
        self._siEndCompDef(self._state)
    
    
    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

    
    def getSolverName(self):
        """Return the name of the solver, as specified in the core module.
        """
        return self._siGetSolverName()
    
    solvername = property(getSolverName)
    
    
    def getSolverDesc(self):
        """Return a short description of the solver, as specified in the
        core module.
        """
        return self._siGetSolverDesc()
    
    solverdesc = property(getSolverDesc)
    
    
    def getSolverAuthors(self):
        """Return the authors of the solver, as specified in the core module.
        """
        return self._siGetSolverAuthors()
    
    solverauthors = property(getSolverAuthors)
    
    
    def getSolverEmail(self):
        """Return an email address at which the solver authors can be
        contacted. Specified in the core module.
        """
        return self._siGetSolverEmail()
    
    solveremail = property(getSolverEmail)
    

	#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #


    def reset(self):
        """Reset the simulation state.
        
        All state variables are set to their default initial values. Time 
        is set to zero. This method should be called prior to a new 
        simulation run, or to clean up from a prior simulation.
        
        This method should never fail.
        """
        self._siReset(self._state)
		

    def run(self, endtime):
        """Forward the simulation until the specified time is reached.
        
        When this time has been reached, the simulation is interrupted
        and control returns to the caller.
        
        Raises:
            steps.error.ArgumentError
                When the specified endtime is smaller than the current time.
        """
        curtime = self.getTime()
        if (endtime < curtime):
            raise serr.ArgumentError, \
                'Cannot run to %f (< current time %f)' \
                % (endtime, curtime)
        if (endtime == curtime):
            return
        self._siRun(self._state, endtime)
        assert endtime == self.getTime(), \
            'Simulation stopped at %f, instead of %f' \
            % (self.getTime(), endtime)


	#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #


    def getTime(self):
        """Return the current simulation time.
        """
        return self._siGetTime(self._state)

    time = property(getTime)

		
	#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
	
    
    def getCompVol(self, comp):
        """Return the volume of a compartment (in m^3).
        
        Arguments:
            comp
                The compartment, identified by name or global index.
        """
        comp = self._comp(comp)
        vol = self._siGetCompVol(self._state, comp)
        assert vol >= 0.0, 'Volume of \'%s\' is negative (%f).' \
            % ( self._compName(comp), vol)
        return vol
    
    
    def setCompVol(self, comp, vol):
        """Set the volume of a compartment.
        
        Note: this function might not work in each solver, for instance when 
        using a mesh-based solver. That is why maybe it should be moved to 
        another set of functionality (e.g. 'func_wm').
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            vol
                The volume (in m^3).
        
        Raises:
            steps.error.ArgumentError
                When a negative volume was specified.
        """
        if vol < 0.0:
            raise serr.ArgumentError, \
                'Cannot set negative volume (%f).' % vol
        self._siSetCompVol(self._state, self._comp(comp), vol)
    
    
    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    
    
    def getCompCount(self, comp, spec):
        """Count the number of molecules of some species in a compartment.
        
        Note: when used in the context of a mesh-based simulation, the
        total amount is computed as the sum of the amount in all voxels of
        the compartment.
        
        Argument:
            comp
                The compartment, identified by name or global index.
            spec
                The species, identified by name or global index.
        """
        comp = self._comp(comp)
        spec = self._spec(spec)
        c = self._siGetCompCount(self._state, comp, spec)
        assert c >= 0, \
            'Count of \'%s\' in \'%s\' is negative (%d).' \
            % ( self._specName(spec), self._compName(comp), c )
        return c
    
    
    def setCompCount(self, comp, spec, num):
        """Set the number of molecules of some species in a compartment.
        
        Note: when used in the context of a mesh-based simulation, the 
        molecular count is equally divided over all voxels in the 
        compartment (i.e., it will results in a uniform distribution 
        throughout the compartment).
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            spec
                The species, identified by name or global index.
            num
                The number of species. Should be a positive integer,
                but gets rounded when a floating point number was
                specified.
        
        Raises:
            steps.error.ArgumentError
                When a negative number was specified.
        """
        if num < 0:
            raise serr.ArgumentError, \
                'Specified amount is negative (%d).' % num
        self._siSetCompCount(self._state, \
            self._comp(comp), self._spec(spec), num)


    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #


    def getCompMass(self, comp, spec):
        """Return the mass of some species in a compartment (in mole).
        
        Note: when used in the context of a mesh-based simulation, the
        total mass is computed as the sum of the mass in all voxels of
        the compartment.
        
        Argument:
            comp
                The compartment, identified by name or global index.
            spec
                The species, identified by name or global index.
        """
        comp = self._comp(comp)
        spec = self._spec(spec)
        m = self._siGetCompMass(self._state, comp, spec)
        assert m >= 0.0, \
            'Mass of \'%s\' in \'%s\' is negative (%f).' \
            % ( self._specName(spec), self._compName(comp), m )
        return m
        
    
    def setCompMass(self, comp, spec, mass):
        """Set the mass of some species in a compartment (in mole).
        
        Note: when used in the context of a mesh-based simulation, the 
        total mass is equally divided over all voxels in the compartment
        (i.e., it will results in a uniform distribution throughout the 
        compartment).
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            spec
                The species, identified by name or global index.
            mass
                The mass, specified in moles.
        
        Raises:
            steps.error.ArgumentError
                When a negative mass was specified.
        """
        if mass < 0.0:
            raise serr.ArgumentError, \
                'Specified mass is negative (%f).' % mass
        self._siSetCompMass(self._state, \
            self._comp(comp), self._spec(spec), mass)
    

    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    

    def getCompConc(self, comp, spec):
        """Return the concentration of some species in a compartment 
        (in Molar units).
        
        Note: when used in the context of a mesh-based simulation,
        the overall concentration in a compartment is computed by
        by taking the volume-weighted sum of the concentration in 
        all voxels of the compartment.
        
        Argument:
            comp
                The compartment, identified by name or global index.
            spec
                The species, identified by name or global index.
        """
        comp = self._comp(comp)
        spec = self._spec(spec)
        c = self._siGetCompConc(self._state, conc, spec)
        assert c >= 0.0, \
            'Concentration of \'%s\' in \'%s\' is negative (%f).' \
            % ( self._specName(spec), self._compName(comp), c )
        return c
        
    
    def setCompConc(self, comp, spec, conc):
        """Set the concentration of some species in a compartment 
        (in Molar units).
        
        Note: when used in the context of a mesh-based simulation, 
        this function changes the concentration to the same value
        in all voxels of the compartment.
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            spec
                The species, identified by name or global index.
            mass
                The concentration, in molar units.
        
        Raises:
            steps.error.ArgumentError
                When a negative concentration was specified.
        """
        if conc < 0.0:
            raise serr.ArgumentError, \
                'Specified concentration is negative (%f)' % conc
        self._siSetCompConc(self._state, \
            self._comp(comp), self._spec(spec), conc)
    

    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    

    def getCompClamped(self, comp, spec):
        """Return whether the concentration of a species in a compartment
        remains constant over time (unless changed explicitly).
        
        Note: when used in the context of a mesh-based simulation, this 
        function will return True only when the species has been clamped 
        in all voxels of the compartment.
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            spec
                The species, identified by name or global index.
        """
        return self._siGetCompClamped(self._state, \
            self._comp(comp), self._spec(spec))
    
    
    def setCompClamped(self, comp, spec, clamp):
        """Turn clamping for a species in a compartment on or off.
        
        Note: when used in the context of a mesh-based simulation, this 
        function will turn on/off clamping in all voxels of the 
        compartment.
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            spec
                The species, identified by name or global index.
            clamp
                A boolean value (True if clamped; False otherwise).
        """
        self._siGetCompClamped(self._state, \
            self._comp(comp), self._spec(spec), clamp)


    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #


    def getCompReacK(self, comp, reac):
        """Return the macroscopic reaction constant of a reaction in a 
        compartment.
        
        Note: when used in the context of a mesh-based simulation, the 
        value is computed as the volume-weighted sum of the reaction 
        constants in all voxels of the compartment.
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            reac
                The reaction, identified by name or global index.
        """
        comp = self._comp(comp)
        reac = self._reac(reac)
        k = self._siGetCompReacK(self._state, comp, reac)
        assert k >= 0.0, \
            'Macroscopic constant of \'%s\' in \'%s\' is negative (%d).' \
            % ( self._reacName(reac), self._compName(comp), k )
        return k


    def setCompReacK(self, comp, reac, k):
        """Set the macroscopic reaction constant of a reaction in a 
        compartment (its units vary on the order of the reaction).
        
        Note: when used in the context of a mesh-based simulation, this
        function changes the reaction constant equally in all voxels of the 
        compartment.
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            reac
                The reaction, identified by name or global index.
            k
                The macroscopic reaction constant.
                
        Raises:
            steps.error.ArgumentError
                When a negative constant was specified.
        """
        if k < 0.0:
            raise serr.ArgumentError, \
                'Macroscopic reaction constant is negative (%f)' % k
        self._siSetCompReacK(self._state, \
            self._comp(comp), self._reac(reac), k)

    
    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    
    
    def getCompReacActive(self, comp, reac):
        """Return whether a reaction in some compartment has been
        activated or not.
        
        Depending on how sophisticated the solver implementation is, 
        inactivating a reaction channel might be more efficient than 
        setting its reaction constant to zero.
        
        Note: when used in the context of a mesh-based solver, this 
        function returns False only when the reaction has been inactivated 
        in all voxels. It returns True otherwise.
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            reac
                The reaction, identified by name or global index.
        """
        return self._siGetCompReacActive(self._state, \
            self._comp(comp), self._reac(reac))
    
    
    def setCompReacActive(self, comp, reac, act):
        """Activate/inactivate a reaction channel in some compartment.
        
        Depending on how sophisticated the solver implementation is, 
        inactivating a reaction channel might be more efficient than 
        setting its reaction constant to zero.
        
        Note: when used in the context of a mesh-based solver, 
        activation/inactivation of some reaction turns it on/off in 
        all voxels at the same time.
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            reac
                The reaction, identified by name or global index.
            act
                A boolean value (True = activated; False = inactivated).
        """
        self._siSetCompReacActive(self._state, \
            self._comp(comp), self._reac(reac), act)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class FuncSSA(FuncCore):


    """Implements simulation functions that are available when using 
    a Gillespie-style solver. 
    
    These solvers track discrete events, meaning that one time step 
    of the simulation corresponds to e.g. one single reaction taking 
    place somewhere. 
    
    With the functions defined in this class, it is possible to advance
    a simulation one event at a time. One can also get access to the 
    propensity values and the extents of each reaction channel.
    """


    def __init__(self):
        # Resolve SSA-specific functionality in the solver module interface.
        self._siStep = self._rsf('siStep')
        self._siGetNSteps = self._rsf('siGetNSteps')
        self._siGetA0 = self._rsf('siGetA0')
        self._siGetCompReacC = self._rsf('siGetCompReacC')
        self._siGetCompReacH = self._rsf('siGetCompReacH')
        self._siGetCompReacA = self._rsf('siGetCompReacA')
        self._siGetCompReacExtent = self._rsf('siGetCompReacExtent')
        self._siResetCompReacExtent = self._rsf('siResetCompReacExtent')


    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #


    def step(self):
        """Advance the simulation by one time step (one discrete event).
        
        In many cases it's not a good idea to do this, because advancing 
        a simulation step by step can substantially increase the relative 
        amount of overhead caused by coming back to the Python script.
        
        Returns:
            The current time of the simulation.
        """
        return self._siStep(self._state)


    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #


    def getNSteps(self):
        """Return the number of steps the simulation has advanced.
        
        The number of steps is reset to zero when reset() is called. 
        
        A machine word is typically used to store the number of steps,
        so this value might wrap around to zero for extremely long
        simulations.
        """
        n = self._siGetNSteps(self._state)
        assert n >= 0, \
            'Number of steps is negative (%d)' % n
        return n

    nsteps = property(getNSteps)
    
    
    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    
    
    def getA0(self):
        """Return the zero propensity of the current simulation state.
        
        The zero propensity is defined as the sum of the propensity
        values of all individual events. It denotes the probability,
        per unit time, that *something* is going to happen.
        """
        a0 = self._siGetA0(self._state)
        assert a0 >= 0.0, \
            'Zero propensity is negative (%f).' % a0
        return a0
        
    a0 = property(getA0)
    
    
    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    
    
    def getCompReacC(self, comp, reac):
        """Return c_mu, the mesoscopic reaction constant of a reaction  
        in a compartment.
        
        The mesoscopic constant differs from the macroscopic in that it
        has been scaled to deal with discrete numbers of molecules.
        
        Note: when called in the context of a mesh-based simulation, the
        mesoscopic reaction constant is computed as the sum of the
        mesoscopic constants in all voxels of the compartment.
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            reac
                The reaction, identified by name or global index.
        """
        comp = self._comp(comp)
        reac = self._reac(reac)
        c = self._siGetCompReacC(self._state, comp, reac)
        assert c >= 0.0, \
            'c_mu is negative (%f).' % c
        return c
    
    
    def getCompReacH(self, comp, reac):
        """Compute h_mu, the distinct number of ways in which a reaction 
        can occur in a compartment, by computing the product of its 
        reactants.
        
        Note: when used in the context of a mesh-based simulation, it 
        returns the sum of the h_mu's over all voxels of the compartment. 
        This can become a very large value.
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            reac
                The reaction, identified by name or global index.
        """
        comp = self._comp(comp)
        reac = self._reac(reac)
        h = self._siGetCompReacH(self._state, comp, reac)
        assert h >= 0, \
            'h_mu is negative (%d).' % h
        return h
    
    
    def getCompReacA(self, comp, reac):
        """Return the propensity a_mu of a reaction in a compartment.
        
        The propensity value gives the probability per unit of time that 
        this reaction will occur, given the current local state.
        
        Note: when called in the context of a mesh-based simulation,
        a_mu is computed as the sum of the a_mu in all voxels of the
        compartment.
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            reac
                The reaction, identified by name or global index.
        """
        comp = self._comp(comp)
        reac = self._reac(reac)
        a = self._siGetCompReacA(self._state, comp, reac)
        assert a >= 0, \
            'Propensity is negative (%f).' % a
        return a
    
    
    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    
    
    def getCompReacExtent(self, comp, reac):
        """Return the extent of a reaction in a compartment.
        
        Note: when used with a mesh-based solver, it returns the sum of
        the reaction extents in all voxels of the compartment.
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            reac
                The reaction, identified by name or global index.
        """
        comp = self._comp(comp)
        reac = self._reac(reac)
        n = self._siGetCompReacExtent(self._state, comp, reac)
        assert n >= 0, \
            'Extent is negative (%d).' % n
        return n
    
    
    def resetCompReacExtent(self, comp, reac):
        """Reset the extent of a reaction in a compartment to zero.
        
        Note: when used with a mesh-based solver, it resets the extents
        of the reaction in all voxels of the compartment.
        
        Arguments:
            comp
                The compartment, identified by name or global index.
            reac
                The reaction, identified by name or global index.
        """
        self._siResetCompReacExtent(self._state, \
            self._comp(comp), self._reac(reac))
    
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
# END
