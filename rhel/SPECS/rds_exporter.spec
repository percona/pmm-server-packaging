%global _dwz_low_mem_die_limit 0

# do not strip debug symbols
%global debug_package   %{nil}

%global provider	github
%global provider_tld	com
%global project		percona
%global repo		rds_exporter
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		16241617f6758d82105ac20793b98a92139254b6
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")
%define release         7
%define rpm_release     %{release}.%{build_timestamp}.%{shortcommit}%{?dist}

Name:		%{repo}
Version:	%{version}
Release:	%{rpm_release}
Summary:	Prometheus exporter for RDS metrics, written in Go with pluggable metric collectors

License:	ASL 2.0
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
rds_exporter is part of Percona Monitoring and Management.
See the PMM docs for more information.


%prep
%setup -q -n %{repo}-%{commit}
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s $(pwd) src/%{provider_prefix}


%build
export GOPATH=$(pwd)
go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -a -v -x %{provider_prefix}


%install
install -d -p %{buildroot}%{_sbindir}
install -p -m 0755 %{repo} %{buildroot}%{_sbindir}/%{repo}


%files
%license src/%{provider_prefix}/LICENSE
%doc src/%{provider_prefix}/README.md
%{_sbindir}/%{name}


%changelog
* Thu Sep  5 2019 Viacheslav Sarzhan <slava.sarzhan@percona.com> - 2.0.0-7
- init version
