%define _name mtk

%{?scl:%scl_package %{_name}}
Name: %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Summary: MISR Toolkit
Version: 1.5.1
Release: 1%{dist}
License: MISR Toolkit License http://www.openchannelfoundation.org/project/print_license.php?group_id=354&license_id=31
Group: Scientific support
URL: https://eosweb.larc.nasa.gov/project/misr/tools/misr_toolkit
Source0: Mtk-src-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: libjpeg-turbo
Requires: zlib
Requires: hdf
Requires: %{?scl:%{scl_prefix}}hdfeos2
BuildRequires: hdf-devel zlib-devel libjpeg-turbo-devel
BuildRequires: %{?scl:%{scl_prefix}}hdfeos2
Packager: alan.iwi@stfc.ac.uk

# add explicit provides line because autodeps notices that the shared library is required
# but when using SCL, does not notice that it is also provided
Provides: libMisrToolkit.so()(64bit)


%description

Welcome to the MISR Toolkit
---------------------------

The MISR Toolkit is a simplified programming interface to access MISR L1B2, L2
conventional and ancillary data products. It is an interface built upon HDF-EOS
that knows about MISR data products. It has the ability to:

   - Specify regions to read based on geographic location and extent or the
     more traditional path and block range
   - Map between path, orbit, block, time range and geographic location
   - Automatically stitch, unpack and unscale MISR data while reading
   - Perform coordinate conversions between lat/lon, SOM x/y, block/line/sample
     and line/sample of a data plane, which means geolocation can be computed
     instantly without referring to an ancillary data set lookups
   - Retrieve pixel acquistion time from L1B2 product files
   - Read a slice of a multi-dimensional field into an 2-D data plane (eg. RetrAppMask[0][5])
   - Convert MISR product files to IDL ENVI files

The MISR Toolkit has been tested on Linux Fedora Core 19
or later, Mac OS X 10.6.8 or later (Intel) and Windows 32-bit XP. It's core interface is C. 
There are also bindings for Python and IDL. 


Complete documentation and function reference
---------------------------------------------

Use a browser to view online documentation: https://nasa.github.io/MISR-Toolkit/html/index.html


%package devel
Group: Development/Libraries	
Summary: Development libraries for Mtk.
Requires: %{?scl:%{scl_prefix}}hdfeos2, hdf-devel, zlib-devel, libjpeg-turbo-devel
Requires: %{name} = %{version}
%description devel
This package contains the development libraries for the MISR toolkit.
For further information see the description for the mtk (non-devel) package.

%prep
%setup -n MISR-Toolkit-%{version}
#%patch0 -p0
#%patch1 -p0

%build

%define installprefix $RPM_BUILD_ROOT/usr
%define docdir /usr/share/doc/mtk-%{version}

export HDFEOS_INC=%{?scl:%{_scl_root}}/usr/include
export HDFEOS_LIB=%{?scl:%{_scl_root}}/usr/lib64/
export HDFLIB=/usr/lib64/hdf/
export HDFINC=/usr/include/hdf/

# unfortunately will not build with -Werror - remove this flag
find . -name Makefile | xargs perl -p -i -e 's/-Werror\s/ /g'

make

%install

export MTK_INSTALLDIR=$RPM_BUILD_ROOT%{?scl:%{_scl_root}}/usr

rm -rf $RPM_BUILD_ROOT
make install
perl -p -i -e "s,$RPM_BUILD_ROOT,," $MTK_INSTALLDIR/bin/Mtk_{c,python}_env.{sh,csh}
mkdir -p $RPM_BUILD_ROOT/`dirname %{_docdir}`
mv $MTK_INSTALLDIR/doc $RPM_BUILD_ROOT%{_docdir}
mv $MTK_INSTALLDIR/examples $RPM_BUILD_ROOT%{_docdir}/examples
mv $MTK_INSTALLDIR/lib $RPM_BUILD_ROOT%{_libdir}

# in the examples/python directory, the scripts are python2, so rename
# *.py to *.py2 to prevent rpmbuild from trying to byte-compile them
# and then aborting the build when it fails (the RPM macros I found
# online that allegedly prevent byte-compiling, or that prevent
# failures from terminating the build, didn't seem to work)
cd $RPM_BUILD_ROOT%{_docdir}/examples/python/
for f in *.py ; do mv $f ${f}2; done

%clean
rm -rf $RPM_BUILD_ROOT




%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%doc %{_datadir}/doc/*

%files devel
%{_includedir}/*
%{_libdir}/*.a

%changelog

* Fri Mar 1 2024 alan.iwi@stfc.ac.uk - 1.5.1-1%{dist}
- Rocky 9 version

* Fri Oct  4 2019 Builder <builder@builder.ceda.ac.uk> - 1.4.5-1%{dist}
- bump version and build for CentOS7/SCL, omitting python wrappers

* Tue Jan 27 2015  <builderdev@builder.jc.rl.ac.uk> - 
- Initial build.
