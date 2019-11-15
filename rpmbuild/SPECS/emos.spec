%define _name libemos

%{?scl:%scl_package %{_name}}
Name: %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Version: 4.5.9
Release: 1%{?dist}
License: LGPL 3.0
Group: Scientific support	
Source0: %{_name}-%{version}-Source.tar.gz
Buildroot: %{_tmppath}/%{_name}-%{version}-%{release}-root
BuildRequires: gcc, gcc-gfortran cmake eccodes-devel
Requires: eccodes
Url: https://confluence.ecmwf.int/display/EMOS/
Summary: EMOSLIB interpolation software from ECMWF


%description					
The EMOS library from ECMWF (32 and 64 bit versions).

%prep

%setup0 -q -n %{_name}-%{version}-Source

%build

%define install_dir %{?scl:%{_scl_root}}/usr

mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=%{install_dir}
make

%install			

rm -rf $RPM_BUILD_ROOT		
cd build
make install DESTDIR=$RPM_BUILD_ROOT


%clean				
rm -rf $RPM_BUILD_ROOT

%files				
%defattr(-,root,root)			
%{install_dir}/lib/libemos*
%{install_dir}/lib/pkgconfig/libemos*
%{install_dir}/bin/*
%{install_dir}/include/libemos
%{install_dir}/share/libemos

%changelog

* Fri Oct  4 2019 Builder <builder@builder.ceda.ac.uk> - 4.5.9-1
- total revamp of spec file; much later (although deprecated) package, and build for CentOS7/SCL

* Thu Jan 17 2013  <builderdev@builder.jc.rl.ac.uk> - 000382-2.ceda
- -fPIC

* Thu Jan  3 2013 Alan Iwi
alan.iwi@stfc.ac.uk 20130102
- Created initial RPM
