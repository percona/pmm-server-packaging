%global with_debug   0

%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%global commit                  v1.16.8
%global commit_noprefix         %(c=%{commit}; echo ${c#v})
%global shortcommit             %(c=%{commit}; echo ${c:0:7})

%global install_golang 0

# Needed otherwise "version_ldflags=$(kube::version_ldflags)" doesn't work
%global _buildshell  /bin/bash
%global _checkshell  /bin/bash


Name:           dbaas-kubectls
Version:        1.16.8
Release:        1%{?dist}
Summary:        CLI client for Kubernetes
License:        ASL 2.0
URL:            https://github.com/kubernetes/kubernetes
ExclusiveArch:  x86_64 %{arm}
Source0:        https://github.com/kubernetes/kubernetes/archive/%{commit}/%{shortcommit}.tar.gz

%if %{install_golang}
BuildRequires: golang >= 1.12.0
%endif
BuildRequires: go-bindata
# which is not installed in official docker image
BuildRequires: which

%description
Kubernetes client tools


%prep
%setup -q -n kubernetes-%{commit_noprefix}

mkdir -p src/k8s.io/kubernetes
mv $(ls | grep -v "^src$") src/k8s.io/kubernetes/.

%build
pushd src/k8s.io/kubernetes/
export KUBE_GIT_TREE_STATE="clean"
export KUBE_GIT_COMMIT=%{commit}
export KUBE_GIT_VERSION=v{version}
export KUBE_EXTRA_GOPATH=$(pwd)/Godeps/_workspace

make WHAT="cmd/kubectl"


%install
pushd src/k8s.io/kubernetes/
. hack/lib/init.sh
kube::golang::setup_env

%ifarch ppc64le
output_path="_output/local/go/bin"
%else
output_path="${KUBE_OUTPUT_BINPATH}/$(kube::golang::host_platform)"
%endif

echo "+++ INSTALLING binaries"
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} ${output_path}/kubectl
mv %{buildroot}%{_bindir}/kubectl %{buildroot}%{_bindir}/dbaas-kubectl-1.16
popd

mv src/k8s.io/kubernetes/*.md .
mv src/k8s.io/kubernetes/LICENSE .

%check
if [ 1 != 1 ]; then
echo "******Testing the commands*****"
hack/test-cmd.sh
echo "******Benchmarking kube********"
hack/benchmark-go.sh

# In Fedora 20 and RHEL7 the go cover tools isn't available correctly
echo "******Testing the go code******"
hack/test-go.sh
echo "******Testing integration******"
hack/test-integration.sh --use_go_build
fi

%files
%license LICENSE
%doc *.md
%{_bindir}/dbaas-kubectl-1.16

############################################
%changelog
* Tue Aug 11 2020 Mykyta Solomko <mykyta.solomko@percona.com> - 1.16.8-1
- Initial import from Fedora Project and modifications

