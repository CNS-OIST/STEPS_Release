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

// Autotools definitions.
#ifdef HAVE_CONFIG_H
#include <steps/config.h>
#endif

// STL headers.
#include <cassert>
#include <sstream>
#include <string>

// STEPS headers.
#include <steps/common.h>
#include <steps/error.hpp>
#include <steps/model/model.hpp>
#include <steps/model/spec.hpp>

////////////////////////////////////////////////////////////////////////////////

USING_NAMESPACE(std);
USING_NAMESPACE(steps::model);

////////////////////////////////////////////////////////////////////////////////

Spec::Spec(string const & id, Model * model)
: pID(id)
, pModel(model)
{
    if (pModel == 0)
    {
        ostringstream os;
        os << "No model provided to Spec initializer function";
        throw steps::ArgErr(os.str());
    }
    pModel->_handleSpecAdd(this);
}

////////////////////////////////////////////////////////////////////////////////

Spec::~Spec(void)
{
    if (pModel == 0) return;
	_handleSelfDelete();
}

////////////////////////////////////////////////////////////////////////////////

void Spec::_handleSelfDelete(void)
{
    pModel->_handleSpecDel(this);
    pModel = 0;
}

////////////////////////////////////////////////////////////////////////////////

void Spec::setID(string const & id)
{
    assert(pModel != 0);
    if (id == pID) return;
    // The following might raise an exception, e.g. if the new ID is not
    // valid or not unique. If this happens, we don't catch but simply let
    // it pass by into the Python layer.
    pModel->_handleSpecIDChange(pID, id);
    // This line will only be executed if the previous call didn't raise
    // an exception.
    pID = id;
}

////////////////////////////////////////////////////////////////////////////////

// END
