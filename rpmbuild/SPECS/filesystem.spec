%define _name filesystem

%{?scl:%scl_package %{_name}}
Name: %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}
Summary: Package that owns various directories under %scl
Version: 1.1
Release: 1%{?dist}
BuildArch: noarch
License: GPLv2+

%description

The purpose of this package is to own directories under %scl that are not otherwise owned by a package 
(which are created automatically as leading directories for various other packages).  This will help to 
remove unwanted empty directories if the SCL is removed.

%prep

if ! rpm -q %scl_name
then
    echo "WARNING - %scl_name should normally be installed before building"
    echo "Build is possible without it (to avoid a bootstrap problem) but you should rebuild this once it is installed"
    echo "so that all directories are captured"
    echo "press enter to continue / ctrl-c to abort..."
    read dummy
fi

%build

# list of files not owned by any package
find /opt/rh/%scl_name -type d | xargs rpm -qf | awk '/not owned by any package/{print $2}' > dirlist

# and if an earlier version of this package is already installed, also add its existing contents
rpm -q %name && rpm -ql %name >> dirlist

awk '{print "%dir",$0}' dirlist | sort > dirlist_with_dir_directives


%install
list=$(pwd)/dirlist
rm -rf $RPM_BUILD_ROOT
sed s,^,$RPM_BUILD_ROOT, $list | xargs mkdir -p

%clean
rm -rf $RPM_BUILD_ROOT

%files -f dirlist_with_dir_directives


%changelog
* Mon Sep 27 2021 Builder <builder@builder.ceda.ac.uk> - sci-filesystem
- Initial build.

