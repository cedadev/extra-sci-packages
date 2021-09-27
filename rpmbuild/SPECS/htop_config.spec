Summary: Package that installs htop and a configuration file for it
Name: htop_config_jasmin
Version: 1.1
Release: 1
BuildArch: noarch
Requires: htop
License: GPLv3


%description
Installs the htop and creates an /etc/htoprc package that sets the delay between updates to reduce CPU usage.

%prep
cat > htoprc <<EOF
# default 5 second delay between updates to limit CPU usage
delay=50
EOF

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc
install -m 644 htoprc $RPM_BUILD_ROOT/etc/

%files
%config /etc/htoprc
