Summary:	DHCP Client Daemon
Name:		dhcpcd
Version:	5.6.2
Release:	1
License:	BSD-Like
Group:		System/Servers
Url:		http://roy.marples.name/projects/dhcpcd
Source0:	http://roy.marples.name/downloads/dhcpcd/%{name}-%{version}.tar.bz2
Patch1:		dhcpcd-5.1.3-fix-install-permissions.patch
Requires(post): rpm-helper
Provides:	dhcp-client-daemon

%description
dhcpcd is an RFC2131 compliant DHCP client. It is fully featured and yet
lightweight: the binary is 60k as reported by size(1) on Linux i386. It has
support for duplicate address detection, IPv4LL, carrier detection, and a
merged resolv.conf and ntp.conf for which other DHCP clients require third
party tools.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--bindir=/sbin \
	--libdir=/%{_lib} \
	--libexecdir=/%{_lib} \
	--with-hook=ntp.conf \
	--with-hook=yp.conf \
	--with-hook=ypbind

%serverbuild

%make

%install
%makeinstall_std

%files
%doc README
%config(noreplace) %{_sysconfdir}/dhcpcd.conf
/sbin/dhcpcd
%dir /%{_lib}/dhcpcd-hooks
/%{_lib}/dhcpcd-hooks/*
/%{_lib}/dhcpcd-run-hooks
%{_mandir}/man5/dhcpcd.conf.5*
%{_mandir}/man8/dhcpcd.8*
%{_mandir}/man8/dhcpcd-run-hooks.8*

