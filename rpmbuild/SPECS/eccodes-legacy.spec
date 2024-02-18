%define _pname eccodes2_27
%define _name eccodes

%{?scl:%scl_package %{_pname}}
Name: %{?scl_pkg_name}%{?!scl_pkg_name:%{_pname}}
Version: 2.27.1
Release: 1%{?dist}
License: Apache
Group: Scientific support	
Source0: %{_name}-%{version}-Source.tar.gz
Buildroot: %{_tmppath}/%{_name}-%{version}-%{release}-root
BuildRequires: gcc, gcc-gfortran cmake
Url: https://confluence.ecmwf.int/display/ECC/
Summary: ECCODES Grib access software from ECMWF, legacy version

%description					
This is a legacy version (2.27.1) of ECCODES, which is needed to compile libemos.
Libemos is no longer under development, but is needed by legacy UM utils
package that may still be of use to JASMIN users.

It is recommended instead to link to current eccodes package for other apps.


%package devel
Summary: devel libs for %{name}
Requires: %{name} == %{version}-%{release}

%description devel
Header files and libraries for %{name}.
See description of %{name} for further details.

%package data
Summary: data for %{name}
BuildArch: noarch

%description data
Data files for %{name}
See description of %{name} for further details.

%prep

%setup0 -q -n %{_name}-%{version}-Source

%build

%define install_dir %{?scl:%{_scl_root}}/opt/eccodes%{version}

mkdir build
cd build

cmake .. -D CMAKE_INSTALL_PREFIX=%{install_dir}
make

%install			

rm -rf $RPM_BUILD_ROOT		
cd build
make install DESTDIR=$RPM_BUILD_ROOT


%clean				
rm -rf $RPM_BUILD_ROOT

%files				
%defattr(-,root,root)			
%{install_dir}/lib64/libeccodes*
%{install_dir}/bin/*
%{install_dir}/include/eccodes*
%{install_dir}/include/grib_api*

%files devel
%{install_dir}/lib64/pkgconfig/eccodes*
%{install_dir}/lib64/cmake/eccodes

%files data
%{install_dir}/share/eccodes


%changelog

* Sun Feb 18 2024 Alan Iwi alan.iwi@stfc.ac.uk 
- Created initial RPM
