# it is impossible to pass ldflags to revel, so disable check
%undefine _missing_build_ids_terminate_build

%global provider	github
%global provider_tld	com
%global project		percona
%global repo		qan-api
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path	%{provider_prefix}
%global commit		01a21b3e6ddf7881bf3de14f9bd2c550aa0434ec
%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%define build_timestamp %(date -u +"%y%m%d%H%M")

Name:		%{project}-%{repo}
Version:	1.1.1
Release:	2.%{build_timestamp}.%{shortcommit}%{?dist}
Summary:	Query Analytics API for PMM

License:	AGPLv3
URL:		https://%{provider_prefix}
Source0:	https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:	%{name}.service

BuildRequires:	golang
Requires:	perl

%if 0%{?fedora} || 0%{?rhel} == 7
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

%description
Percona Query Analytics (QAN) API is part of Percona Monitoring and Management.
See the PMM docs for more information.


%prep
%setup -T -c -n %{repo}-%{version}
%setup -q -c -a 0 -n %{repo}-%{version}
mkdir -p src/%{provider}.%{provider_tld}/%{project}
mv %{repo}-%{commit} src/%{provider_prefix}
ln -s $(pwd)/src/%{provider_prefix}/vendor/github.com/revel src/github.com/revel


%build
mkdir -p bin release
export GOPATH=$(pwd)
export APP_VERSION="%{version}-%{build_timestamp}.%{shortcommit}"
go build -o ./revel ./src/%{provider_prefix}/vendor/github.com/revel/cmd/revel
./revel build %{provider_prefix} release prod
rm -rf release/src/github.com/percona/qan-api


%install
install -d -p %{buildroot}%{_sbindir}
mv ./release/%{repo} %{buildroot}%{_sbindir}/%{name}
install -d -p %{buildroot}%{_datadir}
cp -rpa ./release %{buildroot}%{_datadir}/%{name}
install -d -p %{buildroot}%{_datadir}/%{name}/src/%{provider_prefix}/app/views
install -d -p %{buildroot}%{_datadir}/%{name}/src/%{provider_prefix}/service/query
cp -pa  ./src/%{provider_prefix}/scripts/* %{buildroot}%{_datadir}/%{name}/
cp -rpa ./src/%{provider_prefix}/schema    %{buildroot}%{_datadir}/%{name}/schema
cp -rpa ./src/%{provider_prefix}/conf      %{buildroot}%{_datadir}/%{name}/src/%{provider_prefix}/conf
cp -rpa ./src/%{provider_prefix}/service/query/mini.pl %{buildroot}%{_datadir}/%{name}/src/%{provider_prefix}/service/query/mini.pl

install -d -p %{buildroot}%{_sysconfdir}
cp -rpa ./src/%{provider_prefix}/conf/prod.conf %{buildroot}%{_sysconfdir}/percona-qan-api.conf

install -d %{buildroot}/usr/lib/systemd/system
install -p -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{name}.service


%post
%if 0%{?fedora} || 0%{?rhel} == 7
%systemd_post %{name}.service
%else
#/sbin/chkconfig --add %{name}
%endif

%preun
%if 0%{?fedora} || 0%{?rhel} == 7
%systemd_preun %{name}.service
%else
if [ $1 = 0 ]; then
    #service %{name} stop >/dev/null 2>&1 ||:
    #/sbin/chkconfig --del %{name}
fi
%endif

%postun
%if 0%{?fedora} || 0%{?rhel} == 7
%systemd_postun %{name}.service
%else
if [ "$1" -ge "1" ]; then
    #service %{name} condrestart > /dev/null 2>&1 ||:
fi
%endif


%files
%license src/%{provider_prefix}/LICENSE
%doc src/%{provider_prefix}/README.md src/%{provider_prefix}/CHANGELOG.md
%attr(0755, root, root) %{_sbindir}/%{name}
%{_datadir}/%{name}
/usr/lib/systemd/system/%{name}.service
%config %{_sysconfdir}/percona-qan-api.conf


%changelog
* Mon Mar  6 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.1-2
- mark percona-qan-api.conf as %config

* Thu Feb  2 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 1.1.0-1
- add build_timestamp to Release value
- use deps from vendor dir

* Fri Dec 16 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 1.0.7-1
- init version
