# phonon-to-json
Converts [CASTEP](http://www.castep.org/) .phonon files into .json files readable by [TSS Physics Phonon Visualiser](https://henriquemiranda.github.io/phononwebsite/phonon.html).

# Install
To install ```phonon-to-json``` run:
```
pip install phonon-to-json
```
# Dependencies
```phonon-to-json``` requires 
- [```castep-outputs```](https://pypi.org/project/castep-outputs/)
- [```spglib```](https://pypi.org/project/spglib/)
- ```numpy```

# Command line
```phonon-to-json``` is designed to be run as a command line tool. To run:
```
phonon_to_json [filename] [name] [formula]
```
- ```[filename]``` is the name of the .phonon file (excluding the .phonon extension)
- ```[name]``` is the name of the compound, as displayed at the top of the [website](https://henriquemiranda.github.io/phononwebsite/phonon.html)
- ```[formula]``` is the chemical formula of the compound

```[name]``` and ```[formula]``` are optional, if ommited ```[filename]``` will be used
# As a module
To use ```phonon-to-json``` as a module import ```json_dumper```:
```
import phonon_to_json as pj

filename = "[filename]"
name = "[name]"
formula = "[formula]"

r_data = pj.read_file(filename)
w_data = pj.read_to_write(r_data, name, formula)
pj.write_file(filename, w_data)
``` 