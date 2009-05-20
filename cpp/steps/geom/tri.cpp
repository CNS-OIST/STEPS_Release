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

// STL headers.
#include <cassert>
#include <cmath>
#include <sstream>


// STEPS headers.
#include <steps/common.h>
#include <steps/math/triangle.hpp>
#include <steps/geom/tri.hpp>
#include <steps/error.hpp>

NAMESPACE_ALIAS(steps::tetmesh, stetmesh);

////////////////////////////////////////////////////////////////////////////////

stetmesh::Tri::Tri(Tetmesh * mesh, uint tidx)
: pTetmesh(mesh)
, pTidx(tidx)
, pVerts()
, pBaryc()
{
	if (pTetmesh == 0)
    {
		std::ostringstream os;
        os << "No mesh provided to Tri initializer function";
        throw steps::ArgErr(os.str());
    }

    uint * tri_temp = pTetmesh->_getTri(tidx);
    pVerts[0] = tri_temp[0];
    pVerts[1] = tri_temp[1];
    pVerts[2] = tri_temp[2];

    pBaryc = new double[3];
}

////////////////////////////////////////////////////////////////////////////////

stetmesh::Tri::~Tri(void)
{
	delete pBaryc;
}

////////////////////////////////////////////////////////////////////////////////

double stetmesh::Tri::getArea(void) const
{
	assert(pTetmesh != 0);
	return (pTetmesh->getTriArea(pTidx));
}

////////////////////////////////////////////////////////////////////////////////

std::vector<double> stetmesh::Tri::getBarycenter(void) const
{
	double * v0 = pTetmesh->_getVertex(pVerts[0]);
	double * v1 = pTetmesh->_getVertex(pVerts[1]);
	double * v2 = pTetmesh->_getVertex(pVerts[2]);
	/*double v0[3], v1[3], v2[3];	// Defunct code. Pointers directly fetched
	for (uint i=0; i < 3; ++i)
	{
		v0[i] = v0vec[i];
		v1[i] = v1vec[i];
		v2[i] = v2vec[i];
	}*/
	double baryc[3];
	steps::math::triBarycenter(v0, v1, v2, baryc);
	std::vector<double> barycentre(3);
	barycentre[0] = baryc[0];
	barycentre[1] = baryc[1];
	barycentre[2] = baryc[2];
	return barycentre;
}

////////////////////////////////////////////////////////////////////////////////

std::vector<double> stetmesh::Tri::getNorm(void) const
{
	assert (pTetmesh != 0);
	return (pTetmesh->getTriNorm(pTidx));
}

////////////////////////////////////////////////////////////////////////////////

stetmesh::TmPatch * stetmesh::Tri::getPatch(void) const
{
	assert (pTetmesh != 0);
	return (pTetmesh->getTriPatch(pTidx));
}

////////////////////////////////////////////////////////////////////////////////

stetmesh::Tet stetmesh::Tri::getTet(uint i) const
{
	assert(i <= 1);
	int tetidx = pTetmesh->_getTriTetNeighb(pTidx)[i];
	assert(tetidx != -1);
	return (Tet(pTetmesh, tetidx));
}

////////////////////////////////////////////////////////////////////////////////

int stetmesh::Tri::getTetIdx(uint i) const
{
	assert(i <= 1);
	return (pTetmesh->_getTriTetNeighb(pTidx)[i]);
}

////////////////////////////////////////////////////////////////////////////////

uint stetmesh::Tri::getVertexIdx(uint i) const
{
	assert (i <= 2);
	return pVerts[i];
}

////////////////////////////////////////////////////////////////////////////////

stetmesh::Tet stetmesh::Tri::getTet0(void) const
{
	return getTet(0);
}

////////////////////////////////////////////////////////////////////////////////

stetmesh::Tet stetmesh::Tri::getTet1(void) const
{
	return getTet(1);
}

////////////////////////////////////////////////////////////////////////////////

stetmesh::Tet stetmesh::Tri::getInnerTet(void) const
{
	return getTet(0);
}

////////////////////////////////////////////////////////////////////////////////

stetmesh::Tet stetmesh::Tri::getOuterTet(void) const
{
	return getTet(1);
}

////////////////////////////////////////////////////////////////////////////////

double * stetmesh::Tri::_getNorm(void) const
{
	assert (pTetmesh != 0);
	return (pTetmesh->_getTriNorm(pTidx));
}

////////////////////////////////////////////////////////////////////////////////

double * stetmesh::Tri::_getBarycenter(void) const
{
	double * v0 = pTetmesh->_getVertex(pVerts[0]);
	double * v1 = pTetmesh->_getVertex(pVerts[1]);
	double * v2 = pTetmesh->_getVertex(pVerts[2]);

	steps::math::triBarycenter(v0, v1, v2, pBaryc);

	return pBaryc;
}

////////////////////////////////////////////////////////////////////////////////

// END
