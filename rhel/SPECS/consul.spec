%if 0%{?fedora}
%global with_devel 1
# no bundled dependencies so far
%global with_bundled 0
%global with_debug 1
%global with_check 1
%else
%global with_devel 0
# no bundled dependencies so far
%global with_bundled 1
%global with_debug 0
%global with_check 0
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         hashicorp
%global repo            consul
# https://github.com/hashicorp/consul
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          a9455cd4fc2809570ff1855c37d6ffc2449bd42f
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           consul
Version:        0.7.1
Release:        1%{?dist}
Summary:        Tool for service discovery, monitoring and configuration http://www.consul.io
License:        MPLv2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:	%{repo}.service

%if 0%{?fedora} || 0%{?rhel} == 7
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang} >= 1.7.3

%if ! 0%{?with_bundled}
# commands.go
#BuildRequires: golang(github.com/mitchellh/cli)
BuildRequires: golang-github-mitchellh-cli-devel-temporary

# main.go
#BuildRequires: golang(github.com/mitchellh/cli)
BuildRequires: golang-github-mitchellh-cli-devel-temporary
%endif

%description
%{summary}

%if 0%{?with_devel} || ! 0%{?with_bundled}
%package -n golang-%{provider}-%{project}-%{repo}-devel
Summary:       %{summary}
BuildArch:      noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/armon/circbuf)
BuildRequires: golang(github.com/armon/go-metrics)
BuildRequires: golang(github.com/armon/go-metrics/datadog)
BuildRequires: golang(github.com/armon/go-radix)
BuildRequires: golang(github.com/fsouza/go-dockerclient)
BuildRequires: golang(github.com/hashicorp/go-checkpoint)
BuildRequires: golang(github.com/hashicorp/go-cleanhttp)
BuildRequires: golang(github.com/hashicorp/go-memdb)
BuildRequires: golang(github.com/hashicorp/go-msgpack/codec)
BuildRequires: golang(github.com/hashicorp/go-syslog)
BuildRequires: golang(github.com/hashicorp/golang-lru)
BuildRequires: golang(github.com/hashicorp/hcl)
BuildRequires: golang(github.com/hashicorp/logutils)
BuildRequires: golang(github.com/hashicorp/memberlist)
BuildRequires: golang(github.com/hashicorp/net-rpc-msgpackrpc)
BuildRequires: golang(github.com/hashicorp/raft)
BuildRequires: golang(github.com/hashicorp/raft-boltdb)
BuildRequires: golang(github.com/hashicorp/scada-client)
BuildRequires: golang(github.com/hashicorp/serf/coordinate)
BuildRequires: golang(github.com/hashicorp/serf/serf)
BuildRequires: golang(github.com/hashicorp/yamux)
BuildRequires: golang(github.com/inconshreveable/muxado)
BuildRequires: golang(github.com/miekg/dns)
#BuildRequires: golang(github.com/mitchellh/cli)
BuildRequires: golang-github-mitchellh-cli-devel-temporary
BuildRequires: golang(github.com/mitchellh/mapstructure)
BuildRequires: golang(github.com/ryanuber/columnize)
# indirect dep
BuildRequires: golang(github.com/docker/go-units)
BuildRequires: golang(github.com/opencontainers/runc/libcontainer/user)
%endif

Requires:      golang(github.com/armon/circbuf)
Requires:      golang(github.com/armon/go-metrics)
Requires:      golang(github.com/armon/go-metrics/datadog)
Requires:      golang(github.com/armon/go-radix)
Requires:      golang(github.com/fsouza/go-dockerclient)
Requires:      golang(github.com/hashicorp/go-checkpoint)
Requires:      golang(github.com/hashicorp/go-cleanhttp)
Requires:      golang(github.com/hashicorp/go-memdb)
Requires:      golang(github.com/hashicorp/go-msgpack/codec)
Requires:      golang(github.com/hashicorp/go-syslog)
Requires:      golang(github.com/hashicorp/golang-lru)
Requires:      golang(github.com/hashicorp/hcl)
Requires:      golang(github.com/hashicorp/logutils)
Requires:      golang(github.com/hashicorp/memberlist)
Requires:      golang(github.com/hashicorp/net-rpc-msgpackrpc)
Requires:      golang(github.com/hashicorp/raft)
Requires:      golang(github.com/hashicorp/raft-boltdb)
Requires:      golang(github.com/hashicorp/scada-client)
Requires:      golang(github.com/hashicorp/serf/coordinate)
Requires:      golang(github.com/hashicorp/serf/serf)
Requires:      golang(github.com/hashicorp/yamux)
Requires:      golang(github.com/inconshreveable/muxado)
Requires:      golang(github.com/miekg/dns)
#Requires:      golang(github.com/mitchellh/cli)
Requires:      golang-github-mitchellh-cli-devel-temporary
Requires:      golang(github.com/mitchellh/mapstructure)
Requires:      golang(github.com/ryanuber/columnize)
# Indirect dep
Requires:      golang(github.com/docker/go-units)
Requires:      golang(github.com/opencontainers/runc/libcontainer/user)

