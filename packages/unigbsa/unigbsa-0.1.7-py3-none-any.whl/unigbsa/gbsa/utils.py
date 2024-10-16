import os
from unigbsa.settings import GMXEXE
def set_amber_home(proc):
    """
    Find the directory containing the executable for a command
  
    Args:
      proc: The name of the executable to find.
  
    Returns:
      the path to the amber home directory.
    """
    cmd = 'which %s '%proc
    f = os.popen(cmd)
    text = f.read().strip()
    if not text:
        raise Exception("Command not found: %s "%proc)
    bindir = os.path.split(text)[0]
    amberhome = os.path.split(bindir)[0]
    return amberhome


def obtain_num_of_frame(trajfile):
    """
    Get the number of frames in a trajectory file

    Args:
      trajfile: the trajectory file, in .xtc or .trr format.

    Returns:
      the number of frames in the trajectory file.
    """
    cmd = '%s check -f %s 2>&1 |grep Coords'% (GMXEXE, trajfile)
    fr = os.popen(cmd)
    text = fr.read().strip()
    if not text:
        print(cmd)
        raise Exception("ERROR obtain %s's frame number.")
    nframe = int(text.split()[1])
    return nframe


def mapping_resname(pdbfile, complexfile):
    reskey0 = ["L::MOL:1"]
    records = ('ATOM', 'HETATOM')
    prev_reskey = None
    with open(pdbfile) as fr:
        for line in fr:
            if line.startswith(records):
                resname = line[17:20].strip()
                resid = line[22:27].strip()
                chainID = line[21].strip()
                key = f'R:{chainID}:{resname}:{resid}'
                if key != prev_reskey:
                    reskey0.append(key)
                prev_reskey = key

    reskeydic = {}
    index = 0
    prev_reskey = None
    with open(complexfile) as fr:
        for line in fr:
            if line.startswith(records):
                resname = line[17:20].strip()
                resid = line[22:27].strip()
                chainID = line[21].strip()
                key = f'R:{chainID}:{resname}:{resid}'
                if key != prev_reskey:
                    reskeydic[key] = reskey0[index]
                    index += 1
                    prev_reskey = key
                if index >= len(reskey0):
                    break
    return reskeydic
