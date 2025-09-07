# For udev plugin
%global _disable_ld_no_undefined 1

Summary:	DHCP Client Daemon
Name:		dhcpcd
Version:	10.2.4
Release:	2
License:	BSD-Like
Group:		System/Servers
Url:		https://roy.marples.name/projects/dhcpcd
Source0:	https://github.com/NetworkConfiguration/dhcpcd/releases/download/v%{version}/dhcpcd-%{version}.tar.xz
Source1:	dhcpcd.service
Source2:	dhcpcd@.service
Source3:	dhcpcd-tmpfiles.conf
Patch1:		dhcpcd-6.1.0-fix-install-permissions.patch
Patch2:		dhcpcd-6.1.0-fix-resolvconf-usage.patch
Requires(post): rpm-helper
Provides:	dhcp-client-daemon
BuildRequires:	pkgconfig(udev)

%description
dhcpcd is an RFC2131 compliant DHCP client. It is fully featured and yet
lightweight: the binary is 60k as reported by size(1) on Linux i386. It has
support for duplicate address detection, IPv4LL, carrier detection, and a
merged resolv.conf and ntp.conf for which other DHCP clients require third
party tools.

%prep
%autosetup -p1

%build
%configure \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--dbdir=%{_var}/lib/%{name} \
	--rundir=/run/dhcpcd \
	--with-hook=ntp.conf \
	--with-hook=yp.conf \
	--with-hook=ypbind

%serverbuild

%make_build

%install
%make_install
install -m644 %{S:1} -D %{buildroot}%{_unitdir}/%{name}.service
install -m644 %{S:2} -D %{buildroot}%{_unitdir}/%{name}@.service
install -m644 %{S:3} -D %{buildroot}%{_tmpfilesdir}/%{name}.conf

mkdir -p %{buildroot}%{_sysusersdir}
cat >%{buildroot}%{_sysusersdir}/%{name}.conf <<'EOF'
u dhcpcd - "DHCP client" %{_var}/lib/dhcpcd
EOF

mkdir -p %{buildroot}%{_var}/lib/%{name}

%files
%config(noreplace) %{_sysconfdir}/dhcpcd.conf
%{_bindir}/dhcpcd
%dir %{_libexecdir}/dhcpcd-hooks
%{_libexecdir}/dhcpcd-hooks/*
%{_libexecdir}/dhcpcd-run-hooks
%dir %{_datadir}/dhcpcd
%{_datadir}/dhcpcd/hooks
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}@.service
%{_tmpfilesdir}/%{name}.conf
%{_mandir}/man5/dhcpcd.conf.5*
%{_mandir}/man8/dhcpcd.8*
%{_mandir}/man8/dhcpcd-run-hooks.8*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/dev
%{_libdir}/%{name}/dev/udev.so
%{_sysusersdir}/%{name}.conf
%attr(0755,dhcpcd,dhcpcd) %{_var}/lib/%{name}
