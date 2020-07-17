%global debug_package   %{nil}
%global commit          v7.1.0
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%global install_golang 0

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

Name:           percona-grafana
Version:        7.1.0
Release:        q%{?dist}
Summary:        Grafana is an open source, feature rich metrics dashboard and graph editor
License:        ASL 2.0
URL:            https://github.com/grafana/grafana
Source0:        https://github.com/grafana/grafana/archive/%{commit}/grafana-%{shortcommit}.tar.gz
Source2:        percona-favicon.ico
#Patch0:         grafana-6.7.4-fav-icon.patch
#Patch1:         grafana-6.7.4-share-panel.patch
#Patch2:         grafana-6.7.4-remove-update-tab.patch
ExclusiveArch:  %{ix86} x86_64 %{arm}

%if %{install_golang}
BuildRequires:   golang >= 1.12.0
%endif
BuildRequires: nodejs-grunt-cli fontconfig

Requires:       fontconfig freetype urw-fonts

%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.

%prep
%setup -q -n grafana-%{version}
#%patch0 -p 1
#%patch1 -p 1
#%patch2 -p 1
rm -rf Godeps

%build
mkdir -p _build/src
#mv vendor/google.golang.org _build/src/
#mv vendor/cloud.google.com _build/src/
#mv vendor/github.com _build/src/
#mv vendor/golang.org _build/src/
#mv vendor/gopkg.in   _build/src/

#mkdir -p ./_build/src/github.com/grafana
#ln -s $(pwd) ./_build/src/github.com/grafana/grafana
export GOPATH="$(pwd)/_build"

#export LDFLAGS="$LDFLAGS -X main.version=%{version} -X main.commit=%{shortcommit} -X main.buildstamp=$(date '+%s') "
#%gobuild -o ./bin/grafana-server ./pkg/cmd/grafana-server
#%gobuild -o ./bin/grafana-cli ./pkg/cmd/grafana-cli
#yarn install
#npm --verbose run build
make

%install
install -d -p %{buildroot}%{_datadir}/grafana
cp -rpav conf %{buildroot}%{_datadir}/grafana
cp -rpav public %{buildroot}%{_datadir}/grafana
cp -rpav scripts %{buildroot}%{_datadir}/grafana
cp -rpav tools %{buildroot}%{_datadir}/grafana

