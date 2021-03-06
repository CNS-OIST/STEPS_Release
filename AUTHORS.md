The following people have contributed to the development of STEPS

From Okinawa Institute of Science and Technology Graduate University, Japan and University of Antwerp, Belgium:

Erik De Schutter (OIST, UA, since 2006)
* Project conception and supervision

Iain Hepburn (OIST, UA, since 2008)
* Development of STEPS since version 1.0.0: Well-mixed and spatial stochastic and deterministic solver implementation
* Voltage calculation on tetrahedral mesh (EField) implementation
* Serial TetOpSplit development
* SBML support
* Meshio utilities
* Diffusion Boundaries for Tetexact and TetOpSplit
* Contribution to Swig and Cython bindings
* Validation design, testing, and documentation

Weiliang Chen (OIST, since 2009)
* Development of STEPS since version 1.0.0: Well-mixed and spatial stochastic solver development
* Parallel TetOpSplit implementation
* Implementation of visualization toolkit
* Assertion and Exception logging overhaul
* Meshio utilities
* Utilities supports for third-party software (CUBIT/Trelis, Metis, mesh mapping for swc/hoc morphology)
* Testing and documentation

Jules Lallouette (OIST, since 2019)
* Development of the new python API
* Testing and documentation for the new python API

Guido Klingbeil  (OIST, 2015 - 2019)
* Matlab Simbiology support utility

Stefan Wils (OIST, UA, 2006 - 2009)
* Early version implementation (1.0.0): Well-mixed and spatial stochastic solver development
* Meshio utilities
* Documentation


From École polytechnique fédérale de Lausanne, Switzerland (Since STEPS version 3.0.0):

Fabien Delalondre
* Technical lead and coordination for Blue Brain team contribution (to June 2018)

James King
* Technical lead and coordination for Blue Brain team contribution (from July 2018)

Tristan Carel (from June 2017)
* Docker image (https://github.com/CNS-OIST/STEPS_Docker)
* Modernize code base
* Use strong types to distinguish identifiers in the code

Francesco Casalegno
* R123 random number generator
* parallel PETSc EField solver
* python 2/3 compatibility
* new version of manual as jupyter notebooks (https://github.com/CNS-OIST/STEPS_Example/tree/master/user_manual)

Samuel Melchior
* Rejection-based SSA for well mixed solver
* Optimisation of Wmrk4 non-spatial deterministic solver.

Aleksandr Ovcharenko
* R123 random number generator
* Optimization of spatial solver constructors to speedup initialization of simulation with large mesh (3.1.0)

Fernando Pereira
* Cython bindings
* Compilation with CMake

Sam Yates
* Compilation support with CMake
* Unit testing suite implementation
* First implementation of parallel EField solver using direct solvers
* R123 random number generator
* Other code fixes and optimizations

Giacomo Castiglioni (from October 2020)
* Improved CMake structure
* Support for OpenMP and AppleClang
* Code fixes related to segment-tetrahedron intersection


ACKNOWLEDGEMENT

Ivan Raikov (OIST): Configuration of subversion archive and autotools.

Michele Mattioni: Contributed towards the SBML importer.

Mika Holm: STEPS logo.


If you contributed to STEPS and you name is not included here,
please don't hesitate to contact us.

