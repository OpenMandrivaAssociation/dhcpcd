Summary:	DHCP Client Daemon
Name:		dhcpcd
Version:	5.2.12
Release:	1
License:	BSD-Like
Group:		System/Servers
URL:		http://dhcpcd.berlios.de/
Source0:	http://roy.marples.name/downloads/dhcpcd/%{name}-%{version}.tar.bz2
Patch1:		dhcpcd-5.1.3-fix-install-permissions.patch
Requires(post): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
dhcpcd is an RFC2131 compliant DHCP client. It is fully featured and yet
lightweight: the binary is 60k as reported by size(1) on Linux i386. It has
support for duplicate address detection, IPv4LL, carrier detection, and a
merged resolv.conf and ntp.conf for which other DHCP clients require third
party tools.

%prep
%setup -q
%patch1 -p1 -b .perms~

%build
%configure2_5x	--bindir=/sbin \
		--libdir=/%{_lib} \
		--libexecdir=/%{_lib} \
		--with-hook=ntp.conf \
		--with-hook=yp.conf \
		--with-hook=ypbind

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
