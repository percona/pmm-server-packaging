%define debug_package %{nil}

%global commit_aws          d7c0b2e9131faabb2b09dd804a35ee03822f8447
%global shortcommit_aws     %(c=%{commit_aws}; echo ${c:0:7})

%global install_golang 1

%define build_timestamp %(date -u +"%y%m%d%H%M")
%define release         2
%define rpm_release     %{release}.%{build_timestamp}%{?dist}

Name:           dbaas-tools
Version:        0.5.1
Release:        %{rpm_release}
Summary:        A set of tools for Percona DBaaS
License:        ASL 2.0
URL:            https://github.com/kubernetes-sigs/aws-iam-authenticator
Source0:        https://github.com/kubernetes-sigs/aws-iam-authenticator/archive/%{commit_aws}/aws-iam-authenticator-%{shortcommit_aws}.tar.gz

%if %{install_golang}
BuildRequires:   golang >= 1.13.0
%endif

%description
%{summary}

%description
%{summary}


%prep
%setup -T -c -n aws-iam-authenticator-%{commit_aws}
%setup -q -c -a 0 -n aws-iam-authenticator-%{commit_aws}
mkdir -p src/github.com/kubernetes-sigs/
mv aws-iam-authenticator-%{commit_aws} src/github.com/kubernetes-sigs/aws-iam-authenticator-%{commit_aws}


%build
export GOPATH="$(pwd)"
export CGO_ENABLED=0
export USER=builder

cd src/github.com/kubernetes-sigs/aws-iam-authenticator-%{commit_aws}
sed -i '/dockers:/,+35d' .goreleaser.yaml
make build


%install
install -D -p -m 0755 src/github.com/kubernetes-sigs/aws-iam-authenticator-%{commit_aws}/dist/authenticator_linux_amd64/aws-iam-authenticator %{buildroot}/opt/dbaas-tools/bin/aws-iam-authenticator


%files
%license src/github.com/kubernetes-sigs/aws-iam-authenticator-%{commit_aws}/LICENSE
%doc src/github.com/kubernetes-sigs/aws-iam-authenticator-%{commit_aws}/CONTRIBUTING.md src/github.com/kubernetes-sigs/aws-iam-authenticator-%{commit_aws}/README.md
/opt/dbaas-tools/bin/aws-iam-authenticator

%changelog
* Thu Aug 27 2020 Illia Pshonkin <illia.pshonkin@percona.com> - 0.5.1-1
- Initial packaging for dbaas-tools

