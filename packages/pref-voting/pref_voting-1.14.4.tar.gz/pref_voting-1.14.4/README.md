pref_voting
==========

## Installation

The package can be installed using the ``pip3`` package manager:

```bash
pip3 install pref_voting
```

Note: If you have both Python 2 and Python 3 installed on your system, make sure to use ``pip3`` instead of pip to install packages for Python 3. Alternatively, you can use ``python3 -m pip`` to ensure you're using the correct version of pip. If you have modified your system's defaults or soft links, adjust accordingly.


## Documentation

Online documentation is available at [https://pref-voting.readthedocs.io](https://pref-voting.readthedocs.io).

## Example Usage

A profile (of linear orders over the candidates) is created by initializing a `Profile` class object.  Simply provide a list of rankings (each ranking is a tuple of numbers) and a list giving the number of voters with each ranking:

```python
from pref_voting.profiles import Profile

rankings = [
    (0, 1, 2, 3), # candidate 0 is ranked first, candidate 1 is ranked second, candidate 2 is ranked 3rd, and candidate 3 is ranked last.
    (2, 3, 1, 0), 
    (3, 1, 2, 0), 
    (1, 2, 0, 3), 
    (1, 3, 2, 0)]

rcounts = [5, 3, 2, 4, 3] # 5 voters submitted the first ranking ((0, 1, 2, 3)), 3 voters submitted the second ranking, and so on.

prof = Profile(rankings, rcounts=rcounts)

prof.display() # display the profile
```

The function `generate_profile` is used to generate a profile for a given number of candidates and voters:  

```python
from pref_voting.generate_profiles import generate_profile

# generate a profile using the Impartial Culture probability model
prof = generate_profile(3, 4) # prof is a Profile object with 3 candidates and 4 voters

# generate a profile using the Impartial Anonymous Culture probability model
prof = generate_profile(3, 4, probmod = "IAC") # prof is a Profile object with 3 candidates and 4 voters 
```

To use one of the many voting methods, import the function from `pref_voting.voting_methods` and apply it to the profile: 

```python
from pref_voting.generate_profiles import generate_profile
from pref_voting.voting_methods import *

prof = generate_profile(3, 4) # create a profile with 3 candidates and 4 voters
split_cycle(prof) # returns the sorted list of winning candidates
split_cycle.display(prof) # display the winning candidates

```

Consult the documentation [https://pref-voting.readthedocs.io](https://pref-voting.readthedocs.io) for a complete overview of the package. 

## Testing
 
To ensure that the package is working correctly, you can run the test suite using [pytest](https://docs.pytest.org/en/stable/). The test files are located in the `tests` directory. Follow the instructions below based on your setup.

### Prerequisites

- **Python 3.8 or higher**: Ensure you have a compatible version of Python installed.
- **`pytest`**: Install `pytest` if it's not already installed.

### Running the tests

If you are using **Poetry** to manage your dependencies, run the tests with:

```bash
poetry run pytest

```
 
From the command line, run:

```bash
pytest
```

For more detailed output, add the -v or --verbose flag:

```bash
pytest -v
```

## Questions?

Feel free to [send an email](https://pacuit.org/) if you have questions about the project.

## License

[MIT](https://github.com/jontingvold/pyrankvote/blob/master/LICENSE.txt)
