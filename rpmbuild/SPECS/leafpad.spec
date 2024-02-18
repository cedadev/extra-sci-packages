%define _name leafpad

%{?scl:%scl_package %{_name}}
Name:           %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Version:        0.8.19
Release:        1%{?dist}

Summary:        GTK+ based simple text editor

Group:          Applications/Editors
License:        GPLv2+
URL:            http://tarot.freeshell.org/leafpad/
Source0:        http://savannah.nongnu.org/download/leafpad/%{_name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{_name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel >= 2.4 desktop-file-utils 
BuildRequires:  gettext
BuildRequires:  intltool
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
Leafpad is a GTK+ based simple text editor. The user interface is similar to
Notepad. It aims to be lighter than GEdit and KWrite, and to be as useful as
them.

%prep
%setup -q -n %{_name}-%{version}

%build
%configure --enable-chooser
# unfortunately will not build with -Werror=format-security - remove this flag
find . -name Makefile | xargs perl -p -i -e 's/-Werror=format-security//g'
make %{?_smp_mflags}
cat>>data/leafpad.desktop<<EOF
StartupNotify=true
GenericName=Text Editor
GenericName[de]=Texteditor
EOF

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
desktop-file-install --vendor=fedora \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --delete-original \
  $RPM_BUILD_ROOT%{_datadir}/applications/leafpad.desktop
%find_lang %{_name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
#update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
#update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{_name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{_name}
%{_datadir}/applications/*%{_name}.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/pixmaps/leafpad.*
%{_mandir}/man1/leafpad.1.gz

%changelog
* Fri Sep 27 2019 Builder <builder@builder.ceda.ac.uk> - 0.8.18-1
- build for CentOS7 under SCL

* Fri May 20 2011 Orion Poplawski <orion@cora.nwra.com> - 0.8.18.1-1
- Update to 0.8.18.1
- Add BR intltool

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 01 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.17-1
- Update to 0.8.17
- Drop unnecessary BuildRequires for libgnomeprintui22-devel
- Update icon-cache scriptlets

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 10 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.8.13-1
- Upstream update

* Tue Aug 21 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.8.11-2
- Fix License tag
- Rebuild for F8t2

* Fri Jul 20 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.8.11-1
- Upstream update

* Fri May 11 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 0.8.10le-1
- Upstream update

* Wed Sep 06 2006 Michael J. Knox <michael[AT]knox.net.nz> - 0.8.9-3
- Rebuild for FC6
- added BR of gettext

* Mon Apr 17 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.9-1
- Upstream update

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.7-2
- Rebuild for Fedora Extras 5

* Fri Feb  3 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.7-1
- Upstream update

* Sat Nov 27 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.5-1
- Upstream update

* Sat Oct  1 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.4-1
- Upstream update

* Thu Aug 18 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.3-2
- Rebuild for new Cairo

* Sat Jul 23 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.3-1
- Upstream update

* Thu May 19 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.1-1
- Upstream update

* Fri Apr 29 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.8.0-1
- Upstream update

* Fri Apr 22 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.9-7
- Used %%find_lang
- Cleaned up desktop entry generation a bit

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Mar 19 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.9-5
- %%

* Sat Mar 19 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.9-4
- Added desktop-file-utils to BuildRequires

* Wed Mar 16 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.9-3
- Broke %%description at 80 columns

* Wed Mar 16 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.9-2
- Removed explicit Requires

* Tue Mar 15 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.7.9-1
- Bump release to 1

* Thu Feb  3 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0:0.7.9-0.iva.0
- Initial RPM release.
