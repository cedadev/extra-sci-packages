%define _name libcrayutil

%{?scl:%scl_package %{_name}}
Name:           %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Version: 20121128
Release: 3%{?dist}
License: NCAS
Group: Scientific support	
Source: libcrayutil-%{version}.tar.gz
Buildroot: %{_tmppath}/%{_name}-%{version}-%{release}-root	
BuildRequires: gcc, gcc-gfortran
Summary: a Cray-compatibility utility library for building UM-related utilities

# something more specific to call "util", as this is going into a 
# system path
# (no longer true for SCL build but keep it anyway)
%define util crayutil

%description					
A Cray-compatibility utility library used for building Unified Model
related utilities (such as ff2pp).  Built from source code taken from
Jeff Cole's directory (~jeff/software/util) on the Reading Meteorology 
systems.

Note that in this package the library is installed as "%{util}" 
rather than just "util" (i.e. use #include <%{util}.h>, and -l%{util}).

%prep

%setup -n util

%build				
make -f Makefile_linux_64_gnu UTILLIB=lib%{util}.a
rm -f *.o
make -f Makefile_linux_64_gnu_R8 UTILLIB=lib%{util}R8.a
rm -f *.o
make -f Makefile_linux_64_gnu_RI8 UTILLIB=lib%{util}RI8.a

%install			

rm -rf $RPM_BUILD_ROOT		
dir=$RPM_BUILD_ROOT/%{_libdir}
mkdir -p $dir
cp *.a $dir/
dir=$RPM_BUILD_ROOT/%{_includedir}
mkdir -p $dir
cp util.h $dir/%{util}.h
cp crayio.h $dir/

%clean				
rm -rf $RPM_BUILD_ROOT		

%files				

%defattr(0644,root,root)			
%{_libdir}/lib%{util}.a
%{_libdir}/lib%{util}R8.a
%{_libdir}/lib%{util}RI8.a
%{_includedir}/crayio.h
%{_includedir}/%{util}.h

%changelog
* Fri Oct  4 2019 Builder <builder@builder.ceda.ac.uk> - 20121128-3
- CentOS7 / SCL build

* Wed Jan  2 2013  <builderdev@builder.jc.rl.ac.uk> - 20121128-2.ceda
- added include files, R8 and RI8, and changed "util" to "crayutil" in filenames
- renamed package to libcrayutil

* Wed Nov 28 2012 Alan Iwi
alan.iwi@stfc.ac.uk 20121128
- Created initial RPM
