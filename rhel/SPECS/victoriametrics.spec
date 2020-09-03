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
%global commit          764b3d4fda41e27aa7af83e406503c1087c41d4d
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           percona-victoriametrics
Version:        1.40.0
Release:        2%{?dist}
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
* Wed Sep 3 2020 Aliaksandr Valialkin <valyala@victoriametrics.com> - 1.40.0-2
- PMM-6389 add victoriametrics and vmalert binaries
