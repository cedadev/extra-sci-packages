# extra-sci-packages
A set of RPM packages to supplement Jaspy to provide an scientific analysis environment for CentOS7


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
