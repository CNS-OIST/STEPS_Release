////////////////////////////////////////////////////////////////////////////////
// STEPS - STochastic Engine for Pathway Simulation
// Copyright (C) 2005-2007 Stefan Wils. All rights reserved.
//
// This file is part of STEPS.
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301, USA
//
// $Id$
////////////////////////////////////////////////////////////////////////////////

#ifndef STEPS_WMDIRECT_SOLVER_CORE_COMP_HPP
#define STEPS_WMDIRECT_SOLVER_CORE_COMP_HPP 1

// Autotools definitions.
#ifdef HAVE_CONFIG_H
#include <steps/config.h>
#endif

// STL headers.
#include <cassert>
#include <vector>

// STEPS headers.
#include <steps/common.h>
#include <steps/sim/shared/compdef.hpp>
#include <steps/wmdirect/solver_core/kproc.hpp>
#include <steps/wmdirect/solver_core/patch.hpp>

////////////////////////////////////////////////////////////////////////////////

// Forward declarations.
class Comp;
class Reac;
class Sched;

// Auxiliary declarations.
typedef Comp *                          CompP;
typedef std::vector<CompP>              CompPVec;
typedef CompPVec::iterator              CompPVecI;
typedef CompPVec::const_iterator        CompPVecCI;

////////////////////////////////////////////////////////////////////////////////

class Comp
{
    
public:
    
    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////
    
    Comp(steps::sim::CompDef * compdef);
    ~Comp(void);
    
    void setupKProcs(Sched * s);
    void setupDeps(void);
    
    void reset(void);
    
    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS
    ////////////////////////////////////////////////////////////////////////
    
    inline steps::sim::CompDef * def(void) const
    { return pCompDef; }
    
    inline double vol(void) const
    { return pCompDef->vol(); }
    
    ////////////////////////////////////////////////////////////////////////
    
    inline uint * pools(void) const
    { return pPoolCount; }
    
    static const uint CLAMPED = 1;
    
    inline bool clamped(uint lidx) const
    { return pPoolFlags[lidx] & CLAMPED; }
    void setClamped(uint lidx, bool clamp);

    ////////////////////////////////////////////////////////////////////////

    inline KProcPVecCI kprocBegin(void) const
    { return pKProcs.begin(); }
    inline KProcPVecCI kprocEnd(void) const
    { return pKProcs.end(); }
    inline uint countKProcs(void) const
    { return pKProcs.size(); }
    
    Reac * reac(uint lidx) const;
    
    ////////////////////////////////////////////////////////////////////////
    
    void addIPatch(Patch * p);
    
    inline uint countIPatches(void) const
    { return pIPatches.size(); }
    
    inline PatchPVecCI beginIPatches(void) const
    { return pIPatches.begin(); }
    inline PatchPVecCI endIPatches(void) const
    { return pIPatches.end(); }
    
    void addOPatch(Patch * p);
    
    inline uint countOPatches(void) const
    { return pOPatches.size(); }
    
    inline PatchPVecCI beginOPatches(void) const
    { return pOPatches.begin(); }
    inline PatchPVecCI endOPatches(void) const
    { return pOPatches.end(); }
    
    ////////////////////////////////////////////////////////////////////////
    
private:
    
    ////////////////////////////////////////////////////////////////////////
    
    steps::sim::CompDef *       pCompDef;
    
    /// Numbers of molecules -- stored as machine word integers.
    uint *                      pPoolCount;
    /// Flags on these pools -- stored as machine word flags.
    uint *                      pPoolFlags;
    
    /// The kinetic processes.
    KProcPVec                   pKProcs;
    
    PatchPVec                   pIPatches;
    PatchPVec                   pOPatches;
    
    ////////////////////////////////////////////////////////////////////////
    
    // Disable constructors.
    Comp(void);
    Comp(Comp const &);
    
    ////////////////////////////////////////////////////////////////////////
    
};

////////////////////////////////////////////////////////////////////////////////

#endif
// STEPS_WMDIRECT_SOLVER_CORE_COMP_HPP

// END
