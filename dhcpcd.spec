# For udev plugin
%global _disable_ld_no_undefined 1

Summary:	DHCP Client Daemon
Name:		dhcpcd
Version:	7.0.8
Release:	2
License:	BSD-Like
Group:		System/Servers
Url:		http://roy.marples.name/projects/dhcpcd
Source0:	http://roy.marples.name/downloads/dhcpcd/%{name}-%{version}.tar.xz
Source1:	dhcpcd.service
Source2:	dhcpcd-tmpfiles.conf
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
%setup -q
%apply_patches

%build
%configure2_5x \
	--bindir=/sbin \
	--libdir=/%{_lib} \
	--libexecdir=/lib \
	--rundir=/run/dhcpcd \
	--with-hook=ntp.conf \
	--with-hook=yp.conf \
	--with-hook=ypbind

%serverbuild

%make

%install
%makeinstall_std
install -m644 %{SOURCE1} -D %{buildroot}%{_unitdir}/%{name}.service
install -m644 %{SOURCE2} -D %{buildroot}%{_tmpfilesdir}/%{name}.conf

# handle the moving of any file hooks not coming with the package
# as well
%if "%{_lib}" == "lib64"
%post
if [ -d /lib64/dhcpcd-hooks ]; then
	mv /lib64/dhcpcd-hooks/* /lib/dhcpcd-hooks
	rmdir /lib64/dhcpcd-hooks/
fi
%endif

%files
%config(noreplace) %{_sysconfdir}/dhcpcd.conf
/sbin/dhcpcd
%dir /lib/dhcpcd-hooks
/lib/dhcpcd-hooks/*
/lib/dhcpcd-run-hooks
%{_datadir}/dhcpcd/hooks
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%{_mandir}/man5/dhcpcd.conf.5*
%{_mandir}/man8/dhcpcd.8*
%{_mandir}/man8/dhcpcd-run-hooks.8*
%dir /%{_lib}/%{name}
%dir /%{_lib}/%{name}/dev
/%{_lib}/%{name}/dev/udev.so
