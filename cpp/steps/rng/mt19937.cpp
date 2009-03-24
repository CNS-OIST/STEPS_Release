////////////////////////////////////////////////////////////////////////////////
// STEPS - STochastic Engine for Pathway Simulation
// Copyright (C) 2005-2008 Stefan Wils. All rights reserved.
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
//
////////////////////////////////////////////////////////////////////////////////


// Autotools definitions.
#ifdef HAVE_CONFIG_H
#include <steps/config.h>
#endif

// Standard library & STL headers.
#include <cassert>
#include <string>
#include <sstream>

// STEPS headers.
#include <steps/common.h>
#include <steps/rng/rng.hpp>
#include <steps/rng/mt19937.hpp>
#include <steps/error.hpp>

////////////////////////////////////////////////////////////////////////////////

// STEPS library.
NAMESPACE_ALIAS(steps::rng, srng);
USING(srng, MT19937);

////////////////////////////////////////////////////////////////////////////////

void MT19937::concreteInitialize(ulong seed)
{
    pState[0] = seed & 0xffffffffUL;
    for (pStateInit = 1; pStateInit < MT_N; pStateInit++)
    {
        pState[pStateInit] =
            (1812433253UL * (pState[pStateInit - 1] ^
            (pState[pStateInit - 1] >> 30)) + pStateInit);
        // See Knuth TAOCP Vol2. 3rd Ed. P.106 for multiplier.
        // In the previous versions, MSBs of the seed affect
        // only MSBs of the array pState[].
        // 2002/01/09 modified by Makoto Matsumoto
        pState[pStateInit] &= 0xffffffffUL;
        // for >32 bit machines
    }
}

////////////////////////////////////////////////////////////////////////////////

/// Fills the buffer with random numbers on [0,0xffffffff]-interval.
void MT19937::concreteFillBuffer(void)
{
    ulong y;
    static ulong mag01[2] = { 0x0UL, MT_MATRIX_A };
    // mag01[x] = x * MATRIX_A  for x=0,1

    for (uint *b = rBuffer; b < rEnd; ++b)
    {
        if (pStateInit >= MT_N)
        {
            // Generate N words at one time
            int kk;

            // If init_genrand() has not been called, a default
            // initial seed is used.
            if (pStateInit == MT_N + 1) initialize(5489UL);

            for (kk = 0; kk < MT_N - MT_M; ++kk)
            {
                y = (pState[kk] & MT_UPPER_MASK) | (pState[kk + 1] & MT_LOWER_MASK);
                pState[kk] = pState[kk + MT_M] ^ (y >> 1) ^ mag01[y & 0x1UL];
            }
            for (; kk < MT_N - 1; ++kk)
            {
                y = (pState[kk] & MT_UPPER_MASK) | (pState[kk + 1] & MT_LOWER_MASK);
                pState[kk] = pState[kk + (MT_M - MT_N)] ^
                    (y >> 1) ^ mag01[y & 0x1UL];
            }
            y = (pState[MT_N - 1] & MT_UPPER_MASK) | (pState[0] & MT_LOWER_MASK);
            pState[MT_N - 1] = pState[MT_M - 1] ^ (y >> 1) ^ mag01[y & 0x1UL];

            pStateInit = 0;
        }

        y = pState[pStateInit++];

        // Tempering.
        y ^= (y >> 11);
        y ^= (y << 7) & 0x9d2c5680UL;
        y ^= (y << 15) & 0xefc60000UL;
        y ^= (y >> 18);

        *b = static_cast<uint>(y);
    }
}

////////////////////////////////////////////////////////////////////////////////

MT19937::MT19937(uint bufsize)
: RNG(bufsize)
{
}

////////////////////////////////////////////////////////////////////////////////

MT19937::~MT19937(void)
{
}

////////////////////////////////////////////////////////////////////////////////

srng::RNG * srng::create_mt19937(uint bufsize)
{
    return new MT19937(bufsize);
}

////////////////////////////////////////////////////////////////////////////////

srng::RNG * srng::create(std::string rng_name, uint bufsize)
{
	std::string rn = "mt19937";
	if (rng_name == rn) return new MT19937(bufsize);
	else
	{
		std::ostringstream os;
	    os << "Random number generator " << rng_name << " currently not ";
	    os << "included in STEPS.";
	    throw steps::ArgErr(os.str());
	}
}
////////////////////////////////////////////////////////////////////////////////

// END
