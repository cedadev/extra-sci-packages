%define _name libdrs

%{?scl:%scl_package %{_name}}
Name: %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Version: 3.1.2
Release: 1%{?dist}
License: check with PCMDI
Group: Scientific support	
Source: %{_name}-%{version}.tar.gz
Buildroot: %{_tmppath}/%{_name}-%{version}-%{release}-root	
			#used with non-root builds of RPM files
BuildRequires: gcc, gcc-gfortran
Summary: Data Retrieval and Storage System library

%description					
The PCI Data Retrieval and Storage library developed at PCMDI.

%prep

%setup -n %{_name}-%{version}

%build

cd lib
perl -p -i -l -e '$_ .= " \$\(EXTRA_FFLAGS\)" if /^FFLAGS = /' Makefile.LINUX.gfortran

fflagsr8="-fdefault-real-8"
fflagsri8="$fflagsr8 -fdefault-integer-8"

rm -f *.o
make -f Makefile.LINUX.gfortran EXTRA_FFLAGS="$fflagsr8"
mv libdrs.a libdrsR8.a

rm -f *.o
make -f Makefile.LINUX.gfortran EXTRA_FFLAGS="$fflagsri8"
mv libdrs.a libdrsRI8.a

rm -f *.o
make -f Makefile.LINUX.gfortran

rm -f *.o


%install			

cd lib
rm -rf $RPM_BUILD_ROOT		

dir=$RPM_BUILD_ROOT/%{_libdir}
mkdir -p $dir
install -m 644 *.a $dir

dir=$RPM_BUILD_ROOT/%{_includedir}
mkdir -p $dir
install -m 644 drsdef.h $dir
install -m 644 drscdf.h $dir/drs_cdf.h


%clean				
rm -rf $RPM_BUILD_ROOT

%files				

%defattr(0644,root,root)			
%{_libdir}/libdrs.a
%{_libdir}/libdrsR8.a
%{_libdir}/libdrsRI8.a
%{_includedir}/drs_cdf.h
%{_includedir}/drsdef.h

%changelog

* Fri Oct  4 2019 Builder <builder@builder.ceda.ac.uk> - 3.1.2-1
- change to use official source from github, change build commands, and use CentOS7/SCL

* Thu Apr  7 2016  <builderdev@builder.jc.rl.ac.uk> - 20130102-3.ceda
- move drscdf.h out the way to avoid conflict with libcdms package

* Thu Jan  3 2013  <builderdev@builder.jc.rl.ac.uk> - 20130102-2.ceda
- add defines needed to avoid unresolved external symbols

* Wed Jan  2 2013 Alan Iwi
alan.iwi@stfc.ac.uk 20130102
- Created initial RPM
