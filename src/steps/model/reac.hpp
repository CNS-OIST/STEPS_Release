/*
 #################################################################################
#
#    STEPS - STochastic Engine for Pathway Simulation
#    Copyright (C) 2007-2020 Okinawa Institute of Science and Technology, Japan.
#    Copyright (C) 2003-2006 University of Antwerp, Belgium.
#    
#    See the file AUTHORS for details.
#    This file is part of STEPS.
#    
#    STEPS is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 2,
#    as published by the Free Software Foundation.
#    
#    STEPS is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################   

 */

/*
 *  Last Changed Rev:  $Rev$
 *  Last Changed Date: $Date$
 *  Last Changed By:   $Author$
 */

#ifndef STEPS_MODEL_REAC_HPP
#define STEPS_MODEL_REAC_HPP 1


// STL headers.
#include <cassert>
#include <string>
#include <vector>
#include <map>

// STEPS headers.
#include "steps/common.h"

////////////////////////////////////////////////////////////////////////////////
 namespace steps {
 namespace model {

////////////////////////////////////////////////////////////////////////////////

// Forward declarations.
class Reac;
class Volsys;
class Model;
class Spec;

// Auxiliary declarations.
typedef Reac *                           ReacP;
typedef std::map<std::string, ReacP>     ReacPMap;
typedef ReacPMap::iterator               ReacPMapI;
typedef ReacPMap::const_iterator         ReacPMapCI;
typedef std::vector<ReacP>               ReacPVec;
typedef ReacPVec::iterator               ReacPVecI;
typedef ReacPVec::const_iterator         ReacPVecCI;

////////////////////////////////////////////////////////////////////////////////
/// Reaction in a volume system.
///
/// A kinetic reaction is specified by:
///     - Species appear on the left hand side of the reaction (lhs).
///     - Species appear on the right hand side of the reaction (rhs).
///     - Rate constant for the reaction (kcst).
///
/// \sa SReac, Volsys.
/// \warning Methods start with an underscore are not exposed to Python.
///

class Reac
{

public:

    ////////////////////////////////////////////////////////////////////////
    // OBJECT CONSTRUCTION & DESTRUCTION
    ////////////////////////////////////////////////////////////////////////
    /// Constructor
    ///
    /// \param id ID of the reaction.
    /// \param volsys Pointer to the parent volume system.
    /// \param lhs Vector of pointers to the species on the left hand side of the reaction.
    /// \param rhs Vector of pointers to the species on the right hand side of the reaction.
    /// \param kcst Rate constant for the reaction.
    Reac(std::string const & id, Volsys * volsys,
         std::vector<Spec *> const & lhs = {},
         std::vector<Spec *> const & rhs = {},
         double kcst = 0.0);

    /// Destructor
    ~Reac();

    ////////////////////////////////////////////////////////////////////////
    // REACTION RULE PROPERTIES
    ////////////////////////////////////////////////////////////////////////

    /// Return the reaction rule ID.
    ///
    /// \return ID of the reaction.
    inline std::string getID() const noexcept
    { return pID; }

    /// Set or change the reaction rule ID.
    ///
    /// \param id ID of the reaction.
    void setID(std::string const & id);

    /// Return a pointer to the parent volume system.
    ///
    /// \return Pointer to the volume system.
    inline Volsys * getVolsys() const noexcept
    { return pVolsys; }

    /// Return a pointer to the parent model.
    ///
    /// \return Pointer to the parent Model.
    inline Model * getModel() const noexcept
    { return pModel; }

    ////////////////////////////////////////////////////////////////////////
    // OPERATIONS (EXPOSED TO PYTHON):
    ////////////////////////////////////////////////////////////////////////
    /// Get the species on the left hand side of the reaction.
    ///
    /// \return Vector of pointers to the left hand side species.
    const std::vector<Spec *> & getLHS() const
    { return pLHS; }

    /// Set or reset the species on the left hand side of the reaction.
    ///
    /// \param lhs Vector of pointers to the left hand side species.
    void setLHS(std::vector<Spec *> const & lhs);

    /// Get the species on the right hand side of the reaction.
    ///
    ///    \return Vector of pointers to the right hand side species.
    inline const std::vector<Spec *> & getRHS() const noexcept
    { return pRHS; }

    /// Set or reset the species on the right hand side of the reaction.
    ///
    /// \param rhs Vector of pointers to the right hand side species.
    void setRHS(std::vector<Spec *> const & rhs);

    /// Return all species invloved in the reaction.
    ///
    ///    This method returns a list of all species involved in this reaction,
    /// on both the left and right-hand side. No duplicate member includes.
    ///
    /// \return Vector of pointers to the species.
    std::vector<Spec *> getAllSpecs() const;

    /// Return the order of the reaction.
    ///
    /// \return The order of the reaction.
    inline uint getOrder() const noexcept
    { return pOrder; }

    /// Return the rate constant of the reaction.
    ///
    /// \return The rate constant of the reaction.
    inline double getKcst() const noexcept
    { return pKcst; }

    /// Set or reset the rate constant of the reaction.
    ///
    /// \param kcst The rate constant of the reaction.
    void setKcst(double kcst);

    ////////////////////////////////////////////////////////////////////////
    // INTERNAL (NON-EXPOSED) OPERATIONS: DELETION
    ////////////////////////////////////////////////////////////////////////

    /// Self delete.
    ///
    /// Called if Python object deleted, or from del method in parent object.
    /// \warning Will only be called once
    void _handleSelfDelete();

    ////////////////////////////////////////////////////////////////////////

private:

    ////////////////////////////////////////////////////////////////////////

    std::string                         pID;
    Model                             * pModel;
    Volsys                            * pVolsys;

    std::vector<Spec *>                 pLHS;
    std::vector<Spec *>                 pRHS;
    uint                                pOrder;
    double                              pKcst;

    ////////////////////////////////////////////////////////////////////////

};

////////////////////////////////////////////////////////////////////////////////

}
}

#endif
// STEPS_MODEL_REAC_HPP

// END
