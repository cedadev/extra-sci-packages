%{!?scl:%global scl jasmin-sci}
%scl_package %scl

Summary: Package that installs %scl
Name: %scl_name
Version: 1.2
Release: 1%{?dist}
BuildArch: noarch
License: GPLv2+
BuildRequires: scl-utils-build
Obsoletes: ceda-sci

Requires: %{scl_prefix}runtime == %{version}-%{release}

# Requires from CentOS / EPEL base (non SCL packages)

Requires: GraphicsMagick-c++
Requires: atlas
Requires: atlas-devel
Requires: ddd
Requires: emacs
Requires: emacs-gnuplot
Requires: gcc-gfortran
Requires: firefox
Requires: geany
Requires: geos-devel
Requires: gitk
Requires: glibc-static
Requires: gnuplot
Requires: gpsbabel
Requires: grads
Requires: grass
Requires: grass-devel
Requires: gv
Requires: ksh
Requires: libRmath
Requires: libRmath-devel
Requires: libcurl-devel
Requires: libuuid-devel
Requires: mercurial
Requires: ncview
Requires: nedit
Requires: netcdf-cxx
Requires: netcdf-cxx-devel
Requires: netcdf-devel
Requires: netcdf-fortran-devel
Requires: octave
Requires: octave-devel
Requires: octave-netcdf
Requires: p7zip
Requires: perl-Image-ExifTool
Requires: perl-core
Requires: perl-devel
Requires: postgresql-devel
Requires: proj
Requires: proj-devel
Requires: proj-epsg
Requires: proj-nad
Requires: proj-static
Requires: qt-devel
Requires: redhat-lsb
Requires: sqlite-devel
Requires: subversion
Requires: subversion-devel
Requires: subversion-tools
Requires: tcl-devel
Requires: tcsh
Requires: texlive-dvipng
Requires: tk-devel
Requires: tree
Requires: udunits2-devel
Requires: uuid
Requires: uuid-devel
Requires: vim-enhanced
Requires: wxGTK-devel
Requires: xemacs
Requires: xorg-x11-util-macros
Requires: xpdf

# Requires from local JASMIN builds (SCL packages)

# when updating this list, also update the build_all.sh script at the
# top level of the repo with the names of the spec files required to
# build these
#
Requires: %{scl_prefix}mo_unpack >= 2.0.1-2
Requires: %{scl_prefix}xconv >= 1.94-1
Requires: %{scl_prefix}lxterminal >= 0.3.2-1
Requires: %{scl_prefix}leafpad >= 0.8.18-1
Requires: %{scl_prefix}tkdiff >= 4.3.5-1
Requires: %{scl_prefix}nccmp >= 1.8.3.1-1
Requires: %{scl_prefix}ferret >= 7.5.0-1
Requires: %{scl_prefix}ferret-datasets >= 7.4-2
Requires: %{scl_prefix}hdfeos2 >= 20.1.00-1
Requires: %{scl_prefix}mtk >= 1.4.5-1
Requires: %{scl_prefix}mtk-devel >= 1.4.5-1
Requires: %{scl_prefix}diffuse >= 0.4.8-1
Requires: %{scl_prefix}libemos >= 4.5.9-1
Requires: %{scl_prefix}libdrs >= 3.1.2-1
Requires: %{scl_prefix}libcrayutil >= 20121128-3
Requires: %{scl_prefix}umutil >= 20130102-4
Requires: %{scl_prefix}umutil-lib >= 20130102-4

%if %{?_with_closed_source:1}%{?!_with_closed_source:0}
Requires: %{scl_prefix}withgroups >= 1.1-1
%endif


%description
The %scl Software Collection is a collection of software packages which provide a scientific
software environment.  It is intended to be used in combination with the Jaspy conda environment,
and these RPMs will provide additional packages to supplement Jaspy.  Installing this 
meta-package will cause the installation of:

 1) a number of software packages built for JASMIN, which will install under /opt/rh/jasmin-sci
    and which will require the following setup command before running them:

        source /opt/rh/jasmin-sci/enable

 2) a number of software packages from standard repositories, which will install under 
    ordinary system paths

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils
#Requires: %{scl_name} == %{version}-%{release}
Obsoletes: ceda-sci-runtime

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: %{scl_name}-runtime == %{version}-%{release}

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%prep
%setup -c -T

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_scl_scripts}/root
cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}:\$PATH

if [ -z \$LD_LIBRARY_PATH ]
then
   export LD_LIBRARY_PATH=%{_libdir}
else
   export LD_LIBRARY_PATH=%{_libdir}:\$LD_LIBRARY_PATH
fi

if [ -z \$MANPATH ]
then
   export MANPATH=%{_mandir}
else
   export MANPATH=%{_mandir}:\$MANPATH
fi
EOF
%scl_install

%files

%files runtime
%scl_files

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config


%changelog

# changelog may be incomplete - see history in git

* Fri Dec 13 2019 Builder <builder@builder.ceda.ac.uk> - 1.2-1
- +firefox

* Fri Nov  1 2019 Builder <builder@builder.ceda.ac.uk> - 1-5
- direct dependency on exact version of runtime

* Thu Sep 26 2019 Alan Iwi <alan.iwi@stfc.ac.uk> 1-1
- Initial package


