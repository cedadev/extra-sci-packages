%{?scl:%scl_package minio}
Name: %{?scl_pkg_name}%{?!scl_pkg_name:minio}
Version: 20211007.041958
Release: 1%{?dist}
Source0: mc
License: Affero GPL v3
Group: Scientific support
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix} 
Packager: Alan Iwi <alan.iwi@stfc.ac.uk>
Vendor: MinIO, Inc.
Url: https://docs.min.io/docs/
Summary: High Performance Object Storage command line client
%{?scl:BuildRequires: %{scl_prefix}build}

%define exe_name minio

%description

MinIO is a High Performance Object Storage released under GNU Affero
General Public License v3.0. It is API compatible with Amazon S3 cloud
storage service. Use MinIO to build high performance infrastructure
for machine learning, analytics and application data workloads.

%prep

%build

%install
[ $RPM_BUILD_ROOT != / ] && rm -fr $RPM_BUILD_ROOT

dir=$RPM_BUILD_ROOT/%{_bindir}
mkdir -p $dir
cp %{SOURCE0} $dir/%{exe_name}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog

%files
%defattr(755,root,root)
%{_bindir}/%{exe_name}
