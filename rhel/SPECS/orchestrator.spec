%if 0%{?fedora}
%global with_devel 1
%global with_bundled 1
%global with_debug 1
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

%global isgccgoarch 0
%if 0%{?gccgo_arches:1}
%ifarch %{gccgo_arches}
%global isgccgoarch 1
%endif
%endif

%global provider        github
%global provider_tld    com
%global project         github
%global repo            orchestrator
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          e6a806779d41be219af06116d8bdbf1e71802c71
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           percona-%{repo}
Version:        2.0.3
Release:        0.git%{shortcommit}%{?dist}
Summary:        MySQL replication topology management and HA
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:	%{repo}.service

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

%if 0%{?with_devel}
%package devel
Summary:        %{summary}
BuildArch:     noarch

%if 0%{?with_check}
%endif


%description devel
%{summary}

This package contains library source intended for
building other packages which use %{project}/%{repo}.
%endif

%if 0%{?with_unit_test}
%package unit-test
Summary:         Unit tests for %{name} package
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

mv vendor src

# set working directory
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{provider}.%{provider_tld}/%{project}/%{repo}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
# build from bundled dependencies
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

gobuild -o bin/%{repo} go/cmd/orchestrator/main.go

%install
# consul subpackage
install -D -p -m 0755 bin/%{repo} %{buildroot}%{_sbindir}/%{repo}
%if 0%{?fedora} || 0%{?rhel} == 7
install -d %{buildroot}/usr/lib/systemd/system
install -p -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/%{repo}.service
%else
install -d %{buildroot}%{_initddir}/ 
install -p -m 0755 etc/init.d/orchestrator.bash %{buildroot}%{_initddir}/%{repo}
%endif
install -d %{buildroot}%{_datadir}/%{repo}
cp -rpa ./resources %{buildroot}%{_datadir}/%{repo}/resources
cp -pa ./conf/orchestrator-sample.conf.json %{buildroot}%{_datadir}/%{repo}/


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
/sbin/chkconfig --add %{repo}
%endif

%preun
%if 0%{?fedora} || 0%{?rhel} == 7
%systemd_preun %{repo}.service
%else
if [ $1 = 0 ]; then
    service %{repo} stop >/dev/null 2>&1 ||:
    /sbin/chkconfig --del %{repo}
fi
%endif

%postun
%if 0%{?fedora} || 0%{?rhel} == 7
%systemd_postun %{repo}.service
%else
if [ "$1" -ge "1" ]; then
    service %{repo} condrestart > /dev/null 2>&1 ||:
fi
%endif


%files
%license LICENSE
%doc README.md
%{_sbindir}/%{repo}
%{_datadir}/%{repo}
%if 0%{?fedora} || 0%{?rhel} == 7
/usr/lib/systemd/system/%{repo}.service
%else
%{_initddir}/%{repo}
%endif

%if 0%{?with_devel} || ! 0%{?with_bundled}
%files -n golang-%{provider}-%{project}-%{repo}-devel -f devel.file-list
%license LICENSE
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files -n golang-%{provider}-%{project}-%{repo}-unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc README.md
%endif

%changelog
* Tue Mar 14 2017 Mykola Marzhan <mykola.marzhan@percona.com> - 2.0.3-1
- update to 2.0.3

* Tue Dec 13 2016 Mykola Marzhan <mykola.marzhan@percona.com> - 0.13.0-0.git006d1c7
- First package

