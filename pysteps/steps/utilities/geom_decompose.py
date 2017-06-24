####################################################################################
#
#    STEPS - STochastic Engine for Pathway Simulation
#    Copyright (C) 2007-2017 Okinawa Institute of Science and Technology, Japan.
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
###

from numpy import *
import math

################################################################################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

################################################################################

def binTetsByAxis(mesh, nbins, axis = -1):
    """
    Bin tetrahedrons of the mesh along a specific axis.
    
    This function is now deprecated, use linearPartition() instead.
    
    Parameters:
        * mesh                STEPS Tetmesh object
        * nbins               Number of bins along the axis
        * axis                The partioning axis(Option -1: longest axis, 0:x, 1:y, 2:z)
    
    Return:
        Tetrahedron partition list for parallel TetOpsplit solver
    """
    selected_axis = axis
    max_xyz = mesh.getBoundMax()
    min_xyz = mesh.getBoundMin()
    if axis == -1:
        # search for axis that with maximum distance
        dist = array(max_xyz) - array(min_xyz)
        selected_axis = dist.argmax()
    max = max_xyz[selected_axis]
    min = min_xyz[selected_axis]
    spacing = linspace(min, max, nbins + 1)
    centers = [0.0] * mesh.ntets
    for i in range(mesh.ntets):
        baryc = mesh.getTetBarycenter(i)
        centers[i] = baryc[selected_axis]
    belongs = digitize(centers, spacing)
    belongs -= 1
    return belongs

################################################################################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

################################################################################

def linearPartition(mesh, partition_info):
    """
    Partition the mesh based on the partition info. The partition_info is a list [xbin, ybin, zbin]
    where each element is the number of bins for the axis.
    
    Parameters:
        * mesh                STEPS Tetmesh object
        * partition_info      a list [xbin, ybin, zbin] describing the binning requirement of each axis
    
    Return:
        Tetrahedron partition list for parallel TetOpsplit solver
    """
    assert(len(partition_info)==3)
    
    bmax = mesh.getBoundMax()
    bmin = mesh.getBoundMin()
    
    dx = (bmax[0]-bmin[0])/partition_info[0]
    dy = (bmax[1]-bmin[1])/partition_info[1]
    dz = (bmax[2]-bmin[2])/partition_info[2]
    
    part=zeros(mesh.ntets, dtype='int')    
    
    for tet in range(mesh.ntets):
        idx=0
        baryc = mesh.getTetBarycenter(tet)
        
        z= bmin[2]
        zidx=0
        while(zidx<partition_info[2]):
            y = bmin[1]
            yidx=0
            while(yidx<partition_info[1]):
                x=bmin[0]
                xidx=0
                while(xidx<partition_info[0]):
                    if baryc[2] >= z and baryc[2] < z+dz and baryc[1] >= y and baryc[1] < y+dy and baryc[0] >= x and baryc[0] < x+dx:
                        part[tet] = idx
                    x+=dx
                    xidx+=1
                    idx+=1
                y+=dy
                yidx+=1
            z+=dz
            zidx+=1
    
    return list(part)

################################################################################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

################################################################################

def partitionTris(mesh, tet_partitions, tri_list):
    """
    Partition trangles according to partitioning information of their attached tetrahedrons.
        
    Parameters:
        * mesh                STEPS Tetmesh object
        * tet_partitions      List of partioning for each tetrahedron in the mesh, generated by linearPartition function or third-party software
        * tri_list            List of triangles that require partitioning
        
    Return:
        Triangle partition list for parallel TetOpsplit solver
    """
    
    tri_partitions = {}
    for tri in tri_list:
        neigh_tets = mesh.getTriTetNeighb(tri)
        if neigh_tets[0] == -1 and neigh_tets[0] == -1:
            print "Triangle ", tri, " has no attatched tetrahedron, which is unlikely. Please check your mesh.\n"
            continue
        if neigh_tets[0] == -1:
            tri_partitions[tri] = tet_partitions[neigh_tets[1]]
            continue
        if neigh_tets[1] == -1:
            tri_partitions[tri] = tet_partitions[neigh_tets[0]]
            continue
        if tet_partitions[neigh_tets[0]] == tet_partitions[neigh_tets[1]]:
            tri_partitions[tri] = tet_partitions[neigh_tets[0]]
            continue
        print "Neighbor tetrahedrons of triangle ", tri, " are assigned to different hosts, try to rearrange hosts for them.\n"
        tri_partitions[tri] = tet_partitions[neigh_tets[0]]
        tet_partitions[neigh_tets[1]] = tet_partitions[neigh_tets[0]]

    for tri in tri_list:
        neigh_tets = mesh.getTriTetNeighb(tri)
        for neigh_tet in neigh_tets:
            if neigh_tet == -1: continue
            if tet_partitions[neigh_tet] != tri_partitions[tri]:
                raise Exception("Patch triangle %i and its compartment tet are assigned to different processes." % (tri))

    return tri_partitions

