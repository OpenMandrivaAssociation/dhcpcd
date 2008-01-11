
Summary:	DHCPC Daemon
Name:		dhcpcd
Version:	3.1.8
Release:	%mkrel 2
License:	GPL
Group:		System/Servers
URL:		http://dhcpcd.berlios.de/
Source0:	http://prdownload.berlios.de/dhcpcd/%{name}-%{version}.tar.bz2
Requires(post): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
dhcpcd is an implementation of the DHCP client specified in
draft-ietf-dhc-dhcp-09 (when -r option is not specified) and RFC1541 (when -r
option is specified).

It gets the host information (IP address, netmask, broad- cast address, etc.)
from a DHCP server and configures the network interface of the machine on which
it is running. It also tries to renew the lease time according to RFC1541 or
draft-ietf-dhc-dhcp-09.

%prep
%setup -q

%build
%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}/var/log
touch %{buildroot}/var/log/%{name}.log

%post
# Create initial log files so that logrotate doesn't complain
if [ $1 = 1 ]; then # first install
    %create_ghostfile dhcpcd root root 644
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README ChangeLog
#%config(noreplace) %{_sysconfdir}/dhcpc/*
/sbin/dhcpcd
%{_mandir}/man8/dhcpcd.8*
%ghost /var/log/%{name}.log
