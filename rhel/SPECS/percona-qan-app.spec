%global provider	github
%global provider_tld	com
%global project		percona
%global repo		qan-app
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		29d58f8587e227671182812d2c5805b15240c1bf
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")
%define release         8
%define rpm_release     %{release}.%{build_timestamp}.%{shortcommit}%{?dist}

Name:		%{project}-%{repo}
Version:	%{version}
Release:	%{rpm_release}
Summary:	Query Analytics API for PMM

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:	qan-app-node_modules-1.12.0.tar.gz

BuildRequires:	nodejs
BuildArch:	noarch
Requires:	nginx

%description
Percona Query Analytics (QAN) API is part of Percona Monitoring and Management.
See the PMM docs for more information.


%prep
%setup -q -a 1 -n %{repo}-%{commit}
sed -i 's/"version": "v[0-9].[0-9].[0-9]"/"version": "v%{version}"/' package.json node_modules/package.json


%install
install -d %{buildroot}%{_datadir}/%{name}
cp -pav ./dist/qan-app/*    %{buildroot}%{_datadir}/%{name}


%files
%license LICENSE
%doc README.md
%{_datadir}/%{name}


%changelog
* Mon Jun 25 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 1.12.0-3
- PMM-2660 bump version

* Mon Jun 18 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 1.12.0-2
- PMM-2580 use pre-built dir

* Tue Jun 12 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 1.12.0-1
- PMM-2617 update node_modules

* Wed Feb 21 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 1.8.0-3
- PMM-2002 update node_modules

* Mon Nov 20 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.5.0-2
- PMM-1680 fix build path

* Mon Jun 26 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.3.0-1
- up to 1.3.0

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
