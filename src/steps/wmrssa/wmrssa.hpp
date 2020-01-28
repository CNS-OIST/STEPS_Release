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


#ifndef STEPS_SOLVER_WMRSSA_HPP
#define STEPS_SOLVER_WMRSSA_HPP 1


// STL headers.
#include <string>
#include <vector>
#include <set>
#include <map>
#include <fstream>

// STEPS headers.
#include "steps/common.h"
#include "steps/solver/api.hpp"
#include "steps/solver/statedef.hpp"
#include "steps/solver/compdef.hpp"
#include "steps/solver/patchdef.hpp"
#include "steps/wmrssa/comp.hpp"
#include "steps/wmrssa/patch.hpp"
#include "steps/wmrssa/kproc.hpp"

////////////////////////////////////////////////////////////////////////////////

 namespace steps {
 namespace wmrssa {

////////////////////////////////////////////////////////////////////////////////

// Forward declarations.


// Auxiliary declarations.
typedef uint                            SchedIDX;
typedef std::set<SchedIDX>              SchedIDXSet;
typedef SchedIDXSet::iterator           SchedIDXSetI;
typedef SchedIDXSet::const_iterator     SchedIDXSetCI;
typedef std::vector<SchedIDX>           SchedIDXVec;
typedef SchedIDXVec::iterator           SchedIDXVecI;
typedef SchedIDXVec::const_iterator     SchedIDXVecCI;

////////////////////////////////////////////////////////////////////////////////

/// Copies the contents of a set of SchedIDX entries into a vector.
/// The contents of the vector are completely overridden.
///
extern void schedIDXSet_To_Vec(SchedIDXSet const & s, SchedIDXVec & v);

////////////////////////////////////////////////////////////////////////////////

class Wmrssa: public steps::solver::API
{

public:

    Wmrssa(steps::model::Model *m, steps::wm::Geom *g, const rng::RNGptr &r);
    ~Wmrssa() override;

    ////////////////////////////////////////////////////////////////////////
    // CHECKPOINTING
    ////////////////////////////////////////////////////////////////////////
    /// checkpoint data
    void checkpoint(std::string const & file_name) override;

    /// restore data
    void restore(std::string const & file_name) override;

    ////////////////////////////////////////////////////////////////////////
    // SOLVER INFORMATION
    ////////////////////////////////////////////////////////////////////////

    std::string getSolverName() const override;
    std::string getSolverDesc() const override;
    std::string getSolverAuthors() const override;
    std::string getSolverEmail() const override;


    ////////////////////////////////////////////////////////////////////////
    // SOLVER CONTROLS
    ////////////////////////////////////////////////////////////////////////

    void reset() override;
    void run(double endtime) override;
    void advance(double adv) override;
    void step() override;

    ////////////////////////////////////////////////////////////////////////
    // SOLVER STATE ACCESS:
    //      GENERAL
    ////////////////////////////////////////////////////////////////////////


    double getTime() const override;

    uint getNSteps() const override;

    ////////////////////////////////////////////////////////////////////////
    // SOLVER STATE ACCESS:
    //      ADVANCE
    //      Developer only
    ////////////////////////////////////////////////////////////////////////

    void setTime(double time) override;
    void setNSteps(uint nsteps) override;

    ////////////////////////////////////////////////////////////////////////
    // SOLVER STATE ACCESS:
    //      COMPARTMENT
    ////////////////////////////////////////////////////////////////////////

     double _getCompVol(uint cidx) const override;
    void _setCompVol(uint cidx, double vol) override;

     double _getCompCount(uint cidx, uint sidx) const override;
     void _setCompCount(uint cidx, uint sidx, double n) override;

     double _getCompAmount(uint cidx, uint sidx) const override;
    void _setCompAmount(uint cidx, uint sidx, double a) override;

    double _getCompConc(uint cidx, uint sidx) const override;
     void _setCompConc(uint cidx, uint sidx, double c) override;

    bool _getCompClamped(uint cidx, uint sidx) const override;
    void _setCompClamped(uint cidx, uint sidx, bool b) override;

    double _getCompReacK(uint cidx, uint ridx) const override;
    void _setCompReacK(uint cidx, uint ridx, double kf) override;

     bool _getCompReacActive(uint cidx, uint ridx) const override;
    void _setCompReacActive(uint cidx, uint ridx, bool a) override;

    double _getCompReacC(uint cidx, uint ridx) const override;

    double _getCompReacH(uint cidx, uint ridx) const override;

    long double _getCompReacA(uint cidx, uint ridx) const override;

    unsigned long long _getCompReacExtent(uint cidx, uint ridx) const override;
     void _resetCompReacExtent(uint cidx, uint ridx) override;

    ////////////////////////////////////////////////////////////////////////
/*
    double _getCompDiffD(uint cidx, uint didx);
    void _setCompDiffD(uint cidx, uint didx);

    bool _getCompDiffActive(uint cidx, uint didx);
    void _setCompDiffActive(uint cidx, uint didx, bool act);
*/

    ////////////////////////////////////////////////////////////////////////
    // SOLVER STATE ACCESS:
    //      PATCH
    ////////////////////////////////////////////////////////////////////////

    double _getPatchArea(uint pidx) const override;
    void _setPatchArea(uint pidx, double area) override;

     double _getPatchCount(uint pidx, uint sidx) const override;
    void _setPatchCount(uint pidx, uint sidx, double n) override;

    double _getPatchAmount(uint pidx, uint sidx) const override;
     void _setPatchAmount(uint pidx, uint sidx, double a) override;

    bool _getPatchClamped(uint pidx, uint sidx) const override;
    void _setPatchClamped(uint pidx, uint sidx, bool buf) override;

    double _getPatchSReacK(uint pidx, uint ridx) const override;
      void _setPatchSReacK(uint pidx, uint ridx, double kf) override;

     bool _getPatchSReacActive(uint pidx, uint ridx) const override;
     void _setPatchSReacActive(uint pidx, uint ridx, bool a) override;

     double _getPatchSReacC(uint pidx, uint ridx) const override;

     double _getPatchSReacH(uint pidx, uint ridx) const override;

     double _getPatchSReacA(uint pidx, uint ridx) const override;

     unsigned long long _getPatchSReacExtent(uint pidx, uint ridx) const override;
    void _resetPatchSReacExtent(uint pidx, uint ridx) override;

    ////////////////////////////////////////////////////////////////////////

    // Called from local Comp or Patch objects. Ass KProc to this object
    void addKProc(steps::wmrssa::KProc * kp);

    inline uint countKProcs() const noexcept
    { return pKProcs.size(); }

    ////////////////////////////////////////////////////////////////////////

private:

    ////////////////////////////////////////////////////////////////////////
    // WMRSSA SOLVER METHODS
    ////////////////////////////////////////////////////////////////////////

    uint _addComp(steps::solver::Compdef * cdef);

    uint _addPatch(steps::solver::Patchdef * pdef);

    // called when local comp, patch, reac, sreac objects have been created
    // by constructor
    void _setup();

    void _build();

    uint _getNext() const;

    void _reset();

    void _update(SchedIDXVec const & entries);

    void _executeStep(steps::wmrssa::KProc * kp, double dt);

    ////////////////////////////////////////////////////////////////////////
    // LIST OF WMRSSA SOLVER OBJECTS
    ////////////////////////////////////////////////////////////////////////

    std::vector<steps::wmrssa::KProc *>      pKProcs;

    std::vector<steps::wmrssa::Comp *>       pComps;
    std::map<steps::solver::Compdef *, Comp *> pCompMap;

    std::vector<steps::wmrssa::Patch *>      pPatches;

    /// \brief sum of propensities
    double                                     pA0{0.0};

    ////////////////////////////////////////////////////////////////////////
    // N-ARY TREE
    ////////////////////////////////////////////////////////////////////////

    std::vector<uint>                          pLevelSizes;

    std::vector<double *>                      pLevels;

    ////////////////////////////////////////////////////////////////////////

    // Keeps track of whether _build() has been called
    bool                                       pBuilt{false};

    ////////////////////////////////////////////////////////////////////////

    // Tables to hold update vector indices and random numbers respectively,
    // to be re-used each step.
    uint                                     * pIndices{nullptr};
    uint                                        pMaxUpSize{0};
    double                                   * pRannum{nullptr};

    ////////////////////////////////////////////////////////////////////////

    uint countUpdate{0};
    uint countSteps{0};

};

////////////////////////////////////////////////////////////////////////////////

}
}

#endif
// STEPS_SOLVER_WMRSSA_HPP

// END
