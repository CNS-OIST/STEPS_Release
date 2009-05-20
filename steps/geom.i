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
// $Id$
////////////////////////////////////////////////////////////////////////////////

%module geom_swig

%include "python/std_map.i"
%include "python/std_string.i"
%include "python/std_vector.i"
%include "python/std_set.i"
%include "error.i"
%import "cpp/steps/common.h"

%{
	// Autotools definitions.
#ifdef HAVE_CONFIG_H
#include <steps/config.h>
#endif
#include <steps/geom/geom.hpp>
#include <steps/geom/comp.hpp>
#include <steps/geom/patch.hpp>
#include <steps/geom/tmcomp.hpp>
#include <steps/geom/tmpatch.hpp>
#include <steps/geom/tet.hpp>
#include <steps/geom/tetmesh_rw.hpp>
#include <steps/geom/tetmesh.hpp>
#include <steps/geom/tri.hpp>
#include <steps/error.hpp>
%}


////////////////////////////////////////////////////////////////////////////////

namespace steps
{
namespace wm
{

class Comp;
class Patch;
class Geom;

}
}

namespace steps
{
namespace model
{	

class Surfsys;
class Volsys;

}
}

namespace steps
{
namespace tetmesh
{
		
class Tetmesh;
class Tri;
class Tet;
class TmPatch;
class TmComp;

}
}

///////////////////////////////////////////////////////////////////////////////

namespace std
{
	%template(set_str)    set<std::string>;
	%template(set_ptc)    set<steps::wm::Patch *>;
	%template(vector_ptc) vector<steps::wm::Patch *>;
	%template(vector_cmp) vector<steps::wm::Comp *>;
	%template(vector_int) vector<int>;
	%template(vector_uint) vector<unsigned int>;
	%template(vector_dbl) vector<double>;
	%template(vector_bool) vector<bool>;
}

%feature("autodoc", "1");

///////////////////////////////////////////////////////////////////////////////

%exception 
{
	try {
		$action
	} catch (steps::ArgErr & ae) {
		PyErr_SetString(PyExc_NameError, ae.getMsg());
		return NULL;
	} catch (steps::NotImplErr & nie) {
		PyErr_SetString(PyExc_NotImplementedError, nie.getMsg());
		return NULL;
	}
}

///////////////////////////////////////////////////////////////////////////////

namespace steps
{
namespace wm
{

////////////////////////////////////////////////////////////////////////////////

bool isValidID(std::string const & id);
void checkID(std::string const & id);

////////////////////////////////////////////////////////////////////////////////

class Geom
{
	
public:
	
	Geom(void);
	virtual ~Geom(void);
	
	steps::wm::Comp * getComp(std::string const & id) const;
	void delComp(std::string const & id);
	std::vector<steps::wm::Comp *> getAllComps(void) const;
	
	steps::wm::Patch * getPatch(std::string const & id) const;
	void delPatch(std::string const & id);
	std::vector<steps::wm::Patch *> getAllPatches(void) const;
	
};

////////////////////////////////////////////////////////////////////////////////

%feature("kwargs") Patch::Patch;

class Patch
{
	
public:
	
	Patch(std::string const & id, steps::wm::Geom * container, 
		  steps::wm::Comp * icomp, steps::wm::Comp * ocomp = 0, 
		  steps::model::Surfsys * surfsys = 0, double area = 0.0);
	virtual ~Patch(void);
	
	std::string getID(void) const;
	void setID(std::string const & id);
	
	steps::wm::Geom * getContainer(void) const;
	double getArea(void) const;
	virtual void setArea(double vol);
	
	void addSurfsys(std::string const & id);
	std::set<std::string> getSurfsys(void) const;
	void delSurfsys(std::string const & id);
	
	steps::wm::Comp * getIComp(void) const;
	steps::wm::Comp * getOComp(void) const;
	
};

////////////////////////////////////////////////////////////////////////////////

%feature("kwargs") Comp::Comp;

class Comp
{
	
public:
	
