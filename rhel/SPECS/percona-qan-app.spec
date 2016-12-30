%global provider	github
%global provider_tld	com
%global project		percona
%global repo		qan-app
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		d99d49522a03ef601389dd9053a79560afee485d
%global shortcommit	%(c=%{commit}; echo ${c:0:7})

Name:		%{project}-%{repo}
Version:	1.0.7
Release:	2%{?dist}
Summary:	Query Analytics API for PMM

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:	%{repo}-bower-%{version}.tar.gz

BuildArch:	noarch
Requires:	nginx

%description
Percona Query Analytics (QAN) API is part of Percona Monitoring and Management.
See the PMM docs for more information.


%prep
%setup -q -D -a 1 -n %{repo}-%{commit}
sed -i "s/':9001',/':' + window.location.port + '\/qan-api',/" client/app/app.js


%build


%install
install -d %{buildroot}%{_datadir}/%{name}
cp -pav ./client           %{buildroot}%{_datadir}/%{name}
cp -pav ./scripts          %{buildroot}%{_datadir}/%{name}
cp -pav ./index.html       %{buildroot}%{_datadir}/%{name}
cp -pav ./bower_components %{buildroot}%{_datadir}/%{name}


%files
#license LICENSE
%doc README.md
%{_datadir}/%{name}


%changelog
* Wed Dec 28 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 1.0.7-2
- fix client/app/app.js

* Mon Dec 19 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 1.0.7-1
- init version
