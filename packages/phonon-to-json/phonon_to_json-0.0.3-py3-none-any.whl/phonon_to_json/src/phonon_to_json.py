import sys
from . import constants
from .lattice import Lattice
import numpy as np
import castep_outputs as co

def read_file(filename):
    """reads .phonon file

    Args:
        filename (str): name of the file (excluding the .phonon extension)

    Returns:
        r_(data) (dict): data extracted from the .phonon file
    """
    r_data = co.parse_single(f"{filename}.phonon", co.parse_phonon_file)
    return r_data

def read_to_write(r_data, name, formula):
    """repackages data from the .phonon file to a .json file compatible with https://henriquemiranda.github.io/phononwebsite/phonon.html

    Args:
        r_data (dict): data read from the .phonon file
        name (str): name of the structure
        formula (str): chemical formula of the structure

    Returns:
        w_data (dict): data to be written to the .json file
    """
    w_data = {}
    # add repetitions to write data
    w_data["repetitions"] = [1,1,1]
    # add number of atoms to write data
    w_data["natoms"] = r_data["ions"]
    # add atom types to write data
    w_data["atom_types"] = r_data["coords"]["spec"]
    # add chemical symbols (unique atom types) to write data
    w_data["chemical_symbols"] = []
    for e in r_data["coords"]["spec"]:
        if e not in w_data["chemical_symbols"]:
            w_data["chemical_symbols"].append(e)
    # add atom numbers and atomic numbers (unique atom numbers) to write data
    w_data["atom_numbers"] = []
    w_data["atomic_numbers"] = []
    for e in r_data["coords"]["spec"]:
        n = constants.periodic_table.index(e) + 1
        if n not in w_data["atomic_numbers"]:
            w_data["atomic_numbers"].append(n)
        w_data["atom_numbers"].append(n)
    # add atom positions in fractional coordinates to write data
    w_data["atom_pos_red"] = []
    for i in range(r_data["ions"]):
        pos = [r_data["coords"]["u"][i],r_data["coords"]["v"][i],r_data["coords"]["w"][i]]
        w_data["atom_pos_red"].append(pos)
    # add lattice to write data
    w_data["lattice"] = r_data["unit_cell"]
    lattice = Lattice(w_data["lattice"][0],w_data["lattice"][1],w_data["lattice"][2])
    # add atom positions in absolute coordinates to write data
    w_data["atom_pos_car"] = []
    for coord in w_data["atom_pos_red"]:
        w_data["atom_pos_car"].append(find_cartesian_coords(coord,w_data["lattice"]))
    # add eigenvectors to write data
    w_data["vectors"] = fix_the_vectors(list(r_data["evecs"]),r_data)
    # add eigenvalues to write data
    w_data["eigenvalues"] = r_data["evals"]
    # add qpoint positions to write data
    w_data["qpoints"] = r_data["qpt_pos"]
    #print(len(w_data["qpoints"]))
    # add distances between qpts to write data
    distances, inbetween_distances = qpoint_separation(w_data["qpoints"], lattice)
    w_data["distances"] = distances
    # add linebreaks to write data
    line_breaks = find_linebreaks(inbetween_distances, r_data["wavevectors"])
    w_data["line_breaks"] = line_breaks
    # add high symmetry qpts to write data
    lattice.find_space_group( w_data["atom_pos_red"], w_data["atom_numbers"])
    high_sym_qpts = find_high_sym_qpoints(lattice, w_data["qpoints"])
    w_data["highsym_qpts"] = high_sym_qpts
    # add name and formula to write data
    w_data["name"] = '"'+name+'"'
    w_data["formula"] = '"'+formula+'"'
    if len(w_data["qpoints"]) == 1:
        w_data = duplicate_qpt(w_data)
    return w_data

def write_file(filename, w_data, pretty=True):
    """writes the data to the .json file

    Args:
        filename (str): name of the .json file (excluding the .json extension)
        w_data (dict): data to be written to the .json file
        pretty (bool, optional): if True, adds whitespace to make the .json file more readable. Defaults to True.
    """
    string = "{\n"
    for key in constants.keywords:
        try:
            varname = f'\t"{key}": '
            data_string = str(w_data[key]).replace(" ","").replace("'",'"').replace("(","[").replace(")","]").replace("`","'")
            if pretty:
                content = make_it_pretty(data_string)   # adds whitespace to make .json more readable, not necessary
            else:
                content = data_string
            string += varname + content + ",\n"
        except:
            pass
    string = string[:len(string)-2]     # removes final comma
    string += "\n}"
    with open (f"{filename}.json","w") as file:
        file.write(string)


def duplicate_qpt(w_data):
    w_data["qpoints"] = w_data["qpoints"] * 2
    w_data["vectors"] = w_data["vectors"] * 2
    w_data["eigenvalues"] = w_data["eigenvalues"] * 2
    w_data["line_breaks"] = [(0,1)]
    w_data["distances"] = [0,0]
    w_data["highsym_qpts"] = w_data["highsym_qpts"] * 2
    return w_data