	Comp(std::string const & id, steps::wm::Geom * container,
		 steps::model::Volsys * volsys = 0, double vol = 0.0);
	virtual ~Comp(void);
	
	std::string getID(void) const;
	void setID(std::string const & id);
	
	steps::wm::Geom * getContainer(void) const;
	
	double getVol(void) const;
	virtual void setVol(double vol);
	
	void addVolsys(std::string const & id);
	std::set<std::string> getVolsys(void) const;
	void delVolsys(std::string const & id);
	
	std::set<steps::wm::Patch *> getIPatches(void) const;
	std::set<steps::wm::Patch *> getOPatches(void) const;
    
};

////////////////////////////////////////////////////////////////////////////////

} // namespace wm
} // namespace steps

////////////////////////////////////////////////////////////////////////////////

namespace steps
{
namespace tetmesh
{	

////////////////////////////////////////////////////////////////////////////////

class Tetmesh : public steps::wm::Geom
{

public:
	
	Tetmesh(unsigned int nverts, unsigned int ntris, unsigned int ntets);
	Tetmesh(std::vector<double> const & verts,
			std::vector<unsigned int> const & tets,
			std::vector<unsigned int> const & tris = std::vector<unsigned int>());
	virtual ~Tetmesh(void);
	
	void setVertex(unsigned int vidx, double x, double y, double z);
	void setTri(unsigned int tidx, unsigned int vidx0,
				unsigned int vidx1, unsigned int vidx2);
	void setTet(unsigned int tidx, unsigned int vidx0, unsigned int vidx1,
				unsigned int vidx2, unsigned int vidx3);
	
	void setup(void);
	
	bool isSetupDone(void) const;
	
	std::vector<double> getVertex(unsigned int vidx) const;
	unsigned int countVertices(void) const;
	
	//steps::tetmesh::TmPatch * getTmPatch(std::string const & id) const;
	std::vector<unsigned int> getTri(unsigned int tidx) const;
	unsigned int countTris(void) const;
	double getTriArea(unsigned int tidx) const;
	std::vector<double> getTriNorm(unsigned int tidx) const;
	steps::tetmesh::TmPatch * getTriPatch(unsigned int tidx) const;
	void setTriPatch(unsigned int tidx, steps::tetmesh::TmPatch * patch);
	std::vector<int> getTriTetNeighb(unsigned int tidx) const;
	
	//steps::tetmesh::TmComp * getTmComp(std::string const & id) const;
	std::vector<unsigned int> getTet(unsigned int tidx) const;
	unsigned int countTets(void) const;
	double getTetVol(unsigned int tidx) const;
	steps::tetmesh::TmComp * getTetComp(unsigned int tidx) const;
	void setTetComp(unsigned int tidx, steps::tetmesh::TmComp * comp);
	std::vector<unsigned int> getTetTriNeighb(unsigned int tidx) const;
	std::vector<int> getTetTetNeighb(unsigned int tidx) const;
	int findTetByPoint(std::vector<double> p) const;
	
	std::vector<double> getBoundMin(void) const;
	std::vector<double> getBoundMax(void) const;
	double getMeshVolume(void) const;
	
};

////////////////////////////////////////////////////////////////////////////////

Tetmesh * loadASCII(std::string pathname);

void saveASCII(std::string pathname, Tetmesh * m);

////////////////////////////////////////////////////////////////////////////////

class Tri	
{
	
public:
	
	Tri(Tetmesh * mesh, unsigned int tidx);
	~Tri(void);
	
	unsigned int getIdx(void);
	double getArea(void) const;
	std::vector<double> getBarycenter(void) const;
	std::vector<double> getNorm(void) const;
	steps::tetmesh::TmPatch * getPatch(void) const;
	
	Tet getTet0(void) const;
    Tet getTet1(void) const;
    Tet getInnerTet(void) const;
    Tet getOuterTet(void) const;
	
    unsigned int getTet0Idx(void) const;
    unsigned int getTet1Idx(void) const;

    unsigned int getInnerTetIdx(void) const;
    unsigned int getOuterTetIdx(void) const;
	
