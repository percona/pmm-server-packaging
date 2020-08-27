%define debug_package %{nil}
%global provider        github
%global provider_tld    com
%global project         kubernetes-sigs
%global repo            aws-iam-authenticator
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}

# the lines below are sed'ed by build-server-rpm script to set a correct version
# see: https://github.com/Percona-Lab/pmm-submodules/blob/PMM-2.0/build/bin/build-server-rpm
%global commit          0000000000000000000000000000000000000000
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%define full_pmm_version 2.0.0

%global install_golang 0

Name:           dbaas-tools
# the line below is sed'ed by build-server-rpm script to set a correct version
# see: https://github.com/Percona-Lab/pmm-submodules/blob/PMM-2.0/build/bin/build-server-rpm
Version:        %{version}
Release:        %{rpm_release}
Summary:        A set of tools for Percona DBaaS
License:        ASL 2.0
URL:            https://github.com/kubernetes-sigs/aws-iam-authenticator
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

%if %{install_golang}
BuildRequires:   golang >= 1.13.0
%endif

%description
%{summary}

%description
%{summary}


%prep
%setup -q -n %{repo}-%{commit}
mkdir -p ./build/src/%{provider_prefix}
ln -s $(pwd) ./build/src/%{provider_prefix}


%build
export GOPATH="$(pwd)/build"
export CGO_ENABLED=0
export USER=builder

cd build/src/%{provider_prefix}
make build


%install
install -D -p -m 0755 ./aws-iam-authenticator %{buildroot}/opt/dbaas-tools/bin/aws-iam-authenticator
install -d %{buildroot}%{_datadir}/%{repo}
install -d %{buildroot}%{_sharedstatedir}/%{repo}


%files
%copying LICENSE
%doc CHANGELOG.md CONTRIBUTING.md README.md
#doc Godeps/Godeps.json
/opt/dbaas-tools/bin/aws-iam-authenticator
%{_datadir}/%{repo}
%dir %attr(-, nobody, nobody) %{_sharedstatedir}/%{repo}

%changelog
* Thu Aug 27 2020 Illia Pshonkin <illia.pshonkin@percona.com> - 0.5.1
- Initial packaging for dbaas-tools
