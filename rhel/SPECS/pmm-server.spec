%global provider	github
%global provider_tld	com
%global project		percona
%global repo		pmm-server
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		39d6afbdcf7c3e98693792e93bf2c337861e9a99
%global shortcommit	%(c=%{commit}; echo ${c:0:7})

Name:		%{repo}
Version:	1.0.7
Release:	1%{?dist}
Summary:	Percona Monitoring and Management Server

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildArch:	noarch
Requires:	nginx

%description
Percona Monitoring and Management (PMM) Server.
See the PMM docs for more information.


%prep
%setup -q -n %{repo}-%{commit}


%build


%install
install -d %{buildroot}%{_datadir}/%{name}
cp -pav ./* %{buildroot}%{_datadir}/%{name}


%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_datadir}/%{name}


%changelog
* Mon Dec 19 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 1.0.7-1
- init version
