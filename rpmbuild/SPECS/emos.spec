%define _name libemos

%{?scl:%scl_package %{_name}}
Name: %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Version: 4.5.9
Release: 2%{?dist}
License: LGPL 3.0
Group: Scientific support	
Source0: %{_name}-%{version}-Source.tar.gz
Patch0: emos_allow_arg_mismatch.patch
Buildroot: %{_tmppath}/%{_name}-%{version}-%{release}-root
BuildRequires: gcc, gcc-gfortran cmake %{scl_prefix}eccodes2_27-devel
Requires: %{scl_prefix}eccodes2_27
Url: https://confluence.ecmwf.int/display/EMOS/
Summary: EMOSLIB interpolation software from ECMWF


%description					
The EMOS library from ECMWF (32 and 64 bit versions).

%prep

%setup0 -q -n %{_name}-%{version}-Source
%patch0 -p2

%build

%define install_dir %{?scl:%{_scl_root}}/usr

mkdir build
cd build

%define eccodes_dir /opt/rh/jasmin-sci/root/opt/eccodes2.27.1

export CMAKE_C_FLAGS=-I%{eccodes_dir}/include
export CMAKE_CXX_FLAGS=-I%{eccodes_dir}/include
export CMAKE_LD_FLAGS="-L%{eccodes_dir}/lib64 -leccodes"

cmake .. -D CMAKE_INSTALL_PREFIX=%{install_dir} -D ECCODES_PATH=%{eccodes_dir} \
      -D ECCODES_INCLUDE_DIRS=%{eccodes_dir}/include

ln -s %{eccodes_dir}/lib64/lib* lib/

find . -name 'link.txt' | xargs perl -pil -e "s,(/usr/bin/(gfortran|cc).*),\\1 -L%{eccodes_dir}/lib64 -leccodes,"

make

%install			

rm -rf $RPM_BUILD_ROOT		
cd build
make install DESTDIR=$RPM_BUILD_ROOT

# Manually create the symlinks that fail because the make install doesn't
# honour DESTDIR for symlinks. These caused CMake warnings
# "failed to create symbolic link", which didn't show the link target but
# running the make install through "strace -f -e symlink" showed what they were.
# An alternative approach would be to use strace for the live install and then
# parse the output to create the symlinks.
ln -s interpol $RPM_BUILD_ROOT/%{install_dir}/share/libemos/tables/land_sea_mask
ln -s libemos.a $RPM_BUILD_ROOT/%{install_dir}/lib/libemos.R32.D64.I32.a
ln -s libemosR64.a $RPM_BUILD_ROOT/%{install_dir}/lib/libemos.R64.D64.I32.a

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

* Sun Feb 18 2024 alan.iwi@stfc.ac.uk
- Rocky9 version - depend on legacy eccodes and add a patch for -fallow-argument-mismatch Fortran arg

* Fri Oct  4 2019 Builder <builder@builder.ceda.ac.uk> - 4.5.9-1
- total revamp of spec file; much later (although deprecated) package, and build for CentOS7/SCL

* Thu Jan 17 2013  <builderdev@builder.jc.rl.ac.uk> - 000382-2.ceda
- -fPIC

* Thu Jan  3 2013 Alan Iwi
alan.iwi@stfc.ac.uk 20130102
- Created initial RPM
