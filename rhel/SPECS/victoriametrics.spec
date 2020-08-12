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
%global commit          2791008e1982f30892fe86cc98888f4c4519c858
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           percona-%{repo}
Version:        1.39.4
Release:        1%{?dist}
Summary:        VictoriaMetrics monitoring solution and time series database
License:        ASL 2.0
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
* Wed Aug 12 2020 Aliaksandr Valialkin <valyala@victoriametrics.com> - 1.39.4-1
- PMM-6389 add victoriametrics and vmalert binaries
