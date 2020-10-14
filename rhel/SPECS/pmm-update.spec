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
%define release         44
%define rpm_release     %{release}.%{build_timestamp}.%{shortcommit}%{?dist}

%global install_golang 0

# the line below is sed'ed by build/bin/build-server-rpm to set a correct version
%define full_pmm_version 2.0.0

Name:		%{repo}
Version:	%{version}
Release:	%{rpm_release}
Summary:	Tool for updating packages and OS configuration for PMM Server

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

%if %{install_golang}
BuildRequires:   golang >= 1.12.0
%endif

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
* Wed Oct 14 2020 Nurlan Moldomurov <nurlan.moldomurov@percona.com> - 2.11.0-44
- https://per.co.na/pmm/2.11.0

* Tue Sep 22 2020 Nurlan Moldomurov <nurlan.moldomurov@percona.com> - 2.10.1-43
- https://per.co.na/pmm/2.10.1

* Tue Sep 15 2020 Nurlan Moldomurov <nurlan.moldomurov@percona.com> - 2.10.0-41
- https://per.co.na/pmm/2.10.0

* Tue Aug 04 2020 Nurlan Moldomurov <nurlan.moldomurov@percona.com> - 2.9.1-39
- https://per.co.na/pmm/2.9.1

* Tue Jul 14 2020 Nurlan Moldomurov <nurlan.moldomurov@percona.com> - 2.9.0-37
- https://per.co.na/pmm/2.9.0

* Thu Jul  2 2020 Mykyta Solomko <mykyta.solomko@percona.com> - 2.6.1-35
- PMM-5645 built using Golang 1.14

* Thu Jun 25 2020 Nurlan Moldomurov <nurlan.moldomurov@percona.com> - 2.8.0-34
- https://per.co.na/pmm/2.8.0

* Tue Jun 09 2020 Nurlan Moldomurov <nurlan.moldomurov@percona.com> - 2.7.0-33
- https://per.co.na/pmm/2.7.0

* Mon May 18 2020 Nurlan Moldomurov <nurlan.moldomurov@percona.com> - 2.6.1-32
- https://per.co.na/pmm/2.6.1

* Mon May 11 2020 Nurlan Moldomurov <nurlan.moldomurov@percona.com> - 2.6.0-31
- https://per.co.na/pmm/2.6.0

* Tue Apr 14 2020 Nurlan Moldomurov <nurlan.moldomurov@percona.com> - 2.5.0-30
- https://per.co.na/pmm/2.5.0

* Wed Mar 18 2020 Nurlan Moldomurov <nurlan.moldomurov@percona.com> - 2.4.0-29
- https://per.co.na/pmm/2.4.0

* Mon Feb 17 2020 Alexey Palazhchenko <alexey.palazhchenko@percona.com> - 2.3.0-28
- https://per.co.na/pmm/2.3.0

* Tue Feb 4 2020 Alexey Palazhchenko <alexey.palazhchenko@percona.com> - 2.2.2-27
- https://per.co.na/pmm/2.2.2

* Thu Jan 23 2020 Alexey Palazhchenko <alexey.palazhchenko@percona.com> - 2.2.1-26
- https://per.co.na/pmm/2.2.1

* Tue Dec 24 2019 Alexey Palazhchenko <alexey.palazhchenko@percona.com> - 2.2.0-25
- https://per.co.na/pmm/2.2.0

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
