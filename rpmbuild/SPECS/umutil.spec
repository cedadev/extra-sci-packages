%define _name umutil

%{?scl:%scl_package %{_name}}
Name: %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Version: 20130102
Release: 4%{?dist}
License: NCAS
Group: Scientific support	
Source0: umutil-%{version}-pruned.tar.gz
Source1: umutil-Makefile_Linux_x86_64
Patch1: umutil-pp2drs-col72.patch
Patch2: umutil-check-types.patch
Patch3: umutil-lsm-icopy.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root	
			#used with non-root builds of RPM files
BuildRequires: gcc, gcc-gfortran,zlib-devel,netcdf-fortran-devel,hdf5-devel
BuildRequires: %{?scl:%{scl_prefix}}libemos,%{?scl:%{scl_prefix}}libdrs,%{?scl:%{scl_prefix}}libcrayutil
Requires: %{?scl:%{scl_prefix}}libemos, libgfortran, netcdf-fortran
Summary: Various utilities related to the Unified Model


%description					
Various utilities related to the Unified Model

This package is compiled from a snapshot of the source code taken from
Jeff Cole's directory (~jeff/um/umutil) on the Reading Meteorology 
systems.

%package lib
Group: Development/Libraries
Summary: Development libraries for compiling UM utilities
Requires: %{?scl:%{scl_prefix}}libcrayutil
%description lib
This package contains the libraries needed to build UM utilities such as xconv.

%define mymakefile Makefile_Linux_x86_64_new

%prep

%setup0 -n %{_name}-%{version}
cp %{SOURCE1} %{mymakefile}
%patch1 -p1
%patch2 -p1
%patch3 -p1
perl -p -i -e 's/#include "util.h"/#include "crayutil.h"/' *.c
mv umtrunc.f umtrunc.F

perl -p -i -l -e '$_ .= " \$\(EXTRA_CPPFLAGS\)" if /^CPPFLAGS=/' Makefile_lib_linux_x86_64

%build

%define scl_usr %{?scl:%{_scl_root}}/usr
%define scl_inc %{scl_usr}/include
%define scl_lib %{scl_usr}/lib

%define makevars DRSINC=%{scl_inc} UTILINC=%{scl_inc} UTILLIB="-L%{_libdir} -lcrayutil" DRSLIB="-L%{_libdir} -ldrs" UNPACKLIB="-L%{scl_lib} -lemos"

ln -s /usr/include/netcdf.inc ./
make -f Makefile_lib_linux_x86_64 UMUTILLIB=libumutil.a EXTRA_CPPFLAGS="-I%{scl_inc}"
make -f %{mymakefile} %{makevars}
make -f %{mymakefile} test %{makevars}

%install			

rm -rf $RPM_BUILD_ROOT		

dir=$RPM_BUILD_ROOT/%{_libdir}
mkdir -p $dir
install -m 644 libumutil.a $dir

make -f %{mymakefile} install %{makevars} INSTALLDIR=$RPM_BUILD_ROOT/%{_bindir}

%clean				
rm -rf $RPM_BUILD_ROOT

%files				
%{_bindir}/*

%defattr(-,root,root)

%files lib
%{_libdir}/libumutil.a

%changelog
* Fri Oct  4 2019 Builder <builder@builder.ceda.ac.uk> - 20130102-4.
- CentOS7 / SCL build

* Mon Sep 25 2017  <builderdev@builder.jc.rl.ac.uk> - 20130102-3.ceda
- compile against later hdf5/netcdf

* Thu Apr  7 2016  <builderdev@builder.jc.rl.ac.uk> - 20130102-1.ceda
- rebuild against later netcdf

* Tue Jan 13 2013 Alan Iwi
alan.iwi@stfc.ac.uk 20130102
- Created initial RPM
