import numpy as np
from . import constants
import spglib 


class Lattice:
    def __init__(self,real1,real2,real3):
        self.real1 = np.array(real1)
        self.real2 = np.array(real2)
        self.real3 = np.array(real3)
        self.real = np.array([self.real1,self.real2,self.real3])
        self.real_length = None
        self.real_angle = None
        self.recip1 = None
        self.recip2 = None
        self.recip3 = None
        self.recip = None
        self.lattice_type = None
        self.points = None
        self.generate_reciprocal_lattice()
        self.generate_real_vector_length()
        self.generate_real_vector_angle()

    def __repr__(self):
        string = ""
        if self.lattice_type:
            string += f"lattice type: {self.lattice_type}\n\n"
        string += f"real lattice vectors:\na1 = {self.real1}    length = {self.real_length[0]}\na2 = {self.real2}    length = {self.real_length[1]}\na3 = {self.real3}    length = {self.real_length[2]}\n"
        string +=f"\nreciprocal lattice vectors:\nb1 = {self.recip1}\nb2 = {self.recip2}\nb3 = {self.recip3}"
        return string

    def is_angle_equal(self,angle1, angle2):
        """determines whether two angles are equal, with a small error margin

        Args:
            angle1 (float): angle
            angle2 (float): angle

        Returns:
            (bool): returns True if the angles are the same
        """
        if angle1-constants.error < angle2 and angle1+constants.error > angle2:
            return True
        return False
    
    def is_length_equal(self, length1, length2):
        """determines whether two lengths are equal, with a small error margin

        Args:
            length1 (float): length
            length2 (float): length

        Returns:
            (bool): returns True if the lengths are the same
        """
        if length1-constants.error < length2 and length1+constants.error > length2:
            return True
        return False

    def generate_reciprocal_lattice(self):
        """generates the reciprocal lattice vectors from the real space lattice vectors
        """
        volume = np.dot(self.real1, np.cross(self.real2, self.real3))
        self.recip1 = 2*np.pi*np.cross(self.real2, self.real3)/volume
        self.recip2 = 2*np.pi*np.cross(self.real3, self.real1)/volume
        self.recip3 = 2*np.pi*np.cross(self.real1, self.real2)/volume
        self.recip = np.array([self.recip1,self.recip2,self.recip3])

    def generate_real_vector_length(self):
        """determines the length of the real space lattice vectors
        """
        self.real_length = []
        for vec in self.real:
            length = np.sqrt(np.dot(vec, vec))
            self.real_length.append(length)

    def generate_real_vector_angle(self):
        """determines the angle between pairs of real space lattice vectors
        for vectors a, b, and c and angles alpha, beta, and gamma:
            alpha is the angle between b and c
            beta is the angle between a and c
            gamma is the angle between a and b
        """
        self.real_angle = []
        for i in range(len(self.real)):
            costheta = np.dot(self.real[(i+1)%3], self.real[(i+2)%3])/(self.real_length[(i+1)%3]*self.real_length[(i+2)%3])
            theta = np.arccos(costheta)*180/np.pi
            self.real_angle.append(theta)

    def find_lattice_type(self):
        """
        determines the general type of lattice by comparing lattice vector lengths and angles
        works on conventional unit cell not primitive unit cell
        """
        # either cubic or trigonal
        if self.is_length_equal(self.real_length[0], self.real_length[1]) and self.is_length_equal(self.real_length[0], self.real_length[2]):
            if self.is_angle_equal(self.real_angle[0],90) and self.is_angle_equal(self.real_angle[1],90) and self.is_angle_equal(self.real_angle[2],90):
                self.lattice_type = "cubic"
            else:
                self.lattice_type = "trigonal-h"
        # either hexagonal or tetragonal
        elif self.is_length_equal(self.real_length[0], self.real_length[1]) and not self.is_length_equal(self.real_length[0], self.real_length[2]):
            if self.is_angle_equal(self.real_angle[0],90) and self.is_angle_equal(self.real_angle[1],90) and self.is_angle_equal(self.real_angle[2],90):
                self.lattice_type = "tetragonal"
            else:
                self.lattice_type = "hexagonal"
        # either triclinic or monoclinic or orthorhombic
        else:
            if self.is_angle_equal(self.real_angle[0],90) and self.is_angle_equal(self.real_angle[1],90) and self.is_angle_equal(self.real_angle[2],90):
                self.lattice_type = "orthorhombic"
            elif self.is_angle_equal(self.real_angle[0],90) and not self.is_angle_equal(self.real_angle[1],90) and self.is_angle_equal(self.real_angle[2],90):
                self.lattice_type = "monoclinic"
            else:
                self.lattice_type = "triclinic"

    def find_space_group(self, frac_coords, atom_numbers):
        """finds space group of lattice

        Args:
            frac_coords (arr): fractional coordinate positions of atoms in the unit cell
            atom_numbers (arr): atomic numbers for each atom in the unit cell
        """
        positions = frac_coords
        numbers = atom_numbers
        cell = (self.real,positions,numbers)
        group = spglib.get_spacegroup(cell) 
        group = int(group.split()[1].replace("(","").replace(")",""))
        if group >= 1 and group <= 2:
            self.lattice_type = "triclinic"
        elif group >= 3 and group <= 15:
            #mp = [3,4,6,7,10,11,13,14]
            #ms = [5,8,9,12,15]
            #if group in mp:
            #    return "monoclinic-p"
            #elif group in ms:
            #    return "monoclinic-s"
            self.lattice_type = "monoclinic"
        elif group >= 16 and group <= 74:
            self.lattice_type = "orthorhombic"
        elif group >= 75 and group <= 142:
            self.lattice_type = "tetragonal"
        elif group >= 143 and group <= 167:
            self.lattice_type = "trigonal"
        elif group >= 168 and group <= 194:
            self.lattice_type = "hexagonal"
        elif group >= 195 and group <= 230:
            sc = [195,198,200,201,205,207,208,212,213,215,218,221,222,223,224]
            fcc = [196,202,203,209,210,216,219,225,226,227,228]
            bcc = [197,199,204,206,211,214,217,220,229,230]
            if group in sc:
                self.lattice_type = "sc"
            elif group in fcc:
                self.lattice_type = "fcc"
            elif group in bcc:
                self.lattice_type = "bcc"  
            
    def find_high_sym_points(self):
        """finds high symmetry qpoints based on the type of lattice
        """
        points = {}
        points["\\Gamma"] = [[0,0,0]]
        # coordinates are fractional coordinates of reciprocal lattice vectors if 1 unit = 24 
        # (blame dispersion.pl, it works so I'm not fixing it)
        magic_number = 24   
        if self.lattice_type == "sc":
            points["X"] = [[12,0,0],[0,0,12],[0,12,0]]
            points["M"] = [[12,12,0],[12,0,12],[0,12,12]]
            points["R"] = [[12,12,12]]
        elif self.lattice_type == "fcc":
            points["X"] = [[12,12,0],[12,0,12],[0,12,12]]
            points["W"] = [[12,18,6],[18,6,12],[6,12,18],[12,6,18],[6,18,12],[18,12,6]]
            points["K"] = [[9,15,0],[9,0,15],[0,9,15],[15,9,0],[15,0,9],[0,15,9],
                           [15,15,6],[15,6,15],[6,15,15],[9,9,18],[9,18,9],[18,9,9]]
            points["L"] = [[12,12,12]]
        elif self.lattice_type == "fcc afm":
            points["X"] = [[12,12,0],[12,0,12],[0,12,12]]
            points["L"] = [[12,0,0],[0,12,0],[0,0,12]]
            points["T"] = [[12,12,12]]
        elif self.lattice_type == "bcc":
            points["P"] = [[18,18,18],[6,6,6]]
            points["N"] = [[12,12,0],[12,0,12],[0,12,12],[12,0,0],[0,0,12],[0,12,0]]
            points["H"] = [[12,12,12]]
        elif self.lattice_type == "tetragonal":
            points["X"] = [[12,0,0],[0,12,0]]
            points["Z"] = [[0,0,12]]
            points["M"] = [[12,12,0]]
            points["R"] = [[12,0,12],[0,12,12]]
            points["A"] = [[12,12,12]]
        elif self.lattice_type == "tetragonal-i":
            points["X"] = [[12,12,0],[0,0,12]]
            points["N"] = [[12,0,0],[0,12,0],[12,0,12],[0,12,12]]
            points["P"] = [[6,6,6],[18,18,18]]
            points["K.6"] = [[7,7,17]]
            points["K.9"] = [[17,17,7]]
            points["M"] = [[12,12,12]]
        elif self.lattice_type == "orthorhombic":
            points["X"] = [[12,0,0]]
            points["Y"] = [[0,12,0]]
            points["Z"] = [[0,0,12]]
            points["S"] = [[12,12,0]]
            points["U"] = [[12,0,12]]
            points["T"] = [[0,12,12]]
            points["R"] = [[12,12,12]]
        elif self.lattice_type == "hexagonal":
            points["M"] = [[12,12,0],[12,0,0],[0,12,0]]
            points["L"] = [[12,12,12],[12,0,12],[0,12,12]]
            points["K"] = [[8,8,0],[16,16,0]]
            points["H"] = [[8,8,12],[16,16,12]]
            points["A"] = [[0,0,12]]
        elif self.lattice_type == "hexagonal60":
            points["M"] = [[12,12,0],[12,0,0],[0,12,0]]
            points["L"] = [[12,12,12],[12,0,12],[0,12,12]]
            points["K"] = [[16,8,0],[8,16,0]]
            points["H"] = [[16,8,12],[8,16,12]]
            points["A"] = [[0,0,12]]
        elif self.lattice_type == "trigonal":
            points["Z"] = [[12,12,12]]
            points["L"] = [[12,0,0],[0,12,0],[0,0,12]]
            points["F"] = [[12,12,0],[0,12,12],[12,0,12]]
        elif self.lattice_type == "trigonal-h":
            points["K"] = [[16,16,16]]
            points["M"] = [[12,12,0],[0,12,12],[12,0,12]]
            points["A"] = [[12,12,12]]

        # TODO - include triclinic and monoclinic bravais lattices
        # https://www.materialscloud.org/work/tools/seekpath

        self.points = points

    def reciprocal_vector(self,vector):
        r = np.linalg.solve(self.recip,vector)
        return r
    
    def is_high_sym(self,qp, points):
        """compares a qpoint with the list of high symmetry qpoints

        Args:
            qp (arr): qpoint position
            points (arr): array of high symmetry qpoints

        Returns:
            (bool): True if qpoint is high symmetry, False otherwise
            (arr or None): qpoint position if qpoint is high symmetry, None otherwise
        """
        for p in points:
            if qp[0]>p[0]-constants.error and qp[0]<p[0]+constants.error and qp[1]>p[1]-constants.error and qp[1]<p[1]+constants.error and qp[2]>p[2]-constants.error and qp[2]<p[2]+constants.error:
                return True, p
        return False, None
    
    def find_high_sym_path(self, qpoints):
        """finds the high symmetry path

        Args:
            qpoints (arr): array of qpoint positions

        Returns:
            letters (arr): array of high symmetry labels
            numbers (arr): array of high symmetry qpoint indecies
        """
        high_sym_points = list(self.points.values())
        keys = list(self.points.keys())
        points = []
        letters = []
        numbers = []
        for h in high_sym_points:
            for p in h:
                points.append(p)
        for i in range(len(qpoints)):
            q24 = list(map(lambda x: x*24, qpoints[i]))
            high_sym, point = self.is_high_sym(q24,points)
            if high_sym:
                for k in keys:
                    if point in self.points[k]:
                        if k in letters and k != "\\Gamma":
                            k += "`"
                        letters.append(k)
                        numbers.append(i)
        return letters, numbers