def find_cartesian_coords(frac, lattice):
    """finds the absolute position of the atoms within the unit cell

    Args:
        frac (arr): fractional coordinate positions of the atoms within the unit cell
        lattice (Lattice): lattice object for the structure

    Returns:
        car_coord (arr): array with absolute positions of atoms
    """
    car_coord = [0,0,0]
    for i in range(3):
        r = list(map(lambda x: x * frac[i], lattice[i]))
        for j in range(len(car_coord)):
            car_coord[j]+=r[j]
    return car_coord 

def find_high_sym_qpoints(lattice, qpts):
    """finds high symmetry qpoints along the qpoint path

    Args:
        lattice (Lattice): lattice object for the structure
        qpts (arr): qpoint positions

    Returns:
        high_sym_qpts (arr): array with letter corresponding to each high symmetry qpoint and the qpoint index at that point
    """
    high_sym_qpts = []
    lattice.find_high_sym_points()
    letters, numbers = lattice.find_high_sym_path(qpts)
    for i in range(len(letters)):
        high_sym_qpts.append([int(numbers[i]), letters[i]])
    return high_sym_qpts

def find_linebreaks(inbetween_distances, num_qpts):
    """finds breaks in the qpoint path by comparing differences in the distances between qpoints

    Args:
        inbetween_distances (arr): the difference in distance between qpoints
        num_qpts (int): number of qpoints

    Returns:
        line_breaks (arr): array of linebreaks
    """
    temp = []
    line_breaks = [(0,-1)]
    for i in range(len(inbetween_distances)-1):
        # is the distance between qpoint 1 and 2 and qpoint 2 and 3 roughly the same?
        temp.append(abs(inbetween_distances[i+1]-inbetween_distances[i])<constants.error)

    for i in range(1,len(temp)):
        if not temp[i-1] and not temp[i]: # distances between neighbouring qpoints not the same -> breakpoint
            tup1 = (line_breaks[-1][0],i)
            tup2 = (i,-1)
            line_breaks[-1] = tup1
            line_breaks.append(tup2)
    tup = (line_breaks[-1][0], num_qpts-1) # fills in the last breakpoint up to the last qpoint
    line_breaks[-1] = tup
    return line_breaks

def qpoint_separation(qpts,lattice):
    """calculates the distance between neighbouring qpoints and the differences in distance

    Args:
        qpts (arr): list of qpoint positions in fractional reciprocal coordinates
        lattice (Lattice): lattice object for the structure

    Returns:
        distances (arr): the cumulative distance between qpoints
        inbetween_distances (arr): the difference in distance between qpoints (not cumulative)
    """
    distances = [0]
    inbetween_distances = []
    for i in range(len(qpts)-1):
        q1 = qpts[i]
        q2 = qpts[i+1]
        # convert from fractional reciprocal coords to absolute reciprocal coords
        q1 = q1[0]*lattice.recip1 + q1[1]*lattice.recip2 + q1[2]*lattice.recip3
        q2 = q2[0]*lattice.recip1 + q2[1]*lattice.recip2 + q2[2]*lattice.recip3
        # displacement vector
        d = [q2[0]-q1[0], q2[1]-q1[1], q2[2]-q1[2]]
        sep = np.linalg.norm(d) # length of displacement vector
        distance = float(sep + distances[-1])
        distances.append(distance)
        inbetween_distances.append(sep)
    return distances, inbetween_distances  

def make_it_pretty(string):
    """adds returns and tabs so the resulting json file is more readable

    Args:
        string (str): content for the json file

    Returns:
        content (str): content for the json file in a more readable format
    """
    content = ""
    for ch in string:
        if ch == "[" or ch == ",":
            content += ch + "\n\t "
        elif ch == "]":
            content += "\n\t" + ch
        else:
            content += ch
    return content

def fix_the_vectors(vectors,r_data):
    """nests the eigenvectors from the .phonon file in the correct number of brackets

    Args:
        vectors (arr): eigenvectors from the .phonon file

    Returns:
        qpt_vectors (arr): qpoint qigenvectors
    """
    qpt_vectors = []        # contains [qpts] branch_vectors
    branch_vectors = []     # one per branch, contains [branches] ion_vectors
    ion_vectors = []        # one per ion, contains [ions] eigenvectors
    for i in range(len(vectors)):
        for j in range(len(vectors[i])):
            vec = []
            for k in range(3):
                vec.append([vectors[i][j][k].real, vectors[i][j][k].imag])
            if len(ion_vectors) < r_data["ions"]:
                ion_vectors.append(vec)
                if len(ion_vectors) == r_data["ions"]:
                    branch_vectors.append(ion_vectors)
                    ion_vectors = []
        qpt_vectors.append(branch_vectors)
        branch_vectors = []
    return qpt_vectors



if __name__ == "__main__":
    filename = sys.argv[1]
    name = sys.argv[2]
    formula = sys.argv[3]

    r_data = read_file(filename)
    w_data = read_to_write(r_data, name, formula)
    write_file(filename, w_data)