if [ -d tmp/bin ]; then
 cp -rpav bin/* tmp/bin/
else
 mkdir -p tmp/bin
 cp -rpav bin/* tmp/bin/
fi

install -m 644 %{SOURCE2} %{buildroot}/usr/share/grafana/public/img/percona-favicon.ico

install -d -p %{buildroot}%{_sbindir}
cp tmp/bin/linux-amd64/grafana-server %{buildroot}%{_sbindir}/
install -d -p %{buildroot}%{_bindir}
cp tmp/bin/linux-amd64/grafana-cli %{buildroot}%{_bindir}/

install -d -p %{buildroot}%{_sysconfdir}/grafana
cp conf/sample.ini %{buildroot}%{_sysconfdir}/grafana/grafana.ini
mv conf/ldap.toml %{buildroot}%{_sysconfdir}/grafana/

%if  0%{?rhel} == 6
mkdir -p %{buildroot}%{_initddir}/
install -p -m 0644 packaging/rpm/init.d/grafana-server %{buildroot}%{_initddir}/
%endif

install -d -p %{buildroot}%{_sharedstatedir}/grafana
install -d -p %{buildroot}/var/log/grafana

%check
export GOPATH="$(pwd)/_build"
make test

%files
%defattr(-, grafana, grafana, -)
%{_datadir}/grafana
%doc *.md
%doc docs
%attr(0755, root, root) %{_sbindir}/grafana-server
%attr(0755, root, root) %{_bindir}/grafana-cli
%{_sysconfdir}/grafana/grafana.ini
%{_sysconfdir}/grafana/ldap.toml
%if 0%{?rhel} == 6
%attr(-, root, root) %{_initddir}/grafana-server
%endif
%dir %{_sharedstatedir}/grafana
%dir /var/log/grafana

%pre
getent group grafana >/dev/null || groupadd -r grafana
getent passwd grafana >/dev/null || \
    useradd -r -g grafana -d /etc/grafana -s /sbin/nologin \
    -c "Grafana Dashboard" grafana
exit 0

%changelog
* Thu Jul  2 2020 Mykyta Solomko <mykyta.solomko@percona.com> - 6.7.4-2
- PMM-5645 Built using Golang 1.14

* Thu Jun  4 2020 Mykyta Solomko <mykyta.solomko@percona.com> - 6.7.4-1
- PMM-6009 Update Grafana to 6.7.4; Fixes CVE-2020-13379

* Thu May 21 2020 Vadim Yalovets <vadim.yalovets@percona.com> - 6.7.3-3
- PMM-5906 Remove Update page

* Wed May  6 2020 Vadim Yalovets <vadim.yalovets@percona.com> - 6.7.3-2
- PMM-5882 Delete Snapshot throws an Error

* Wed Apr 29 2020 Mykyta Solomko <mykyta.solomko@percona.com> - 6.7.3-1
- PMM-5549 update Grafana v.6.7.3

* Mon Mar 23 2020 Alexander Tymchuk <alexander.tymchuk@percona.com> - 6.5.1-4
- PMM-4252 Better resolution favicon

* Wed Feb  5 2020 Vadim Yalovets  <vadim.yalovets@percona.com> - 6.5.1-2
- PMM-5251 Last two rows are not visible when scrolling data tables

* Mon Dec  9 2019 Vadim Yalovets  <vadim.yalovets@percona.com> - 6.5.1-1
- PMM-5087 update Grafana v.6.5.1

* Tue Nov 19 2019 Vadim Yalovets  <vadim.yalovets@percona.com> - 6.4.4-1
- PMM-4969 update Grafana v.6.4.4

* Wed Sep 18 2019 Alexey Palazhchenko <alexey.palazhchenko@percona.com> - 6.3.5-2
- Remove old patches.

* Wed Sep  4 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 6.3.5-1
- PMM-4592 Grafana v6.3.5

* Thu Aug 22 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 6.3.3-1
- PMM-4560 Update to Grafana v.6.3.3

* Fri Aug 09 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 6.3.2-1
- PMM-4491 Grafana v6.3.2

* Fri Jul 05 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 6.2.5-1
- PMM-4303 Grafana v6.2.5

* Tue Jun 25 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 6.2.4-1
- PMM-4248 Grafana v6.2.4

* Thu Jun 13 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 6.2.2-1
- PMM-4141 Grafana v6.2.1

* Wed May  1 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 6.1.6-1
- PMM-3969 Grafana 6.1.6

* Fri Apr 26 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 6.1.4-1
- PMM-3936 Grafana v6.1.4

* Wed Apr 10 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 6.1.3-1
- PMM-3806 Grafana 6.1.2 update

* Tue Apr  9 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 6.1.2-1
- PMM-3806 Grafana 6.1.2 update

* Thu Apr  4 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 6.1.0-1
- PMM-3771 Grafana 6.1.0

* Thu Feb 28 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 6.0.0-1
- PMM-3561 grafana update for 6.0

* Mon Jan  7 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 5.4.2-1
- PMM-2685 Grafana 5.4.2

* Thu Nov 15 2018 Vadim Yalovets <vadim.yalovets@percona.com> - 5.3.3-1
- PMM-2685 Grafana 5.3

* Wed Nov 14 2018 Vadim Yalovets <vadim.yalovets@percona.com> - 5.1.3-7
- PMM-3257 Apply Patch from Grafana 5.3.3 to latest PMM version

* Mon Nov 5 2018 Nurlan Moldomurov <nurlan.moldomurov@percona.com> - 5.1.3-5
- PMM-2837 Fix image rendering

* Mon Oct 8 2018 Daria Lymanska <daria.lymanska@percona.com> - 5.1.3-4
- PMM-2880 add change-icon patch

* Mon Jun 18 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 5.1.3-3
- PMM-2625 fix share-panel patch

* Mon Jun 18 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 5.1.3-2
- PMM-2625 add share-panel patch

* Mon May 21 2018 Vadim Yalovets <vadim.yalovets@percona.com> - 5.1.3-1
- PMM-2561 update to 5.1.3

* Thu Mar 29 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 5.0.4-1
- PMM-2319 update to 5.0.4

* Mon Jan  8 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 4.6.3-1
- PMM-1895 update to 4.6.3

* Mon Nov  6 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.6.1-1
- PMM-1652 update to 4.6.1

* Tue Oct 31 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.6.0-1
- PMM-1652 update to 4.6.0

* Fri Oct  6 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.5.2-1
- PMM-1521 update to 4.5.2

* Tue Sep 19 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.4.3-2
- fix HOME variable in unit file

* Wed Aug  2 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.4.3-1
- PMM-1221 update to 4.4.3

* Wed Aug  2 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.4.2-1
- PMM-1221 update to 4.4.2

* Wed Jul 19 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.4.1-1
- PMM-1221 update to 4.4.1

* Thu Jul 13 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.3.2-2
- PMM-1208 install fontconfig freetype urw-fonts

* Thu Jun  1 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 4.3.2-1
- update to 4.3.2

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
