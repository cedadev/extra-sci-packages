%define _name ferret-datasets

%{?scl:%scl_package %{_name}}
Name: %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Summary: An Analysis Tool for Gridded and Non-Gridded Data
Version: 7.4
Release: 1%{dist}
License: OSD - http://ferret.pmel.noaa.gov/Ferret/ferret-legal
Group: Scientific support
URL: http://www.ferret.noaa.gov/Ferret/
%define tar_stem FerretDatasets-%{version}
Requires: %{?scl:%{scl_prefix}}ferret
Source0: %{tar_stem}.tar.gz
BuildRoot: %{_tmppath}/%{_name}-%{version}-%{release}-root


%description

Standard datasets for Ferret and PyFerret

The value of the Ferret/PyFerret environment variable FER_DSETS should
be a directory with the contents of this package. (So the $FER_DSETS
directory contains the data, descr, and grids subdirectories.)


%define fer_dir %{?scl:%{_scl_root}}/usr/lib/ferret

%prep
%setup -q -n %{tar_stem}

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{fer_dir}
mv * $RPM_BUILD_ROOT%{fer_dir}/
chmod -R a+rX $RPM_BUILD_ROOT%{fer_dir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{fer_dir}

%changelog

* Wed Oct  2 2019 Builder <builder@builder.ceda.ac.uk> - 7.4.%{dist}
- Initial package for CentOS7 / SCL, separate from ferret base package


* Tue Jan 27 2015  <builderdev@builder.jc.rl.ac.uk> - bin-1
- Initial build.
