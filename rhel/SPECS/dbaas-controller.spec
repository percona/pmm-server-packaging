%undefine _missing_build_ids_terminate_build
%global _dwz_low_mem_die_limit 0

# do not strip debug symbols
%global debug_package   %{nil}

%global provider	github
%global provider_tld	com
%global project		percona-platform
%global repo		dbaas-controller
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		41d72afe43a88f522bdd35a4281a447424f18055
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")
%define release         1
%define rpm_release     %{release}.%{build_timestamp}.%{shortcommit}%{?dist}

%global install_golang 0

Name:		%{repo}
Version:	%{version}
Release:	%{rpm_release}
Summary:	Simplified API for managing Percona Kubernetes Operators

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

%if %{install_golang}
BuildRequires:   golang >= 1.14.0
%endif

%description
dbaas-controller exposes a simplified API for managing Percona Kubernetes Operators
See the PMM docs for more information.


%prep
%setup -q -n %{repo}-%{commit}
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s $(pwd) src/%{provider_prefix}


%build
cd src/github.com/percona-platform/dbaas-controller
make release


%install
install -d -p %{buildroot}%{_bindir}
install -d -p %{buildroot}%{_sbindir}
install -p -m 0755 bin/dbaas-controller %{buildroot}%{_sbindir}/dbaas-controller


%files
#%license src/%{provider_prefix}/LICENSE
%doc src/%{provider_prefix}/README.md
%{_sbindir}/dbaas-controller


%changelog
* Fri Jul  10 2020 Mykyta Solomko <mykyta.solomko@percona.com> - 2.9.0-1
- init version
