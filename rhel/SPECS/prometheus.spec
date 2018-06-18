%if 0%{?fedora} || 0%{?rhel} == 6
%global with_devel 1
%global with_bundled 1
%global with_debug 1
# No test files so far
%global with_check 0
%global with_unit_test 0
%else
%global with_devel 0
%global with_bundled 1
%global with_debug 1
%global with_check 0
%global with_unit_test 0
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%define copying() \
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7 \
%license %{*} \
%else \
%doc %{*} \
%endif

%global isgccgoarch 0
%if 0%{?gccgo_arches:1}
%ifarch %{gccgo_arches}
%global isgccgoarch 1
%endif
%endif

%global provider        github
%global provider_tld    com
%global project         prometheus
%global repo            prometheus
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          290d71791a507a5057b9a099c9d48703d86dc941
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           percona-%{repo}
Version:        2.3.0
Release:        1%{?dist}
Summary:        The Prometheus monitoring system and time series database
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:        %{repo}.service

%if 0%{?fedora} || 0%{?rhel} == 7
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

# If go_arches not defined fall through to implicit golang archs
%if 0%{?go_arches:1}
ExclusiveArch:  %{go_arches}
%else
ExclusiveArch:  %{ix86} x86_64 %{arm}
%endif
# If gccgo_arches does not fit or is not defined fall through to golang
%if %{isgccgoarch}
BuildRequires:   gcc-go >= %{gccgo_min_vers}
%else
BuildRequires:   golang >= 1.7.3
%endif

%description
%{summary}


%if ! 0%{?with_bundled}
BuildRequires: golang(bitbucket.org/ww/goautoneg)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/hashicorp/consul/api)
BuildRequires: golang(github.com/julienschmidt/httprouter)
BuildRequires: golang(github.com/miekg/dns)
BuildRequires: golang(github.com/samuel/go-zookeeper/zk)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb/filter)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb/iterator)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb/opt)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb/util)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(gopkg.in/fsnotify.v1)
BuildRequires: golang(gopkg.in/yaml.v2)
%endif


%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:        %{summary}
BuildArch:     noarch

%if 0%{?with_check}
BuildRequires: golang(bitbucket.org/ww/goautoneg)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/hashicorp/consul/api)
BuildRequires: golang(github.com/julienschmidt/httprouter)
BuildRequires: golang(github.com/miekg/dns)
BuildRequires: golang(github.com/samuel/go-zookeeper/zk)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb/filter)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb/iterator)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb/opt)
BuildRequires: golang(github.com/syndtr/goleveldb/leveldb/util)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(gopkg.in/fsnotify.v1)
BuildRequires: golang(gopkg.in/yaml.v2)
%endif

Requires: golang(bitbucket.org/ww/goautoneg)
Requires: golang(github.com/golang/protobuf/proto)
Requires: golang(github.com/hashicorp/consul/api)
Requires: golang(github.com/julienschmidt/httprouter)
Requires: golang(github.com/miekg/dns)
Requires: golang(github.com/samuel/go-zookeeper/zk)
Requires: golang(github.com/syndtr/goleveldb/leveldb)
Requires: golang(github.com/syndtr/goleveldb/leveldb/filter)
Requires: golang(github.com/syndtr/goleveldb/leveldb/iterator)
Requires: golang(github.com/syndtr/goleveldb/leveldb/opt)
Requires: golang(github.com/syndtr/goleveldb/leveldb/util)
Requires: golang(golang.org/x/net/context)
Requires: golang(gopkg.in/fsnotify.v1)
Requires: golang(gopkg.in/yaml.v2)


%description devel
%{summary}

This package contains library source intended for 
building other packages which use %{project}/%{repo}.
%endif

%if 0%{?with_unit_test}
%package unit-test
Summary:         Unit tests for %{name} package
# If go_arches not defined fall through to implicit golang archs
%if 0%{?go_arches:1}
ExclusiveArch:   %{go_arches}
%else
ExclusiveArch:   %{ix86} x86_64 %{arm}
%endif
# If gccgo_arches does not fit or is not defined fall through to golang
%if %{isgccgoarch}
BuildRequires:   gcc-go >= %{gccgo_min_vers}
%else
BuildRequires:   golang
%endif

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}
#patch0 -p1

%build
# If gccgo_arches does not fit or is not defined fall through to golang
# gccco arches
%if %{isgccgoarch}
%if 0%{?gcc_go_build:1}
export GOCOMPILER='%{gcc_go_build}'
%else
echo "No compiler for SA"
exit 1
%endif
# golang arches (due to ExclusiveArch)
%else
%if 0%{?golang_build:1}
export GOCOMPILER='%{golang_build} -ldflags "$LDFLAGS"'
%else
export GOCOMPILER='go build -ldflags "$LDFLAGS"'
%endif
%endif