Provides:      golang(%{import_path}/acl) = %{version}-%{release}
Provides:      golang(%{import_path}/api) = %{version}-%{release}
Provides:      golang(%{import_path}/command) = %{version}-%{release}
Provides:      golang(%{import_path}/command/agent) = %{version}-%{release}
Provides:      golang(%{import_path}/consul) = %{version}-%{release}
Provides:      golang(%{import_path}/consul/state) = %{version}-%{release}
Provides:      golang(%{import_path}/consul/structs) = %{version}-%{release}
Provides:      golang(%{import_path}/testutil) = %{version}-%{release}
Provides:      golang(%{import_path}/tlsutil) = %{version}-%{release}
Provides:      golang(%{import_path}/watch) = %{version}-%{release}

%description -n golang-%{provider}-%{project}-%{repo}-devel
%{summary}

This package contains library source intended for
building other packages which use %{project}/%{repo}.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package -n golang-%{provider}-%{project}-%{repo}-unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
%endif

%description -n golang-%{provider}-%{project}-%{repo}-unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}

%build
mkdir -p src/github.com/hashicorp
ln -s ../../../ src/github.com/hashicorp/consul

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

%gobuild -o bin/%{name} %{import_path}

%install
# consul subpackage
install -D -p -m 0755 bin/%{name} %{buildroot}%{_sbindir}/%{name}
install -d %{buildroot}/usr/lib/systemd/system
install -p -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{repo}.service
#install -d %{buildroot}%{_initddir}/ 
#install -p -m 0755 etc/init.d/orchestrator.bash %{buildroot}%{_initddir}/%{repo}
install -d %{buildroot}%{_sysconfdir}/%{repo}.d
install -d %{buildroot}%{_sharedstatedir}/%{repo}

%if 0%{?with_devel} || ! 0%{?with_bundled}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list
done
%endif

%if 0%{?with_devel} || ! 0%{?with_bundled}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/Godeps/_workspace:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}
%gotest %{import_path}/acl
%gotest %{import_path}/api
#%%gotest %{import_path}/command
#%%gotest %{import_path}/command/agent
#%%gotest %{import_path}/consul
%gotest %{import_path}/consul/state
%gotest %{import_path}/consul/structs
%gotest %{import_path}/testutil
#%%gotest %{import_path}/tlsutil
%gotest %{import_path}/watch
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}


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
%license LICENSE
%doc CHANGELOG.md README.md
%{_sbindir}/%{name}
#{_initddir}/%{repo}
/usr/lib/systemd/system/%{repo}.service
%dir %{_sysconfdir}/%{repo}.d
%dir %attr(-, nobody, nobody) %{_sharedstatedir}/%{repo}

%if 0%{?with_devel} || ! 0%{?with_bundled}
%files -n golang-%{provider}-%{project}-%{repo}-devel -f devel.file-list
%license LICENSE
%doc CHANGELOG.md README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files -n golang-%{provider}-%{project}-%{repo}-unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc CHANGELOG.md README.md
%endif

%changelog
* Tue Jan 17 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 0.7.1-1.gita9455cd
- update to 0.7.1

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-0.6.git46499d6
- https://fedoraproject.org/wiki/Changes/golang1.7

* Thu Mar 17 2016 jchaloup <jchaloup@redhat.com> - 0.6.0-0.5.git46499d6
- Polish the spec file
  resolves: #1318556

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-0.4.git46499d6
- https://fedoraproject.org/wiki/Changes/golang1.6

* Tue Feb 16 2016 jchaloup <jchaloup@redhat.com> - 0.6.0-0.3.git46499d6
- Add deps missing in docker (temporary fix)
  related: #1290013

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-0.2.git46499d6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 09 2015 jchaloup <jchaloup@redhat.com> - 0.6.0-0.1.git46499d6
- Update to 0.6.0
  resolves: #1290013

* Wed Apr 15 2015 jchaloup <jchaloup@redhat.com> - 0-0.1.git5079177
- First package for Fedora
  resolves: #1208616

