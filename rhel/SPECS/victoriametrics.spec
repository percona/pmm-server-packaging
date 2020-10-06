%define debug_package %{nil}

%define copying() \
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7 \
%license %{*} \
%else \
%doc %{*} \
%endif

%global provider        github
%global provider_tld    com
%global project         VictoriaMetrics
%global repo            VictoriaMetrics
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          2b1d0510faafb53535220c32b2a694ddc5951471
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           percona-victoriametrics
Version:        1.43.0
Release:        1%{?dist}
Summary:        VictoriaMetrics monitoring solution and time series database
License:        Apache-2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz


%description
%{summary}


%prep
%setup -q -n %{repo}-%{commit}


%build
export PKG_TAG=%{shortcommit}
export BUILDINFO_TAG=%{commit}
export USER=builder

make victoria-metrics-pure
make vmalert-pure


%install
install -D -p -m 0755 ./bin/victoria-metrics-pure %{buildroot}%{_sbindir}/victoriametrics
install -D -p -m 0755 ./bin/vmalert-pure %{buildroot}%{_sbindir}/vmalert


%files
%copying LICENSE
%doc README.md
%{_sbindir}/victoriametrics
%{_sbindir}/vmalert


%changelog
* Tue Oct 6 2020 Aliaksandr Valialkin <valyala@victoriametrics.com> - 1.43.0-1
- PMM-6401 upgrade victoriametrics for reading Prometheus data files

* Fri Sep 4 2020 Aliaksandr Valialkin <valyala@victoriametrics.com> - 1.40.1-1
- PMM-6389 add victoriametrics and vmalert binaries