export LDFLAGS=""
%if 0%{?with_debug}
%if %{isgccgoarch}
export OLD_RPM_OPT_FLAGS="$RPM_OPT_FLAGS"
function gobuild {
export RPM_OPT_FLAGS="$OLD_RPM_OPT_FLAGS -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')"
eval ${GOCOMPILER} -a -v -x "$@";
}
%else
export OLD_LDFLAGS="$LDFLAGS"
function gobuild {
export LDFLAGS="$OLD_LDFLAGS -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')"
eval ${GOCOMPILER} -a -v -x "$@";
}
%endif
%else
function gobuild { eval ${GOCOMPILER} -a -v -x "$@"; }
%endif

# set working directory
mkdir -p src/github.com/prometheus
ln -s ../../../ src/github.com/prometheus/prometheus

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
# build from bundled dependencies
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

# set environment variables
export GO_VERSION=$(go version | cut -d' ' -f3 | sed 's/go//')
export BUILDDATE=$(date +%Y%m%d-%H:%M:%S)

# build prometheus
export OLD_LDFLAGS="$OLD_LDFLAGS -X github.com/prometheus/prometheus/vendor/github.com/prometheus/common/version.Branch=v%{version} "
export OLD_LDFLAGS="$OLD_LDFLAGS -X github.com/prometheus/prometheus/vendor/github.com/prometheus/common/version.Version=%{version} "
export OLD_LDFLAGS="$OLD_LDFLAGS -X github.com/prometheus/prometheus/vendor/github.com/prometheus/common/version.Revision=%{commit} "
export OLD_LDFLAGS="$OLD_LDFLAGS -X github.com/prometheus/prometheus/vendor/github.com/prometheus/common/version.BuildUser=Jenkins "
export OLD_LDFLAGS="$OLD_LDFLAGS -X github.com/prometheus/prometheus/vendor/github.com/prometheus/common/version.BuildDate=${BUILDDATE} "

gobuild -o bin/prometheus %{import_path}/cmd/prometheus
gobuild -o bin/promtool   %{import_path}/cmd/promtool

%install
install -D -p -m 0755 bin/%{repo}  %{buildroot}%{_sbindir}/%{repo}
install -D -p -m 0755 bin/promtool %{buildroot}%{_bindir}/promtool
install -d %{buildroot}%{_datadir}/%{repo}
cp -rpa ./consoles %{buildroot}%{_datadir}/%{repo}/consoles
cp -rpa ./console_libraries %{buildroot}%{_datadir}/%{repo}/console_libraries
install -d %{buildroot}/usr/lib/systemd/system
install -p -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{repo}.service
install -d %{buildroot}%{_sharedstatedir}/%{repo}

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done
for file in $(find ./config/testdata -iname "*"); do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done
for file in $(find ./promql/testdata -iname "*"); do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if %{isgccgoarch}
function gotest { %{gcc_go_test} "$@"; }
%else
%if 0%{?golang_test:1}
function gotest { %{golang_test} "$@"; }
%else
function gotest { go test "$@"; }
%endif
%endif

export GOPATH=%{buildroot}/%{gopath}:%{gopath}
gotest %{import_path}/web/api
gotest %{import_path}/utility
gotest %{import_path}/templates
gotest %{import_path}/storage/remote
gotest %{import_path}/storage/remote/opentsdb
gotest %{import_path}/storage/remote/influxdb
gotest %{import_path}/storage/metric
#gotest %{import_path}/storage/local
#gotest %{import_path}/storage/local/flock
#gotest %{import_path}/storage/local/codable
#gotest %{import_path}/rules
#gotest %{import_path}/promql
gotest %{import_path}/retrieval
gotest %{import_path}/notification
gotest %{import_path}/config
%endif

%post
%if 0%{?fedora} || 0%{?rhel} == 7
%systemd_post %{repo}.service
%else
#/sbin/chkconfig --add %{repo}
%endif

%preun
%if 0%{?fedora} || 0%{?rhel} == 7
%systemd_preun %{repo}.service
%else
if [ $1 = 0 ]; then
    #service %{repo} stop >/dev/null 2>&1 ||:
    #/sbin/chkconfig --del %{repo}
fi
%endif

%postun
%if 0%{?fedora} || 0%{?rhel} == 7
%systemd_postun %{repo}.service
%else
if [ "$1" -ge "1" ]; then
    #service %{repo} condrestart > /dev/null 2>&1 ||:
fi
%endif


%files
%copying LICENSE
%doc CHANGELOG.md CONTRIBUTING.md README.md NOTICE
#doc Godeps/Godeps.json
%{_sbindir}/%{repo}
%{_bindir}/promtool
%{_datadir}/%{repo}
/usr/lib/systemd/system/%{repo}.service
%dir %attr(-, nobody, nobody) %{_sharedstatedir}/%{repo}

%if 0%{?with_devel}
%files devel -f devel.file-list
%copying LICENSE
%doc CHANGELOG.md CONTRIBUTING.md README.md
#doc Godeps/Godeps.json
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%dir %{gopath}/src/%{import_path}
%endif

%if 0%{?with_unit_test}
%files unit-test -f unit-test.file-list
%copying LICENSE.md
%doc README.md
%endif

%changelog
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
