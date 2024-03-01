%define _name hdfeos2
%define _version 3.0
%define srcname hdf-eos2-%{version}

%{?scl:%scl_package %{_name}}
Name:           %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Summary: HDF-EOS2 libraries
Version: %{_version}
Source0: %{srcname}-src.tar.gz
Release: 2%{dist}
License: UNKNOWN
Group: Scientific support
URL: http://hdfeos.org/software
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Packager: alan.iwi@stfc.ac.uk
BuildRequires: ncompress hdf-devel
Requires: hdf-devel

%description

Description: The HDF-EOS2 is a software library designed built on
HDF4* to support EOS-specific data structures, namely Grid, Point, and
Swath. The new data structures are constructed from standard HDF data
objects, using EOS conventions, through the use of a software
library. A key feature of HDF-EOS files is that instrument-independent
services, such as subsetting by geolocation, can be applied to the
files across a wide variety of data products.

%prep
rm -fr hdfeos
tar xvfz %{SOURCE0}

%build
cd %{srcname}
export CFLAGS="-I/usr/include/hdf -Df2cFortran"
export LDFLAGS="-L/usr/lib64/hdf" 
export F77=gfortran
export FC=gfortran
%configure --with-pic --enable-install-include
make

%install
cd %{srcname}
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT	
# add extra header files - they are needed by the mtk build
cp include/*.h gctp/include/*.h $RPM_BUILD_ROOT/%{_includedir}/

%post
if test `whoami` == root; then
   echo "Running /sbin/ldconfig"
   /sbin/ldconfig
fi

%clean				
#rm -rf $RPM_BUILD_ROOT		

%postun
if test `whoami` == root; then
   echo "Running /sbin/ldconfig"
   /sbin/ldconfig
fi

%files
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.la

%changelog
* Fri Oct  4 2019 Builder <builder@builder.ceda.ac.uk> - 20.%{vmin}-1%{dist}
- bump version and build for CentOS7 / SCL

* Mon Jul 13 2015  <builderdev@builder.jc.rl.ac.uk> - 19.1.00-1.ceda
- update to v19 and compile with Fortran support

* Tue Jan 27 2015  <builderdev@builder.jc.rl.ac.uk> - 
- Initial build.

