%global provider	github
%global provider_tld	com
%global project		percona
%global repo		qan-app
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		ad8b6ce171946876dca222506ce4848522d4a7e0
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")

Name:		%{project}-%{repo}
Version:	1.1.0
Release:	1.%{build_timestamp}.%{shortcommit}%{?dist}
Summary:	Query Analytics API for PMM

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildArch:	noarch
Requires:	nginx

%description
Percona Query Analytics (QAN) API is part of Percona Monitoring and Management.
See the PMM docs for more information.


%prep
%setup -q -n %{repo}-%{commit}
sed -i "s/':9001',/':' + window.location.port + '\/qan-api',/" client/app/app.js
sed -i "s/v[0-9].[0-9].[0-9]/v%{version}/" index.html


%build


%install
install -d %{buildroot}%{_datadir}/%{name}
cp -pav ./client           %{buildroot}%{_datadir}/%{name}
cp -pav ./scripts          %{buildroot}%{_datadir}/%{name}
cp -pav ./index.html       %{buildroot}%{_datadir}/%{name}
cp -pav ./bower_components %{buildroot}%{_datadir}/%{name}


%files
%license LICENSE
%doc README.md
%{_datadir}/%{name}


%changelog
* Thu Feb  2 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.0-1
- add build_timestamp to Release value
- use bower deps from main archive

* Mon Jan 23 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.0.7-3
- fix version inside index.html

* Wed Dec 28 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 1.0.7-2
- fix client/app/app.js

* Mon Dec 19 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 1.0.7-1
- init version
