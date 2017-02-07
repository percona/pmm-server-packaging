%global provider	github
%global provider_tld	com
%global project		Percona-Lab
%global repo		pmm-update
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		77033e64bd218378c7fa2db01d0faadc0f787e3e
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")

Name:		%{repo}
Version:	1.1.0
Release:	1.%{build_timestamp}.%{shortcommit}%{?dist}
Summary:	Tool for updating packages and OS configuration for PMM Server

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildArch:	noarch


%description
%{summary}


%prep
%setup -q -n %{repo}-%{commit}


%build


%install
install -d %{buildroot}%{_bindir}
cp -pav ./* %{buildroot}%{_bindir}


%files
%license LICENSE
%doc README.md
%{_bindir}/*


%changelog
* Tue Feb  7 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.0-1
- init version
