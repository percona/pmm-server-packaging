%define debug_package %{nil}
%global provider_aws        github
%global provider_tld_aws    com
%global project_aws         kubernetes-sigs
%global repo_aws            aws-iam-authenticator
%global provider_prefix_aws %{provider_aws}.%{provider_tld_aws}/%{project_aws}/%{repo_aws}

# the lines below are sed'ed by build-server-rpm script to set a correct version
# see: https://github.com/Percona-Lab/pmm-submodules/blob/PMM-2.0/build/bin/build-server-rpm
%global commit_aws          0000000000000000000000000000000000000000
%global shortcommit_aws     %(c=%{commit_aws}; echo ${c:0:7})

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
Source0:        https://%{provider_prefix_aws}/archive/%{commit_aws}/%{repo_aws}-%{shortcommit_aws}.tar.gz

%if %{install_golang}
BuildRequires:   golang >= 1.13.0
%endif

%description
%{summary}

%description
%{summary}


%prep
%setup -q -n %{repo_aws}-%{commit_aws}
mkdir -p ./build/src/%{provider_prefix_aws}
ln -s $(pwd) ./build/src/%{provider_prefix_aws}


%build
export GOPATH="$(pwd)/build"
export CGO_ENABLED=0
export USER=builder

cd build/src/%{provider_prefix_aws}
make build


%install
install -D -p -m 0755 ./aws-iam-authenticator %{buildroot}/opt/dbaas-tools/bin/aws-iam-authenticator
install -d %{buildroot}%{_datadir}/%{repo_aws}
install -d %{buildroot}%{_sharedstatedir}/%{repo_aws}


%files
%copying LICENSE
%doc CHANGELOG.md CONTRIBUTING.md README.md
#doc Godeps/Godeps.json
/opt/dbaas-tools/bin/aws-iam-authenticator
%{_datadir}/%{repo_aws}
%dir %attr(-, nobody, nobody) %{_sharedstatedir}/%{repo_aws}

%changelog
* Thu Aug 27 2020 Illia Pshonkin <illia.pshonkin@percona.com> - 0.5.1
- Initial packaging for dbaas-tools
