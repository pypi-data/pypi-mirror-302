# Akantu Geomechanical Solver

_Python package containing a geomechanical simulator based on the open-source FEM library [Akantu](https://gitlab.com/akantu/akantu)_

[![PyPI version](https://badge.fury.io/py/akantu-geomechanical-solver.svg)](https://badge.fury.io/py/akantu-geomechanical-solver)
[![Project Status](https://img.shields.io/badge/status-under%20development-yellow)](https://gitlab.com/emil.gallyamov/akantu-geomechanical-solver)
[![GitLab License](https://img.shields.io/gitlab/license/emil.gallyamov%2Fakantu-geomechanical-solver)](https://img.shields.io/gitlab/license/emil.gallyamov%2Fakantu-geomechanical-solver)

See the package documentation on [GitLab Pages](https://akantu-geomechanical-solver-emil-gallyamov-1511fed408434e70bb06.gitlab.io/)

# Installation

## Serial

### pip install (Linux-based systems only)

``` bash
pip install akantu-geomechanical-solver[serial] --index-url https://gitlab.com/api/v4/projects/15663046/packages/pypi/simple
```

## Parallel

To use the parallel version of  Akantu for the geomechanical simulator, a Docker image can be pulled and used out of the box, or build Akantu from source.

### Docker image (Linux-based systems and MacOS)

To use the Docker image including a parallel version of the geomechanical solver, follow these steps:

1. Make sure you have Docker installed on your system.
2. Pull the Docker image from the registry using the following command:

```bash
docker pull registry.gitlab.com/emil.gallyamov/akantu-geomechanical-solver/parallel-gms-images:main
```

3. Once the image is pulled, you can run a container using the image with the following command:

```bash
docker run -it registry.gitlab.com/emil.gallyamov/akantu-geomechanical-solver/parallel-gms-images:main /bin/bash
```

This will start a container and give you an interactive bash shell inside it.

4. You can now use the Docker image for your desired purposes.

### Installation with Akantu built from source (Linux-based systems and MacOS)

#### Dependencies

In order to compile Akantu, some libraries are required:

* CMake
* Boost
* LAPACK
* BLAS
* MPI
* Scotch
* MUMPS
* Gmsh

Please note that the compilation from source will only work with a gcc version < 13

**On `.deb` based systems**

```bash
> sudo apt install cmake libboost-devl iblapack-dev libblas-dev zlib1g-dev  gmsh
> sudo apt install libopenmpi-dev openmpi-bin libscotch-dev libmumps-dev
```

#### Building from source

Clone the repository, for instance using

```bash
git clone git@gitlab.com:emil.gallyamov/akantu-geomechanical-solver.git
```

Use the `installation.sh` script to build the parallel version of hydromechanical coupling branch of Akantu used by the geomechanical solver on your machine. This will create an `akantu` subfolder in the `akantu-geomechanical-solver` folder. Once this is done, add three Akantu path to `PYTHONPATH` variable

```bash
export PYTHONPATH="${PYTHONPATH}:${PWD}/akantu/build/python:${PWD}/akantu/test:${PWD}/akantu/test/test_fe_engine"
```

You can then install the parallel version version of the geomechanical solver via pip.

``` bash
pip install .[parallel]
```
