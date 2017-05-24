%global provider	github
%global provider_tld	com
%global project		Percona-Lab
%global repo		pmm-update
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		9fd890b36fb21fbe3d475312b0838d67759ae8ae
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")

Name:		%{repo}
Version:	1.1.4
Release:	2.%{build_timestamp}.%{shortcommit}%{?dist}
Summary:	Tool for updating packages and OS configuration for PMM Server

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildArch:	noarch
Requires:	PyYAML


%description
%{summary}


%prep
%setup -q -n %{repo}-%{commit}


%build


%install
install -d %{buildroot}%{_bindir}
cp -pav ./bin/* %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/%{name}
cp -pav ./ansible %{buildroot}%{_datadir}/%{name}
cp -pav ./helpers %{buildroot}%{_datadir}/%{name}


%files
%license LICENSE
%doc README.md
%{_bindir}/*
%{_datadir}/%{name}


%changelog
* Mon Feb 13 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.0-2
- add ansible dir to %{_datadir}/%{name}

* Tue Feb  7 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.0-1
- init version
