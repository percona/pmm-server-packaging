%global provider	github
%global provider_tld	com
%global project		percona
%global repo		pmm-server
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit	        0dbbc0ca255591000f0371012cd4e7515624a059
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")
%global pmm_repo        pmm
%global pmm_prefix      %{provider}.%{provider_tld}/%{project}/%{pmm_repo}
%global pmm_commit      @@pmm_commit@@
%global pmm_shortcommit %(c=%{pmm_commit}; echo ${c:0:7})
%define release         5
%define rpm_release     %{release}.%{build_timestamp}.%{shortcommit}%{?dist}

Name:		%{repo}
Version:	%{version}
Release:	%{rpm_release}
Summary:	Percona Monitoring and Management Server

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:	https://%{pmm_prefix}/archive/%{pmm_commit}/%{pmm_repo}-%{pmm_shortcommit}.tar.gz

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
%setup -q -n %{repo}-%{commit}
sed -i "s/ENV_SERVER_USER/${SERVER_USER:-pmm}/g" prometheus.yml
sed -i "s/ENV_SERVER_PASSWORD/${SERVER_PASSWORD:-pmm}/g" prometheus.yml
echo "${SERVER_USER:-pmm}:$(openssl passwd -apr1 ${SERVER_PASSWORD:-pmm})" > .htpasswd
sed -i "s/v[0-9].[0-9].[0-9]/v%{version}/" landing-page/index.html


%install
tar -zxvf %SOURCE1
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
mv prometheus.yml %{buildroot}%{_sysconfdir}/prometheus.yml

install -d %{buildroot}%{_sysconfdir}/clickhouse-server

install -d %{buildroot}%{_sysconfdir}/supervisord.d
mv supervisord.conf %{buildroot}%{_sysconfdir}/supervisord.d/pmm.ini

install -d %{buildroot}%{_datadir}/%{name}/landing-page/img
cp -pav ./entrypoint.sh %{buildroot}%{_datadir}/%{name}/entrypoint.sh
cp -pav ./password-page/dist %{buildroot}%{_datadir}/%{name}/password-page
cp -pav ./landing-page/img/pmm-logo.svg %{buildroot}%{_datadir}/%{name}/landing-page/img/pmm-logo.svg
cp -pav ./%{pmm_repo}-%{pmm_commit}/api/swagger %{buildroot}%{_datadir}/%{name}/swagger
rm -rf %{pmm_repo}-%{pmm_commit}

install -d %{buildroot}/usr/lib/systemd/system
install -p -m 0644 node_exporter.service %{buildroot}/usr/lib/systemd/system/node_exporter.service
install -p -m 0644 clickhouse_exporter.service %{buildroot}/usr/lib/systemd/system/clickhouse_exporter.service


%post
/usr/bin/systemd-tmpfiles --create
%systemd_post node_exporter.service
%systemd_post clickhouse_exporter.service

%preun
%systemd_preun node_exporter.service
%systemd_preun clickhouse_exporter.service

%postun
%systemd_postun node_exporter.service
%systemd_postun clickhouse_exporter.service


%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_sysconfdir}/sysconfig
%{_sysconfdir}/supervisord.d
%{_sysconfdir}/prometheus.yml
%{_sysconfdir}/nginx/.htpasswd
%{_sysconfdir}/nginx/conf.d/pmm.conf
%{_sysconfdir}/nginx/conf.d/pmm-ssl.conf
%{_sysconfdir}/tmpfiles.d/pmm.conf
%{_sysconfdir}/cron.daily/purge-qan-data
%{_datadir}/percona-dashboards/import-dashboards.py*
%{_datadir}/%{name}
/usr/lib/systemd/system/node_exporter.service
/usr/lib/systemd/system/clickhouse_exporter.service


%changelog
* Thu Apr 11 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 2.0.0-4
- PMM-3606 get the latest version of Swagger

* Mon Mar 18 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 2.0.0-3
- PMM-3677 remove Orchestrator from pmm2

* Fri Mar 15 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 2.0.0-2
- PMM-3606 Serve new Swagger spec and UI

* Tue Dec  4 2018 Vadim Yalovets <vadim.yalovets@percona.com> - 2.0.0-1
- PMM-3176 Remove Prometheus 1.x

* Thu Nov 15 2018 Vadim Yalovets <vadim.yalovets@percona.com> - 1.12.0-13
- PMM-2911 PMM with Clickhouse

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