    unsigned int getVertex0Idx(void) const;
    unsigned int getVertex1Idx(void) const;
    unsigned int getVertex2Idx(void) const;
	
};
	
////////////////////////////////////////////////////////////////////////////////

class Tet
{
	
public:
	
	Tet(Tetmesh * mesh, unsigned int tidx);
	~Tet(void);
	
	unsigned int getIdx(void) const;
	double getVol(void) const;
	std::vector<double> getBarycenter(void) const;
	double getQualityRER(void) const;
	steps::tetmesh::TmComp * getComp(void) const;
	
	Tet getTet0(void) const;
    Tet getTet1(void) const;
    Tet getTet2(void) const;
    Tet getTet3(void) const;

	unsigned int getTet0Idx(void) const;
    unsigned int getTet1Idx(void) const;
    unsigned int getTet2Idx(void) const;
    unsigned int getTet3Idx(void) const;
	
    double getTet0Dist(void) const;
    double getTet1Dist(void) const;
    double getTet2Dist(void) const;
    double getTet3Dist(void) const;
	
    Tri getTri0(void) const;
    Tri getTri1(void) const;
    Tri getTri2(void) const;
    Tri getTri3(void) const;
	
    unsigned int getTri0Idx(void) const;
    unsigned int getTri1Idx(void) const;
    unsigned int getTri2Idx(void) const;
    unsigned int getTri3Idx(void) const;

    double getTri0Dist(void) const;
    double getTri1Dist(void) const;
    double getTri2Dist(void) const;
    double getTri3Dist(void) const;
	
    double getTri0Area(void) const;
    double getTri1Area(void) const;
    double getTri2Area(void) const;
    double getTri3Area(void) const;

    unsigned int getVertex0Idx(void) const;
    unsigned int getVertex1Idx(void) const;
    unsigned int getVertex2Idx(void) const;
    unsigned int getVertex3Idx(void) const;
	
	unsigned int getVertex0(void) const;
    unsigned int getVertex1(void) const;
    unsigned int getVertex2(void) const;
    unsigned int getVertex3(void) const;
	
    bool isInside(double * p) const;
	std::vector<double> getRanPnt(steps::rng::RNG * r, unsigned int n = 1) const;

};
	
////////////////////////////////////////////////////////////////////////////////
	
%feature("kwargs") TmComp::TmComp;

class TmComp : public steps::wm::Comp
{
public:
		
	TmComp(std::string const & id, Tetmesh * container, 
		 std::vector<unsigned int> const & tets,
		 steps::model::Volsys * volsys = 0);
	virtual ~TmComp(void);
	
	virtual void setVol(double vol);
	
	std::vector<unsigned int> getAllTetIndices(void) const;
	std::vector<bool> isTetInside(std::vector<unsigned int> tet) const;
	
	std::vector<double> getBoundMin(void) const;
	std::vector<double> getBoundMax(void) const;
	
};

////////////////////////////////////////////////////////////////////////////////

%feature("kwargs") TmPatch::TmPatch;

class TmPatch : public steps::wm::Patch
{
public:
	/*
	TmPatch(std::string const & id, Tetmesh * container,
		  std::vector<unsigned int> const & tris, steps::tetmesh::TmComp * icomp,
		  steps::tetmesh::TmComp * ocomp = 0, steps::model::Surfsys * surfsys = 0);
	*/
	TmPatch(std::string const & id, Tetmesh * container,
			std::vector<unsigned int> const & tris, steps::wm::Comp* icomp,
			steps::wm::Comp* ocomp = 0, steps::model::Surfsys * surfsys = 0);
	virtual ~TmPatch(void);
	
	virtual void setArea(double area);
	
	std::vector<unsigned int> getAllTriIndices(void) const;
	std::vector<bool> isTriInside(std::vector<unsigned int> tet) const;
	
};
		
		
////////////////////////////////////////////////////////////////////////////////

}	// end namespace tetmesh
}	// end namespace steps

// END
	
