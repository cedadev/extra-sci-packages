%define _name tkdiff

%{?scl:%scl_package %{_name}}
Name:           %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}

Version: 4.3.5
%define _version 4-3-5
Release: 1.ceda%{?dist}
Source0: %{_name}-%{_version}.zip
License: GPL v2
Group: Development/Tools
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix} 
Packager: Alan Iwi <alan.iwi@stfc.ac.uk>
Vendor: John M. Klassa
Url: http://tkdiff.sourceforge.net
Summary: a Tcl/Tk front-end to diff
Requires: tk

%description
TkDiff is a Tcl/Tk front-end to diff for Unix and  Windows, and is Copyright (C) 1994-2018 by John M. Klassa.

%prep
%setup -n %{_name}-%{_version}

%build

%install

dir=$RPM_BUILD_ROOT/%{_bindir}
mkdir -p $dir
cp tkdiff $dir/

dir=$RPM_BUILD_ROOT/%{_docdir}
mkdir -p $dir
cp *.txt $dir/

%clean
rm -rf $RPM_BUILD_ROOT

%changelog

* Fri Sep 27 2019 Builder <builder@builder.ceda.ac.uk> - 4.3.5-1.ceda
- CentOS7 SCL build

%files
%defattr(-,root,root,-)
%attr(755,root,root) %{_bindir}/tkdiff
%doc %{_docdir}/README.txt
%doc %{_docdir}/LICENSE.txt
%doc %{_docdir}/CHANGELOG.txt
