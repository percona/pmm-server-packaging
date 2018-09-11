%global provider	github
%global provider_tld	com
%global project		percona
%global repo		pmm-server
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		313549577c9517dd16f381001d1642e6fc73ed8b
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")

Name:		%{repo}
Version:	1.12.0
Release:	11.%{build_timestamp}.%{shortcommit}%{?dist}
Summary:	Percona Monitoring and Management Server

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildArch:	noarch
Requires:	nginx ansible git bats
BuildRequires:	openssl

%if 0%{?fedora} || 0%{?rhel} == 7
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

%description
Percona Monitoring and Management (PMM) Server.
See the PMM docs for more information.


%prep
%setup -q -a 1 -n %{repo}-%{commit}
sed -i "s/ENV_SERVER_USER/${SERVER_USER:-pmm}/g" prometheus.yml prometheus1.yml
sed -i "s/ENV_SERVER_PASSWORD/${SERVER_PASSWORD:-pmm}/g" prometheus.yml prometheus1.yml
echo "${SERVER_USER:-pmm}:$(openssl passwd -apr1 ${SERVER_PASSWORD:-pmm})" > .htpasswd
sed -i "s/v[0-9].[0-9].[0-9]/v%{version}/" landing-page/index.html

%install
install -d %{buildroot}%{_sysconfdir}/nginx/conf.d
mv .htpasswd  %{buildroot}%{_sysconfdir}/nginx/.htpasswd
mv nginx.conf %{buildroot}%{_sysconfdir}/nginx/conf.d/pmm.conf
mv nginx-ssl.conf %{buildroot}%{_sysconfdir}/nginx/conf.d/pmm-ssl.conf
install -d %{buildroot}%{_sysconfdir}/cron.daily
mv purge-qan-data %{buildroot}%{_sysconfdir}/cron.daily/purge-qan-data
install -d %{buildroot}%{_datadir}/percona-dashboards
mv import-dashboards.py %{buildroot}%{_datadir}/percona-dashboards/import-dashboards.py
install -d %{buildroot}%{_sysconfdir}/tmpfiles.d
mv tmpfiles.d-pmm.conf %{buildroot}%{_sysconfdir}/tmpfiles.d/pmm.conf

mv sysconfig %{buildroot}%{_sysconfdir}/sysconfig
mv orchestrator.conf.json %{buildroot}%{_sysconfdir}/orchestrator.conf.json
mv prometheus.yml %{buildroot}%{_sysconfdir}/prometheus.yml
mv prometheus1.yml %{buildroot}%{_sysconfdir}/prometheus1.yml

install -d %{buildroot}%{_sysconfdir}/clickhouse-server
mv clickhouse.xml %{buildroot}%{_sysconfdir}/clickhouse-server/config.xml

install -d %{buildroot}%{_sysconfdir}/my.cnf.d
mv my.cnf %{buildroot}%{_sysconfdir}/my.cnf.d/00-pmm.cnf

install -d %{buildroot}%{_sysconfdir}/supervisord.d
mv supervisord.conf %{buildroot}%{_sysconfdir}/supervisord.d/pmm.ini

install -d %{buildroot}%{_datadir}/%{name}/landing-page/img
cp -pav ./entrypoint.sh %{buildroot}%{_datadir}/%{name}/entrypoint.sh
cp -pav ./password-page/dist %{buildroot}%{_datadir}/%{name}/password-page
cp -pav ./landing-page/img/pmm-logo.svg %{buildroot}%{_datadir}/%{name}/landing-page/img/pmm-logo.svg

install -d %{buildroot}/usr/lib/systemd/system
install -p -m 0644 node_exporter.service %{buildroot}/usr/lib/systemd/system/node_exporter.service


%post
/usr/bin/systemd-tmpfiles --create
%systemd_post node_exporter.service

%preun
%systemd_preun node_exporter.service

%postun
%systemd_postun node_exporter.service


%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_sysconfdir}/my.cnf.d
%{_sysconfdir}/sysconfig
%{_sysconfdir}/supervisord.d
%{_sysconfdir}/prometheus.yml
%{_sysconfdir}/prometheus1.yml
%{_sysconfdir}/nginx/.htpasswd
%{_sysconfdir}/nginx/conf.d/pmm.conf
%{_sysconfdir}/nginx/conf.d/pmm-ssl.conf
%{_sysconfdir}/tmpfiles.d/pmm.conf
%{_sysconfdir}/orchestrator.conf.json
%{_sysconfdir}/cron.daily/purge-qan-data
%{_sysconfdir}/clickhouse-server/config.xml
%{_datadir}/percona-dashboards/import-dashboards.py*
%{_datadir}/%{name}
/usr/lib/systemd/system/node_exporter.service


%changelog
* Mon Jun 18 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 1.12.0-11
- PMM-2629 add prometheus1 config

* Wed Mar 21 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 1.9.0-10
- PMM-1823 add password page compilation

* Thu Nov 16 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.5.0-6
- PMM-1708 use node_exporter from pmm-client

* Tue Aug 22 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.3.0-5
- add supervisord.d config

* Tue Aug 22 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.2.2-3
- add clickhouse.xml

* Tue Mar 14 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.2-3
- add my.cnf

* Mon Feb 13 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.0-2
- add version to landing page

* Thu Feb  9 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.0-1
- add build_timestamp to Release value

* Wed Dec 28 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 1.0.7-7
- add /etc/tmpfiles.d/pmm.conf file
- run systemd-tmpfiles tool during post install

* Wed Dec 28 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 1.0.7-2
- add sysconfig

* Mon Dec 19 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 1.0.7-1
- init version
