////////////////////////////////////////////////////////////////////////////////
// STEPS - STochastic Engine for Pathway Simulation
// Copyright (C) 2005-2007 Stefan Wils. All rights reserved.
//
// $Id$
////////////////////////////////////////////////////////////////////////////////

#ifndef STEPS_MATH_CONSTANTS_HPP
#define STEPS_MATH_CONSTANTS_HPP 1

// Autotools definitions.
#ifdef HAVE_CONFIG_H
#include <steps/config.h>
#endif

// STEPS headers.
#include <steps/common.h>

START_NAMESPACE(steps)
START_NAMESPACE(math)

////////////////////////////////////////////////////////////////////////////////

const double E                          = 2.71828182845904523536028747135;
const double PI                         = 3.14159265358979323846264338328;

const float  IEEE_MACH_EPSILON32        = 2e-24;
const double IEEE_MACH_EPSILON64        = 2e-53;
const float  IEEE_EPSILON32             = 1.0e-7;
const double IEEE_EPSILON64             = 1.0e-15;

const double  IEEE_HUGE                 = 1e150;

////////////////////////////////////////////////////////////////////////////////

/// Source: physics.nist.gov/cgi-bin/cuu/Value?na|search_for=avogadrp
const double AVOGADRO                   = 6.0221415e23;

////////////////////////////////////////////////////////////////////////////////

const double M_TO_NM                    = 1.0e9;
const double M_TO_UM                    = 1.0e6;
const double M_TO_MM                    = 1.0e3;
const double M_TO_CM                    = 1.0e2;
const double M_TO_DM                    = 1.0e1;

const double UM_TO_M                    = 1.0e-6;

////////////////////////////////////////////////////////////////////////////////

const double M2_TO_UM2                  = 1.0e12;

const double UM2_TO_M2                  = 1.0e-12;

////////////////////////////////////////////////////////////////////////////////

const double M3_TO_DM3                  = 1.0e3;

const double DM3_TO_M3                  = 1.0e-3;

const double M3_TO_UM3                  = 1.0e18;

const double UM3_TO_M3                  = 1.0e-18;

////////////////////////////////////////////////////////////////////////////////

const double MS_TO_S                    = 1.0e-3;

const double S_TO_MS                    = 1.0e3;

////////////////////////////////////////////////////////////////////////////////

END_NAMESPACE(math)
END_NAMESPACE(steps)

#endif
// STEPS_MATH_CONSTANTS_HPP

// END
