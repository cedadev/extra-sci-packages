%define _name ferret
%define arch RHEL7

%{?scl:%scl_package %{_name}}
Name: %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Summary: An Analysis Tool for Gridded and Non-Gridded Data
Version: 7.6.0
Release: 1%{dist}
License: OSD - http://ferret.pmel.noaa.gov/Ferret/ferret-legal
Group: Scientific support
URL: http://www.ferret.noaa.gov/Ferret/
%define tar_stem Ferret-%{version}-%{arch}
Source0: %{tar_stem}.tar.gz
Source1: libhistory.so.6
Source2: libreadline.so.6
Source3: libtinfo.so.5
BuildRoot: %{_tmppath}/%{_name}-%{version}-%{release}-root


%description

Ferret is an interactive computer visualization and analysis
environment designed to meet the needs of oceanographers and
meteorologists analyzing large and complex gridded data sets.

%define fer_dir %{?scl:%{_scl_root}}/usr/lib/ferret
%define old_libs_dir %{fer_dir}/legacy_libs

%prep
%setup -q -n %{tar_stem}

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{fer_dir}  $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{old_libs_dir}
pushd bin
cp ferret_paths_template.sh ferret_paths.sh
cp ferret_paths_template.csh ferret_paths.csh
perl -p -i -e 's,((setenv|export).*FER_(DIR|DSETS).*")(.*)("),\1%{fer_dir}\5,' ferret_paths.{sh,csh}

#------------------------------------------------
# replace 'ferret' symlink with wrapper script that utilises old libs
# via LD_LIBRARY_PATH
fer_exe=$(ls -l ~/test/Ferret-7.6.0-RHEL7/bin/ferret | awk '{print $11}')
rm ferret
cat > ferret <<EOF
#!/bin/sh
export LD_LIBRARY_PATH=%{old_libs_dir}:\$LD_LIBRARY_PATH
exec %{fer_dir}/bin/$fer_exe "\$@"
EOF
chmod 755 ferret
popd
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} $RPM_BUILD_ROOT%{old_libs_dir}
#------------------------------------------------

mv * $RPM_BUILD_ROOT%{fer_dir}/
chmod -R a+rX $RPM_BUILD_ROOT%{fer_dir}
ln -s %{fer_dir}/bin/{ferret,ferret_paths.{sh,csh}} $RPM_BUILD_ROOT%{_bindir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/ferret
%{_bindir}/ferret_paths.*
%{fer_dir}

%changelog

* Sun Feb 18 2024 alan.iwi@stfc.ac.uk
- bump version and migrate to Rocky9
- uses some libs copied from Centos7 because no Rocky9 executable is provided

* Wed Oct  2 2019 Builder <builder@builder.ceda.ac.uk> - 7.5.0-1.%{dist}
- bump version and migrate to CentOS7 / SCL; data in separate package

* Tue Jan 27 2015  <builderdev@builder.jc.rl.ac.uk> - bin-1
- Initial build.
