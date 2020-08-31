%define debug_package %{nil}

%global project_aws         kubernetes-sigs
%global repo_aws            aws-iam-authenticator
%global provider_prefix_aws github.com/%{project_aws}/%{repo_aws}
%global commit_aws          d7c0b2e9131faabb2b09dd804a35ee03822f8447
%global shortcommit_aws     %(c=%{commit_aws}; echo ${c:0:7})

%define full_pmm_version 2.0.0
%global install_golang 1

%define build_timestamp %(date -u +"%y%m%d%H%M")
%define release         1
%define rpm_release     %{release}.%{build_timestamp}%{?dist}

Name:           dbaas-tools
# the line below is sed'ed by build-server-rpm script to set a correct version
# see: https://github.com/Percona-Lab/pmm-submodules/blob/PMM-2.0/build/bin/build-server-rpm
Version:        0.5.1
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

cd build/src/%{provider_prefix_aws}/%{repo_aws}-%{commit_aws}
sed -i '/dockers:/,+35d' .goreleaser.yaml
make build


%install
install -D -p -m 0755 ./dist/authenticator_linux_amd64/%{repo_aws} %{buildroot}/opt/dbaas-tools/bin/%{repo_aws}


%files
%license LICENSE.md
%doc CONTRIBUTING.md README.md
/opt/dbaas-tools/bin/%{repo_aws}

%changelog
* Thu Aug 27 2020 Illia Pshonkin <illia.pshonkin@percona.com> - 0.5.1-1
- Initial packaging for dbaas-tools

