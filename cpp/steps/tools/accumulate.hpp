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

#ifndef STEPS_TOOLS_ACCUMULATE_HPP
#define STEPS_TOOLS_ACCUMULATE_HPP 1

// Autotools definitions.
#ifdef HAVE_CONFIG_H
#include <steps/config.h>
#endif

// STEPS headers.
#include <steps/common.h>

START_NAMESPACE(steps)
START_NAMESPACE(tools)

////////////////////////////////////////////////////////////////////////////////

template <typename InputIterator, typename ValueType >
ValueType accumulate(InputIterator begin, InputIterator end, ValueType init)
{
    while (begin != end)
    {
        init += *begin;
        ++begin;
    }
    return init;
}

////////////////////////////////////////////////////////////////////////////////

END_NAMESPACE(tools)
END_NAMESPACE(steps)

#endif
// STEPS_TOOLS_ACCUMULATE_HPP

// END
