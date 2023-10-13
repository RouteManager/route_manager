# Route Manager Project

## Description

This project uses the OSMnx library to manage routes for different types of travel (e.g., walking, skating, bicycling). It includes a RouteManager class that retrieves and stores routes, and a FilterManager class that manages filters for different types of routes. The project also includes a Fitness class that calculates the fitness of routes.

## Installation

1. Clone this repository.
2. Create a new Anaconda environment with Python 3.11: `conda create -n route_manager python=3.11`
3. Activate the new environment: `conda activate route_manager`
4. Install the necessary packages, including OSMnx: `conda install -c conda-forge osmnx`
5. Save the conda environment to file: `conda env export --name route_manager --no-builds --from-history > environment.yml`
6. To recreate the conda environment from file: `conda env create -f environment.yml`
7. To create a requirements.txt `pip list --format=freeze > requirements.txt`

NB: Conda installed sqlite3 with Python 3.11 on OSX, but there was some configuration issue with `libsqlite`. Force reinstalling it solved the isse `conda install -c conda-forge libsqlite --force-reinstall`

## Usage

Import and use the RouteManager, FilterManager, and Fitness classes in your code.

## Testing

Unit tests are included in the `tests/` directory.

## License

[Your preferred license]
