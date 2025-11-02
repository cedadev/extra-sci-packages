%define _name saga

%{?scl:%scl_package %{_name}}
Name:           %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Version:        9.10.0
Release:        1%{?dist}
Summary:        GTK+ based simple text editor
Group:          Scientific support
License:        GPL
URL:            https://saga-gis.sourceforge.io/
Source0:        https://sourceforge.net/projects/saga-gis/files/SAGA%20-%209/SAGA%20-%20%{version}/saga-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{_name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  wxGTK-devel proj-devel gdal-devel libtiff-devel unixODBC-devel

%description
System for Automated Geoscientific Analyses

%prep
%setup -q -n %{_name}-%{version}

%build
%define install_dir %{?scl:%{_scl_root}}/usr
mkdir build
cd build/
cmake ../saga-gis -DCMAKE_INSTALL_PREFIX=%{install_dir}
cmake --build . --config Release

%install
rm -rf $RPM_BUILD_ROOT
cd build
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_datadir}/saga
%{_mandir}/man1/saga*
%{_datadir}/applications/org.saga_gis.saga_gui.desktop
%{_datadir}/pixmaps/saga.png
%{_datadir}/icons/hicolor/*/apps/saga.png
%{_datadir}/metainfo/org.saga_gis.saga_gui.appdata.xml
%{_libdir}/libsaga*
%{_libdir}/saga
%{_includedir}/saga
%{_bindir}/saga_cmd
%{_bindir}/saga_gui


%changelog
* Mon Apr  8 2024 alan.iwi@stfc.ac.uk - 9.3.2
- inital build for Rocky 9 under SCL
