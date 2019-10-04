%define _name diffuse

%{?scl:%scl_package %{_name}}
Name: %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Version: 0.4.8
Release: 1%{?dist}
Summary: Graphical tool for comparing and merging text files

Group: Development/Tools
License: GPLv2+
URL: http://%{name}.sourceforge.net/
Source0: http://dl.sf.net/sourceforge/%{_name}/%{_name}-%{version}.tar.bz2

BuildRequires: desktop-file-utils
Requires: python >= 2.4, pygtk2 >= 2.10

BuildArch: noarch
BuildRoot: %(mktemp -ud %{_tmppath}/%{_name}-%{version}-%{release}-XXXXXX)

%description
Diffuse is a graphical tool for merging and comparing text files.  Diffuse is
able to compare an arbitrary number of files side-by-side and gives users the
ability to manually adjust line matching and directly edit files.  Diffuse can
also retrieve revisions of files from Bazaar, CVS, Darcs, Git, Mercurial,
Monotone, Subversion, and SVK repositories for comparison and merging.

%prep
%setup -q -n %{_name}-%{version}

%build

%install
rm -rf %{buildroot}
%define tmpsclroot %{buildroot}/%{?scl:%{_scl_root}}
mkdir -p %{tmpsclroot}
cp -a src/* %{tmpsclroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_bindir}/diffuse
%{_datadir}/diffuse/
%{_datadir}/applications/diffuse.desktop
%{_datadir}/icons
%{_datadir}/gnome
%{_datadir}/omf
%config(noreplace) %{_sysconfdir}/diffuserc
%{_mandir}/*

%doc AUTHORS ChangeLog COPYING README

%changelog
* Fri Oct  4 2019 Builder <builder@builder.ceda.ac.uk> - 0.4.8-1
- port to CentOS7 / SCL and remove the scrollkeeper stuff

* Tue Aug 10 2010 Jon Levell <fedora@coralbark.net> - 0.4.3-1
- Update to 0.4.3 upstream release

* Thu Sep 17  2009 Jon Levell <fedora@coralbark.net> - 0.4.0-1
- Update to new upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 4  2009 Jon Levell <fedora@coralbark.net> - 0.3.4-1
- Update to new upstream release (patch no longer needed)

* Tue Jun 30 2009 Jon Levell <fedora@coralbark.net> - 0.3.3-1
- Update to latest upstream release
- Add patch provided by upstream 

* Tue Mar 10 2009 Jon Levell <fedora@coralbark.net> - 0.3.1-1
- Update to latest upstream release

* Wed Feb 11 2009 Jon Levell <fedora@coralbark.net> - 0.2.15-4
- Validate the .desktop file
- Use the prescribed forms for scrollkeeper/update-desktop-database
- Clean up the unowned directories

* Sat Jan 24 2009 Jon Levell <fedora@coralbark.net> - 0.2.15-3
- Fix typos in formatting of changelog
- Fix buildroot in line with packaging guidelines
- Updated defattr with default directory permissions

* Wed Jan 21 2009 Jon Levell <fedora@coralbark.net> - 0.2.15-2
- Use macros in file paths
- patch .desktop file to add trailing semi-colons
- updated URL/source/group

* Tue Jan 20 2009 Jon Levell <fedora@coralbark.net> - 0.2.15-1
- clean buildroot on install
- conditional use scrollkeeper/update-desktop-database
- updated release/license as per Fedora guidelines
- first version submitted to Fedora

* Sun Apr 27 2008 Derrick Moser <derrick_moser@yahoo.com>
- created initial diffuse package
