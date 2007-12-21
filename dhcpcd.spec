%define	rversion 1.3.22-pl4

Summary:	DHCPC Daemon
Name:		dhcpcd
Version:	1.3.22pl4
Release:	%mkrel 7
License:	GPL
Group:		System/Servers
URL:		http://www.phystech.com/download/dhcpcd.html
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/dhcpcd-%{rversion}.tar.bz2
Patch1:		dhcpcd-1.3.22-pl4-resolvrdv.patch
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

%setup -q -n %{name}-%{rversion}
%patch1 -p1 -b .resolvrdv

%build
%configure2_5x
%make DEFS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/var/log

install -m0755 dhcpcd -D %{buildroot}/sbin/dhcpcd
install -m0755 dhcpcd.exe -D %{buildroot}%{_sysconfdir}/dhcpc/dhcpcd.exe
install -m0644 dhcpcd.8 -D %{buildroot}/%{_mandir}/man8/dhcpcd.8
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
%doc README ChangeLog INSTALL *.lsm
%config(noreplace) %{_sysconfdir}/dhcpc/*
/sbin/dhcpcd
%{_mandir}/man8/dhcpcd.8*
%ghost /var/log/%{name}.log


