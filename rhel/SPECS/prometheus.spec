%define debug_package %{nil}

%define copying() \
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7 \
%license %{*} \
%else \
%doc %{*} \
%endif

%global commit          c448ada63d83002e9c1d2c9f84e09f55a61f0ff7
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%global install_golang 0

Name:           percona-prometheus
Version:        2.19.2
Release:        1%{?dist}
Summary:        The Prometheus monitoring system and time series database
License:        ASL 2.0
URL:            https://github.com/prometheus/prometheus
Source0:        https://github.com/prometheus/prometheus/archive/%{commit}/prometheus-%{shortcommit}.tar.gz

%if %{install_golang}
BuildRequires:   golang >= 1.12.0
%endif

%description
%{summary}

%description
%{summary}


%prep
%setup -q -n prometheus-%{commit}
mkdir -p ./build/src/github.com/prometheus
ln -s $(pwd) ./build/src/github.com/prometheus/prometheus


%build
export GOPATH="$(pwd)/build"
export CGO_ENABLED=0
export USER=builder

cd build/src/github.com/prometheus/prometheus
make build


%install
install -D -p -m 0755 ./prometheus  %{buildroot}%{_sbindir}/prometheus
install -D -p -m 0755 ./promtool %{buildroot}%{_bindir}/promtool
install -d %{buildroot}%{_datadir}/prometheus
cp -rpa ./consoles %{buildroot}%{_datadir}/prometheus/consoles
cp -rpa ./console_libraries %{buildroot}%{_datadir}/prometheus/console_libraries
install -d %{buildroot}%{_sharedstatedir}/prometheus


%files
%copying LICENSE
%doc CHANGELOG.md CONTRIBUTING.md README.md NOTICE
#doc Godeps/Godeps.json
%{_sbindir}/prometheus
%{_bindir}/promtool
%{_datadir}/prometheus
%dir %attr(-, nobody, nobody) %{_sharedstatedir}/prometheus

%changelog
* Wed Jul 22 2020 Mykyta Solomko <mykyta.solomko@percona.com> - 2.19.2-1
- PMM-6234 Update to Prometheus 2.19.2

* Thu Jul  2 2020 Mykyta Solomko <mykyta.solomko@percona.com> - 2.16.0-2
- PMM-5645 built using Golang 1.14

* Tue Feb 25 2020 Vadim Yalovets <vadim.yalovets@percona.com> - 2.16.0-1
- PMM-5329 Update Prometheus to version 2.16.0

* Thu Aug 22 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 2.12.0-1
- PMM-4559 Update to Prometheus v2.12.0

* Fri Jun 14 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 2.10.0-1
- PMM-4187 Prometheus v2.10.0

* Fri Mar  1 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 2.7.1-1
- PMM-3460 Prometheus v2.7.1

* Mon Jan  7 2019 Vadim Yalovets <vadim.yalovets@percona.com> - 2.6.0-1
- PMM-3301 update to 2.6.0

* Fri Nov  9 2018 Vadim Yalovets <vadim.yalovets@percona.com> - 2.5.0-1
- PMM-2912 update to 2.5.0

* Tue Jul 24 2018 Kamil Dziedzic <kamil.dziedzic@percona.com> - 2.3.2-1
- PMM-2725 update to 2.3.2

* Thu Jun 28 2018 Kamil Dziedzic <kamil.dziedzic@percona.com> - 2.3.1-1
- PMM-2182 update to 2.3.1

* Mon Jun 18 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 2.3.0-1
- PMM-2182 update to 2.3.0

* Mon May 28 2018 Kamil Dziedzic <kamil.dziedzic@percona.com> - 2.2.1-1
- PMM-2182 update to 2.2.1

* Thu May 17 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 2.1.0-1
- PMM-2182 update to 2.1.0

* Tue Apr 17 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 1.8.2-3
- PMM-2358 add sleep to unit file, maybe system time will be synced

* Mon Mar 26 2018 Mykola Marzhan <mykola.marzhan@percona.com> - 1.8.2-2
- PMM-2282 start prometheus.service after chronyd.service

* Mon Nov 13 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.8.2-1
- PMM-1577 update to 1.8.2

* Tue Oct 24 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.8.1-1
- PMM-1577 update to 1.8.1

* Thu Oct  5 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.7.2-1
- update to 1.7.2
- PMM-1519 add prometheus stop timeout to systemd unit

* Mon Jun 19 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.7.1-2
- add BuildUser and Branch tags.
  resolves: PMM-968

* Tue Jun 13 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.7.1-1
- update to 1.7.1

* Mon Jun 12 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.7.0-1
- update to 1.7.0

* Thu Jun  1 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.6.3-1
- update to 1.6.3

* Thu Apr 20 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.6.1-1
- update to 1.6.0

* Mon Apr 17 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.6.0-1
- update to 1.6.0

* Tue Mar 14 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.5.2-1
- update to 1.5.2

* Thu Feb  9 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.5.1-1
- update to 1.5.1

* Thu Jan 26 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.5.0-1
- update to 1.5.0

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0-3
- https://fedoraproject.org/wiki/Changes/golang1.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 23 2015 jchaloup <jchaloup@redhat.com> - 0.15.0-1
- Update to 0.15.0
  resolves: #1246058

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 jchaloup <jchaloup@redhat.com> - 0.13.3-2
- Add debug info
  related: #1190426

* Tue May 12 2015 jchaloup <jchaloup@redhat.com> - 0.13.3-1
- Update to 0.13.3
  related: #1190426

* Sat May 09 2015 jchaloup <jchaloup@redhat.com> - 0.13.2-1
- Update to 0.13.2
  related: #1190426

* Sat Feb 07 2015 jchaloup <jchaloup@redhat.com> - 0-0.1.git4e6a807
- First package for Fedora
  resolves: #1190426
