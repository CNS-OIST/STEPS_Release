////////////////////////////////////////////////////////////////////////////////
// STEPS - STochastic Engine for Pathway Simulation
// Copyright (C) 2007-2009�Okinawa Institute of Science and Technology, Japan.
// Copyright (C) 2003-2006�University of Antwerp, Belgium.
//
// See the file AUTHORS for details.
//
// This file is part of STEPS.
//
// STEPS�is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// STEPS�is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.�If not, see <http://www.gnu.org/licenses/>.
//
////////////////////////////////////////////////////////////////////////////////

#ifndef STEPS_SOLVER_DIFFDEF_HPP
#define STEPS_SOLVER_DIFFDEF_HPP 1

// Autotools definitions.
#ifdef HAVE_CONFIG_H
#include <steps/config.h>
#endif

// STL headers.
#include <string>

// STEPS headers.
#include <steps/common.h>
#include <steps/solver/statedef.hpp>
#include <steps/model/diff.hpp>

////////////////////////////////////////////////////////////////////////////////

START_NAMESPACE(steps)
START_NAMESPACE(solver)

// Forwards declarations
//class Statedef;

////////////////////////////////////////////////////////////////////////////////
/// Defined diffusion object.
class Diffdef
{

public:
    /// Constructor
    ///
    /// \param sd State of the solver.
    /// \param idx Global index of the object.
    /// \param d Pointer to the associated Diff object.
	Diffdef(Statedef * sd, uint idx, steps::model::Diff * d);

    /// Destructor
	~Diffdef(void);

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: DIFFUSION RULE
    ////////////////////////////////////////////////////////////////////////

	/// Return the global index of this diffusion rule.
	inline uint gidx(void) const
	{ return pIdx; }

    /// Return the name of this diffusion rule.
	std::string const name(void) const;

	/// Return the diffusion constant.
	double dcst(void) const;

    ////////////////////////////////////////////////////////////////////////
    // DATA ACCESS: LIGAND
    ////////////////////////////////////////////////////////////////////////

    /// Return the global index of the ligand species.
    uint lig(void) const;

    /// \todo check
    int dep(uint gidx) const;
    /// \todo check
    bool reqspec(uint gidx) const;


    ////////////////////////////////////////////////////////////////////////
    // SOLVER METHODS: SETUP
    ////////////////////////////////////////////////////////////////////////

    /// Setup the object.
	void setup(void);

    ////////////////////////////////////////////////////////////////////////
    // SOLVER METHODS: DIFFUSION RULE
    ////////////////////////////////////////////////////////////////////////

	/// Set the diffusion constant for this diffusion rule.
    ///
    /// \param d Rate constant of the diffusion rule.
	void setDcst(double d);

	/// Set the ligand of the diffusion rule by its global index
    ///
    /// \param gidx Global index of the diffusion rule.
	void setLig(uint gidx);

    ////////////////////////////////////////////////////////////////////////

private:

    ////////////////////////////////////////////////////////////////////////

	Statedef                          * pStatedef;
	steps::model::Diff                * pDiff;
	uint                                pIdx;
	bool								pSetupdone;

    ////////////////////////////////////////////////////////////////////////
    // DATA: LIGAND
    ////////////////////////////////////////////////////////////////////////

    int                               * pSpec_DEP;

    ////////////////////////////////////////////////////////////////////////

};

////////////////////////////////////////////////////////////////////////////////

END_NAMESPACE(solver)
END_NAMESPACE(steps)

#endif
// STEPS_SOLVER_DIFFDEF_HPP

// END
