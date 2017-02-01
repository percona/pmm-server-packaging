%global provider	github
%global provider_tld	com
%global project		Percona-Lab
%global repo		pmm-manage
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		53e62fda9ff89273ac1325148147049cef1a962e
%global shortcommit	%(c=%{commit}; echo ${c:0:7})

Name:		%{repo}
Version:	1.1.0
Release:	1%{?dist}
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
go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -a -v -x %{provider_prefix}/cmd/pmm-configurator


%install
install -d -p %{buildroot}%{_sbindir}
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
%{_sbindir}/pmm-configurator
/usr/lib/systemd/system/%{name}.service


%changelog
* Wed Feb  1 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.0-1
- init version