################################################################################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

################################################################################

def getTetPartitionTable(partitions):
    """
    Convert a [tet0_host, tet1_host, ...] partitioning list to a {host0:[tet0, tet1, ...], ...} table.
        
    Parameters:
        * partitions          Partitioning list for tetrahedrons in the format of [tet0_host, tet1_host, ...]
        
    Return:
        A dictionary in the format of {host0:[tet0, tet1, ...], ...}
    """
    part_table = {}
    for element in range(len(partitions)):
        if partitions[element] not in part_table.keys():
            part_table[partitions[element]] = []
        part_table[partitions[element]].append(element)
    return part_table

def getTriPartitionTable(partitions):
    """
    Convert a {tri0:tri0_host, tri1:tri1_host, ...} partitioning data to a {host0:[tri0, tri1, ...], ...} table.
        
    Parameters:
        * partitions          Partitioning dictionary for triangles in the format of {tri0:tri0_host, tri1:tri1_host, ...}
        
    Return:
        A dictionary in the format of {host0:[tri0, tri1, ...], ...}
    """
    part_table = {}
    for element in partitions:
        if partitions[element] not in part_table.keys():
            part_table[partitions[element]] = []
        part_table[partitions[element]].append(element)
    return part_table

def validatePartition(mesh, tet_partitions, tri_partitions = {}):
    """
    Validate the partitioning of the mesh.
        
    Parameters:
        * mesh              STEPS Tetmesh object
        * tet_partitions    Partition list for tetrahedrons
        * tri_partitions    Partition list for triangles (Optional)
        
    Return:
        None
    """
    print "Validation starts."
    tet_part_table = {}
    for tet in range(len(tet_partitions)):
        if tet_partitions[tet] not in tet_part_table.keys():
            tet_part_table[tet_partitions[tet]] = []
        tet_part_table[tet_partitions[tet]].append(tet)
    
    tri_part_table = {}
    for tri in tri_partitions:
        if tri_partitions[tri] not in tri_part_table.keys():
            tri_part_table[tri_partitions[tri]] = []
        tri_part_table[tri_partitions[tri]].append(tri)
    
    # validate if elements in each tet partition are connected
    for part in tet_part_table.values():
        for tet in part:
            neighb_tets = mesh.getTetTetNeighb(tet)
            neighb_in_part = False
            for n_tet in neighb_tets:
                if n_tet == -1: continue
                if n_tet in part:
                    neighb_in_part = True
                    break
            if not neighb_in_part:
                print("Tetrahedron %i has no neighbor in its partition. This is unusual but still acceptable." % (tet))

    for tri in tri_partitions:
        neigh_tets = mesh.getTriTetNeighb(tri)
        for neigh_tet in neigh_tets:
            if neigh_tet == -1: continue
            if tet_partitions[neigh_tet] != tri_partitions[tri]:
                raise Exception("Patch triangle %i and its compartment tet are assigned to different processes." % (tri))
    print "Validation completed."

################################################################################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

################################################################################

def printHostDistStat(tet_partitions = [], tri_partitions = {}, wmvol_partitions = []):
    print "Warnning: This function has been renamed to printPartitionStat(tet_partitions, tri_partitions, wmvol_partitions)."

    printPartitionStat(tet_partitions, tri_partitions, wmvol_partitions)

################################################################################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

################################################################################

