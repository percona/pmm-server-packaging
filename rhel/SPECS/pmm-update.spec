%undefine _missing_build_ids_terminate_build

# we need to remove it as soon as we remove all noarch pmm-update rpms
# from 'pmm2-components/yum/laboratory'
%define _binaries_in_noarch_packages_terminate_build   0

%global provider	github
%global provider_tld	com
%global project		percona
%global repo		pmm-update
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		592eddf656bce32a11bd958af0a32c62bd5ea34c
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")
%define release         9
%define rpm_release     %{release}.%{build_timestamp}.%{shortcommit}%{?dist}

%define full_pmm_version 2.0.0

Name:		%{repo}
Version:	%{version}
Release:	%{rpm_release}
Summary:	Tool for updating packages and OS configuration for PMM Server

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildRequires:  golang

BuildArch:	noarch
Requires:	PyYAML


%description
%{summary}


%prep
%setup -q -n %{repo}-%{commit}
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s $(pwd) src/%{provider_prefix}

%build
export GOPATH=$(pwd)/

export PMM_RELEASE_VERSION=%{full_pmm_version}
export PMM_RELEASE_FULLCOMMIT=%{commit}
export PMM_RELEASE_BRANCH=""

cd src/github.com/percona/pmm-update
make release


%install
install -d %{buildroot}%{_bindir}

install -p -m 0755 ./bin/pmm-update %{buildroot}%{_bindir}/pmm-update
install -p -m 0755 ./bin/pmm-update-check %{buildroot}%{_bindir}/pmm-update-check
install -p -m 0755 ./bin/pmm-update-stage2 %{buildroot}%{_bindir}/pmm-update-stage2

install -d %{buildroot}%{_datadir}/%{name}
cp -pav ./ansible %{buildroot}%{_datadir}/%{name}

install -d %{buildroot}%{_sbindir}
cd src/github.com/percona/pmm-update
install -p -m 0755 bin/pmm2-update %{buildroot}%{_sbindir}/


%files
%license LICENSE
%doc README.md
%{_bindir}/*
%{_sbindir}/pmm2-update
%{_datadir}/%{name}
/usr/lib/debug/usr/sbin/pmm2-update.debug


%changelog
* Fri Jun 30 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.6-1
- move repository from Percona-Lab to percona organization

* Mon Feb 13 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.0-2
- add ansible dir to %{_datadir}/%{name}

* Tue Feb  7 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.0-1
- init version
