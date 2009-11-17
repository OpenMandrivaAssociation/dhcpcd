Summary:	DHCP Client Daemon
Name:		dhcpcd
Version:	5.1.3
Release:	%mkrel 1
License:	BSD-Like
Group:		System/Servers
URL:		http://dhcpcd.berlios.de/
Source0:	http://prdownload.berlios.de/dhcpcd/%{name}-%{version}.tar.bz2
Requires(post): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%configure2_5x	--bindir=/sbin \
		--libdir=/%{_lib} \
		--libexecdir=/%{_lib}

%serverbuild

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
%doc README
%config(noreplace) %{_sysconfdir}/dhcpcd.conf
/sbin/dhcpcd
%dir /%{_lib}/dhcpcd-hooks
/%{_lib}/dhcpcd-hooks/*
/%{_lib}/dhcpcd-run-hooks
%{_mandir}/man5/dhcpcd.conf.5*
%{_mandir}/man8/dhcpcd.8*
%{_mandir}/man8/dhcpcd-run-hooks.8*
%ghost /var/log/%{name}.log