def printPartitionStat(tet_partitions = [], tri_partitions = {}, wmvol_partitions = [], mesh = None):
    """
    Print out partitioning stastics.
        
    Parameters:
        * tet_partitions    Partition list for tetrahedrons
        * tri_partitions    Partition list for triangles (Optional)
        * wmvol_partitions  Partition list for well-mixed volumes (Optional)
        * mesh              STEPS Tetmesh object (Optional)
        
    Return:
        (If mesh is provided) tet_stats, tri_stats, wm_stats, num_hosts, min_degree, max_degree, mean_degree
        [tet/tri/wm]_stats contains the number of tetrahedrons/triangles/well-mixed volumes in each hosting process, num_hosts provide the number of hosting processes, [min/max/mean]_degree provides the minimum/maximum/average connectivity degree of the partitioning
    """
    tet_stats = []
    for host in tet_partitions:
        if host >= len(tet_stats):
            tet_stats.extend([0] * (host - len(tet_stats) + 1))
        tet_stats[host] += 1

    print "Total number of assigned tets: ", len(tet_partitions)
    if tet_stats != []:
        print "Distribution: ",
        sum = 0
        for h in tet_stats:
            print h,
            sum += h
        print ""
        print "Sum: ", sum

    tri_stats = []
    for tri_id in tri_partitions.keys():
        host = tri_partitions[tri_id]
        if host >= len(tri_stats):
            tri_stats.extend([0] * (host - len(tri_stats) + 1))
        tri_stats[host] += 1

    print "Total number of assigned tris: ", len(tri_partitions)
    if tri_stats != []:
        print "Distribution: ",
        sum = 0
        for h in tri_stats:
            sum += h
            print h,
        print ""
        print "Sum: ", sum

    wm_stats = []
    for host in wmvol_partitions:
        if host >= len(wmvol_partitions):
            wmvol_partitions.extend([0] * (host - len(wmvol_partitions) + 1))
        wmvol_partitions[host] += 1

    print "Total number of assigned well-mixed volumes: ", len(wmvol_partitions)
    if wm_stats != []:
        print "WMVol Distribution: ",
        sum = 0
        for h in wm_stats:
            sum += h
            print h,
        print ""
        print "Sum: ", sum

    if mesh is not None:
        partition_neighbors = {}
        for tet in range(mesh.ntets):
            tet_part = tet_partitions[tet]
            if tet_part not in partition_neighbors.keys():
                partition_neighbors[tet_part] = set()
            neighbor_tets = mesh.getTetTetNeighb(tet)
            for neighb in neighbor_tets:
                if neighb == -1: continue
                neighb_tet_part = tet_partitions[neighb]
                if neighb_tet_part != tet_part:
                    partition_neighbors[tet_part].add(neighb_tet_part)

        host_degrees = []
        for neighbs in partition_neighbors.values():
            host_degrees.append(len(neighbs))
        print "Number of partitions: ", len(tet_stats)
        print "Min Tet Partition Degree: ", min(host_degrees)
        print "Max Tet Partition Degree: ", max(host_degrees)
        print "Mean Tet Partition Degree: ", mean(host_degrees)
        print ""
        return tet_stats, tri_stats, wm_stats, len(tet_stats), min(host_degrees), max(host_degrees), mean(host_degrees)


################################################################################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

################################################################################

def isPointInCylinder(cyl_p0, cyl_p1, test_pnt, scale):
    """
        Check if a point is inside a cylinder in 3D. The cylinder is defined by an axis from
        cyl_p0 to cyl_p1, with length cyl_length and radius cyl_radius.
        
        Arguements:
        * cyl_p0 coordinates of the first end point of the cylinder
        * cyl_p1 coordinates of the second end point of the cylinder
        * cyl_length length of the cylinder
        * cyl_radius radius of the cylinder
        * test_pnt coordinate of the test point
        
        Return:
        -1 if point is outside the cylinder,
        distance squared from cylinder axis if point is inside.
        
        License Info:
        Convert from CylTest_CapsFirst of Greg James - gjames@NVIDIA.com
        http://www.flipcode.com/archives/Fast_Point-In-Cylinder_Test.shtml
        Original Lisc: Free code - no warranty & no money back.  Use it all you want
        """
    
    dx = (cyl_p1[0] - cyl_p0[0]) * scale
    dy = (cyl_p1[1] - cyl_p0[1]) * scale
    dz = (cyl_p1[2] - cyl_p0[2]) * scale
    
    cyl_lengthsq = dx * dx + dy * dy + dz * dz
    
    pdx = test_pnt[0] - cyl_p0[0] * scale
    pdy = test_pnt[1] - cyl_p0[1] * scale
    pdz = test_pnt[2] - cyl_p0[2] * scale
    
    dsq_p0 = pdx * pdx + pdy * pdy + pdz * pdz
    
    pdx1 = test_pnt[0] - cyl_p1[0] * scale
    pdy1 = test_pnt[1] - cyl_p1[1] * scale
    pdz1 = test_pnt[2] - cyl_p1[2] * scale
    
    dsq_p1 = pdx1 * pdx1 + pdy1 * pdy1 + pdz1 * pdz1
    
    dot = pdx * dx + pdy * dy + pdz * dz
    
    #print "dot: ", dot, " lengthsq: ", cyl_lengthsq
    if dot < 0.0 or dot > cyl_lengthsq:
        return -1
    else:
        dsq = (pdx * pdx + pdy * pdy + pdz * pdz) - dot * dot / cyl_lengthsq
        radiussq = (cyl_p0[3] / 2.0 * scale) ** 2
        
        #print "dsq: ", dsq, " radiussq: ", radiussq
        if dsq > radiussq:
            return -1
        else:
            #print "dsq: ", dsq, " dsq_p0: ", dsq_p0, " dsq_p1: ", dsq_p1
            return min(dsq, dsq_p0, dsq_p1)
            #return dsq

################################################################################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

################################################################################
def getCenter(p0, p1, scale):
    """
    Compute the center of p0 and p1, multiply by the scaling factor
    """
    return [(p0[0] + p1[0]) * scale / 2.0, (p0[1] + p1[1]) * scale / 2.0, (p0[2] + p1[2]) * scale / 2.0]


