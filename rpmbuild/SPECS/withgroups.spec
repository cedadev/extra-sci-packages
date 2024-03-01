%define _name withgroups

%{?scl:%scl_package %{_name}}
Name: %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Summary: A utility to change the current groups including during non-interactive workflows
Version: 1.1
Release: 2%{?dist}
Group: Applications/System
Source0: %{_name}-v%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
License: STFC
Requires: libcap
BuildRequires: libcap-devel

%description

The "withgroups" utility allows the user to specify the group list with which a command is run 
by prefixing "withgroups group1,group2,..." to a command.

This is intended for use in situations where the filesystem type (e.g. NFS) only recognises a 
limited number of groups and the user is a member of more groups than this.  This can mean that 
a file operation which ought to work in principle in fact gives a permission denied error because 
the filesystem looks at only an arbitrary subset of the group list.  The withgroups command allows 
the user to work around this by running a command with the group list narrowed down to the ones of 
relevance.

%prep
%setup -q -n %{_name}-v%{version}

%build
make

%install
%define exe withgroups
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install %{exe} $RPM_BUILD_ROOT%{_bindir}

%post
setcap cap_setgid=p %{_bindir}/%{exe}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(111, root, -) %{_bindir}/%{exe}

%changelog
* Fri Mar 1 2024 alan.iwi@stfc.ac.uk
- Rocky 9 build

* Fri Nov 15 2019 Builder <builder@builder.ceda.ac.uk> - 
- Initial build.

