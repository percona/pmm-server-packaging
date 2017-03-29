%global debug_package   %{nil}
%global provider        github
%global provider_tld    com
%global project         grafana
%global repo            grafana
# https://github.com/grafana/grafana
%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit          v4.2.0
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**}; 
%endif

Name:           percona-%{repo}
Version:        4.2.0
Release:        2%{?dist}
Summary:        Grafana is an open source, feature rich metrics dashboard and graph editor
License:        ASL 2.0
URL:            https://%{import_path}
Source0:        https://%{import_path}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source2:        grafana-node_modules-%{shortcommit}.el7.tar.gz
Source3:        grafana-server.service
Patch0:         grafana-v4.2.0-fix-tooltip.patch
ExclusiveArch:  %{ix86} x86_64 %{arm}

BuildRequires: golang >= 1.7.3
BuildRequires: nodejs-grunt-cli fontconfig

%if 0%{?fedora} || 0%{?rhel} == 7
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

#Requires:       golang >= 1.7.3

%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.

%prep
%setup -q -a 2 -n %{repo}-%{version}
%patch0
rm -rf Godeps
sed -i -e 's/var version = "[0-9].[0-9].[0-9]"/var version = "%{version}"/' ./pkg/cmd/grafana-server/main.go

%build
mkdir -p _build/src
mv vendor/github.com _build/src/
mv vendor/golang.org _build/src/
mv vendor/gopkg.in   _build/src/

mkdir -p ./_build/src/github.com/grafana
ln -s $(pwd) ./_build/src/github.com/grafana/grafana
export GOPATH=$(pwd)/_build:%{gopath}

%gobuild -o ./bin/grafana-server ./pkg/cmd/grafana-server
%gobuild -o ./bin/grafana-cli ./pkg/cmd/grafana-cli
/usr/bin/node --max-old-space-size=4500 /usr/bin/grunt --verbose release
#/usr/bin/node --max-old-space-size=4500 /usr/bin/grunt --verbose jshint:source jshint:tests jscs tslint clean:release copy:node_modules copy:public_to_gen phantomjs css htmlmin:build ngtemplates cssmin:build ngAnnotate:build concat:js filerev remapFilerev usemin uglify:genDir build-post-process compress:release

%install
# install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# cp -pav *.go %{buildroot}/%{gopath}/src/%{import_path}/
# cp -rpav pkg public conf tests %{buildroot}/%{gopath}/src/%{import_path}/
install -d -p %{buildroot}%{_datadir}/%{repo}
cp -pav *.md %{buildroot}%{_datadir}/%{repo}
# cp -rpav benchmarks %{buildroot}/%{gopath}/src/%{import_path}/
cp -rpav docs %{buildroot}%{_datadir}/%{repo}
cp -rpav public_gen %{buildroot}%{_datadir}/%{repo}/public
cp -rpav scripts %{buildroot}%{_datadir}/%{repo}
cp -rpav vendor %{buildroot}%{_datadir}/%{repo}
install -d -p %{buildroot}%{_sbindir}
cp bin/%{repo}-server %{buildroot}%{_sbindir}/
install -d -p %{buildroot}%{_bindir}
cp bin/%{repo}-cli %{buildroot}%{_bindir}/
install -d -p %{buildroot}%{_sysconfdir}/%{repo}
cp conf/sample.ini %{buildroot}%{_sysconfdir}/%{repo}/grafana.ini
mv conf/ldap.toml %{buildroot}%{_sysconfdir}/%{repo}/
cp -rpav conf %{buildroot}%{_datadir}/%{repo}
%if 0%{?fedora} || 0%{?rhel} == 7
mkdir -p %{buildroot}/usr/lib/systemd/system
install -p -m 0644 %{SOURCE3} %{buildroot}/usr/lib/systemd/system/
%else
mkdir -p %{buildroot}%{_initddir}/
install -p -m 0644 packaging/rpm/init.d/grafana-server %{buildroot}%{_initddir}/
%endif
#mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
#install -p -m 0644 packaging/rpm/sysconfig/grafana-server %{buildroot}%{_sysconfdir}/sysconfig
install -d -p %{buildroot}%{_sharedstatedir}/%{repo}
install -d -p %{buildroot}/var/log/%{repo}

%check
export GOPATH=$(pwd)/_build:%{gopath}
go test ./pkg/api
go test ./pkg/bus
go test ./pkg/components/apikeygen
go test ./pkg/components/renderer
go test ./pkg/events
go test ./pkg/models
go test ./pkg/plugins
go test ./pkg/services/sqlstore
go test ./pkg/services/sqlstore/migrations
go test ./pkg/setting
go test ./pkg/util

%files
%defattr(-, grafana, grafana, -)
%{_datadir}/%{repo}
%exclude %{_datadir}/%{repo}/*.md
%exclude %{_datadir}/%{repo}/docs
%doc %{_datadir}/%{repo}/CHANGELOG.md
%doc %{_datadir}/%{repo}/LICENSE.md
%doc %{_datadir}/%{repo}/NOTICE.md
%doc %{_datadir}/%{repo}/README.md
%doc %{_datadir}/%{repo}/docs
%attr(0755, root, root) %{_sbindir}/%{repo}-server
%attr(0755, root, root) %{_bindir}/%{repo}-cli
%{_sysconfdir}/%{repo}/grafana.ini
%{_sysconfdir}/%{repo}/ldap.toml
%if 0%{?fedora} || 0%{?rhel} == 7
%attr(-, root, root) /usr/lib/systemd/system/grafana-server.service
%else
%attr(-, root, root) %{_initddir}/grafana-server
%endif
#attr(-, root, root) %{_sysconfdir}/sysconfig/grafana-server
%dir %{_sharedstatedir}/%{repo}
%dir /var/log/%{repo}

%pre
getent group grafana >/dev/null || groupadd -r grafana
getent passwd grafana >/dev/null || \
    useradd -r -g grafana -d /etc/grafana -s /sbin/nologin \
    -c "Grafana Dashboard" grafana
exit 0

%post
%systemd_post grafana.service

%preun
%systemd_preun grafana.service

%postun
%systemd_postun grafana.service

%changelog
* Wed Mar 29 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.2.0-2
- up to 4.2.0
- PMM-708 rollback tooltip position

* Tue Mar 14 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.1.2-1
- up to 4.1.2

* Thu Jan 26 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.1.1-1
- up to 4.1.1

* Thu Dec 29 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 4.0.2-2
- use fixed grafana-server.service

* Thu Dec 15 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 4.0.2-1
- up to 4.0.2

* Fri Jul 31 2015 Graeme Gillies <ggillies@redhat.com> - 2.0.2-3
- Unbundled phantomjs from grafana

* Tue Jul 28 2015 Lon Hohberger <lon@redhat.com> - 2.0.2-2
- Change ownership for grafana-server to root

* Tue Apr 14 2015 Graeme Gillies <ggillies@redhat.com> - 2.0.2-1
- First package for Fedora
