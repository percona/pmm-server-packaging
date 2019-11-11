%undefine _missing_build_ids_terminate_build

# do not strip debug symbols
%global debug_package   %{nil}

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
%define release         23
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
install -d %{buildroot}%{_datadir}/%{name}
cp -pav ./ansible %{buildroot}%{_datadir}/%{name}

install -d %{buildroot}%{_sbindir}
cd src/github.com/percona/pmm-update
install -p -m 0755 bin/pmm-update %{buildroot}%{_sbindir}/


%files
%license LICENSE
%doc README.md
%{_sbindir}/pmm-update
%{_datadir}/%{name}


# Currently, the only thing from changelog that is used by pmm-update is the first URL.
# Specifically, the change date is ignored – RPM's "Buildtime" is used instead.

%changelog

* Mon Nov 11 2019 Alexey Palazhchenko <alexey.palazhchenko@percona.com> - 2.1.0-23
- https://per.co.na/pmm/2.1.0

* Mon Sep 23 2019 Alexey Palazhchenko <alexey.palazhchenko@percona.com> - 2.0.1-19
- https://per.co.na/pmm/2.0.1

* Wed Sep 18 2019 Alexey Palazhchenko <alexey.palazhchenko@percona.com> - 2.0.0-18
- https://per.co.na/pmm/2.0.0

* Tue Sep 17 2019 Alexey Palazhchenko <alexey.palazhchenko@percona.com> - 2.0.0-17.rc4
- https://per.co.na/pmm/2.0.0-rc4

* Mon Sep 16 2019 Alexey Palazhchenko <alexey.palazhchenko@percona.com> - 2.0.0-16.rc3
- https://per.co.na/pmm/2.0.0-rc3

* Fri Sep 13 2019 Alexey Palazhchenko <alexey.palazhchenko@percona.com> - 2.0.0-15.rc2
- https://per.co.na/pmm/2.0.0-rc2

* Wed Sep 11 2019 Alexey Palazhchenko <alexey.palazhchenko@percona.com> - 2.0.0-14.rc1
- https://per.co.na/pmm/2.0.0-rc1

* Mon Sep  9 2019 Alexey Palazhchenko <alexey.palazhchenko@percona.com> - 2.0.0-12.beta7
- https://per.co.na/pmm/2.0.0-beta7
