# extra-sci-packages

A set of RPM packages to supplement Jaspy to provide an scientific analysis environment for CentOS7, principally for use on JASMIN.

To use these packages:
```
source /opt/rh/ceda-sci/enable
```


## Removed packages

The following packages which were previously supported under JAP are not provided:

* Any packages provided under Jaspy are not also provided under extra-sci-packages unless it is necessary to do so in order to satisfy a dependency.

* CMOR: Owing to the strong version-dependency, we now advise groups requiring CMOR to maintain their own installations so that they can manage the version they wish to use, because the extra-sci-packages does not allow for multiple co-existing versions. (A version is in fact provided in Jaspy although it does not include the development libraries.)

  * cmip6-cmor-tables: again because of the strong version dependency, we do not want to include a fixed version as an RPM. Master copies can be found [here](https://github.com/PCMDI/cmip6-cmor-tables). (Users should use the branch of relevance, but copy the `CMIP6_CV.json` file from the `master` branch.) For convenience, we hope to provide local copies in versioned directories for JASMIN users.

* The ncBrowse netCDF browser has been discontinued ([website](https://www.nodc.noaa.gov/woce/woce_v3/wocedata_1/utils/netcdf/ncbrowse/index.htm) contains stale download link)

* The EMOS library is marked as deprecated by ECMWF (see note on [website](https://confluence.ecmwf.int//display/EMOS/Emoslib)), as well as the old grib_api interface (see ECMWF's ["end of the road"](https://www.ecmwf.int/en/newsletter/152/news/end-road-grib-api) announcement). The grib_api has been superseded by eccodes, which is provided in Jaspy (and had also been provided in JAP for some time). A version of EMOS _might_ be provided in order to satisfy a dependency from another package, but this should not be relied upon.

* octave-octcdf - the [website](https://octave.sourceforge.io/octcdf/) marks it as obsolete and advises use of the `netcdf` package instead

* thea - the [GitHub repository](https://github.com/SciTools/thea) has been archived and marked as unsupported

* pdftk - this was provided using RPMs supplied by PDF Labs; they have not provided a CentOS 7 version (see [downloads page](https://www.pdflabs.com/docs/install-pdftk-on-redhat-or-centos/))


## Package-specific documentation

### Misr toolkit python bindings

Python bindings are not provided for the Misr toolkit, because this would tie it into a 
particular python installation.  Instead, instructions are provided here for you to
compile your own python wrapper under your directory, for the Python installation that 
you are working with.

The example below assumes that you are working with the default release of Jaspy 2.7.
(Note that when tested, the Python 3.7 equivalent gave an error, so it may be that 
the MTK Python bindings are not supported for Python 3.)

#### Build example

The following commands are typed at the shell prompt.

```
# load ceda-sci tools and Jaspy
source /opt/rh/ceda-sci/enable
module load jaspy/2.7

# create and activate a virtual environment
virtualenv --system-site-packages my_venv
. my_venv/bin/activate

# get the MTK source (matching the installed version) and build the python
# bindings

wget -O Mtk-src-1.4.5.tar.gz https://github.com/nasa/MISR-Toolkit/archive/v1.4.5.tar.gz
tar xvfz Mtk-src-1.4.5.tar.gz
cd MISR-Toolkit-1.4.5/wrappers/python/
export HDFLIB=/usr/lib64/hdf/
export HDFINC=/usr/include/hdf/
export HDFEOS_INC=/opt/rh/ceda-sci/root/usr/include/
export HDFEOS_LIB=/opt/rh/ceda-sci/root/usr/lib64/
ln -s $HDFEOS_LIB/libMisrToolkit.a ../../lib
export CFLAGS=`python-config --cflags`
python setup.py install
```

#### Run-time example

The following commands are typed at the shell prompt, except for the example python session, shown indented.

```
# set up the environment
source /opt/rh/ceda-sci/enable
module load jaspy/2.7
. my_venv/bin/activate

# get some test data
wget https://gamma.hdfgroup.org/ftp/pub/outgoing/NASAHDF/MISR_AM1_CGAL_2017_F06_0024.hdf

# example python session
python

  >>> from MisrToolkit import *
  >>> r = MtkRegion(37, 50, 60)
  >>> r.center
  (44.327741112333754, -108.92382807624027)
  >>> f = MtkFile("MISR_AM1_CGAL_2017_F06_0024.hdf")
  >>> f.grid_list
  ['AlbedoAverage_1_degree', 'AlbedoAverage_5_degree']
```
