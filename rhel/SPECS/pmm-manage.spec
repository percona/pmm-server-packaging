%global _dwz_low_mem_die_limit 0

%global provider	github
%global provider_tld	com
%global project		percona
%global repo		pmm-manage
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		56f6671dc4ac56cd835bc893469f092f2f8bea3c
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")
%define release         2
%define rpm_release     %{release}.%{build_timestamp}.%{shortcommit}%{?dist}

Name:		%{repo}
Version:	%{version}
Release:	%{rpm_release}
Summary:	PMM configuration managament tool

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildRequires:	golang

%if 0%{?fedora} || 0%{?rhel} == 7
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

%description
PMM Manage tool is part of Percona Monitoring and Management.
See the PMM docs for more information.


%prep
%setup -q -n %{repo}-%{commit}
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s $(pwd) src/%{provider_prefix}


%build
export GOPATH=$(pwd)
go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -a -v -x %{provider_prefix}/cmd/pmm-configure
go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -a -v -x %{provider_prefix}/cmd/pmm-configurator


%install
install -d -p %{buildroot}%{_bindir}
install -d -p %{buildroot}%{_sbindir}
install -p -m 0755 pmm-configure    %{buildroot}%{_bindir}/pmm-configure
install -p -m 0755 pmm-configurator %{buildroot}%{_sbindir}/pmm-configurator

install -d %{buildroot}/usr/lib/systemd/system
install -p -m 0644 packaging/pmm-manage.service %{buildroot}/usr/lib/systemd/system/%{name}.service


%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service


%files
%license src/%{provider_prefix}/LICENSE
%doc src/%{provider_prefix}/README.md
%{_bindir}/pmm-configure
%{_sbindir}/pmm-configurator
/usr/lib/systemd/system/%{name}.service


%changelog
* Fri Jun 30 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.6-1
- move repository from Percona-Lab to percona organization

* Fri Mar  3 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.1-1
- add pmm-configure

* Fri Feb  3 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.0-2
- add build_timestamp to Release value

* Wed Feb  1 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.0-1
- init version
