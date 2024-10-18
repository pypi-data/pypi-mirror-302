#import phonon_to_json as pj
import sys
print(sys.path)
from phonon_to_json.src import phonon_to_json as pj
import os.path
import filecmp



def test_run():
    r_data = pj.read_file("tests/h-BN")
    w_data = pj.read_to_write(r_data, "h-BN", "h-BN")
    pj.write_file("tests/h-BN",w_data)
    f1 = "tests/h-BN.json"
    f2 = "tests/output.json"
    compare = filecmp.cmp(f1,f2,shallow=False)
    assert os.path.isfile(f1) == True
    assert compare == True



