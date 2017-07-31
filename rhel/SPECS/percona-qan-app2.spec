%global provider	github
%global provider_tld	com
%global project		percona
%global repo		qan-app
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		64054a8cf4c7d8dc95287a55eef16d91ad56b859
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")

Name:		%{project}-%{repo}2
Version:	1.2.1
Release:	1.%{build_timestamp}.%{shortcommit}%{?dist}
Summary:	Query Analytics API for PMM

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:	qan-app2-node_modules-1.2.1.tar.gz

BuildRequires:	nodejs
BuildArch:	noarch
Requires:	nginx

%description
Percona Query Analytics (QAN) API is part of Percona Monitoring and Management.
See the PMM docs for more information.


%prep
%setup -q -a 1 -n %{repo}-%{commit}
sed -i 's/"version": "v[0-9].[0-9].[0-9]"/"version": "v%{version}"/' package.json node_modules/package.json
diff package.json node_modules/package.json


%build
npm run build:prod


%install
install -d %{buildroot}%{_datadir}/%{name}
cp -pav ./dist/qan-app2/*    %{buildroot}%{_datadir}/%{name}


%files
%license LICENSE
%doc README.md
%{_datadir}/%{name}


%changelog
* Mon Jun 26 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.2.1-1
- up to 1.2.1
- use prefetched node_modules

* Mon Jun 26 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.6-1
- PMM-1087 fix QAN2 package building issue

* Thu Feb  2 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.4-1
- add angular2 support

* Thu Feb  2 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.0-1
- add build_timestamp to Release value
- use bower deps from main archive

* Mon Jan 23 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.0.7-3
- fix version inside index.html

* Wed Dec 28 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 1.0.7-2
- fix client/app/app.js

* Mon Dec 19 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 1.0.7-1
- init version
