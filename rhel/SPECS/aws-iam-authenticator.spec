%define debug_package %{nil}
%global provider        github
%global provider_tld    com
%global project         kubernetes-sigs
%global repo            aws-iam-authenticator
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          d7c0b2e9131faabb2b09dd804a35ee03822f8447
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%global install_golang 0

Name:           %{repo}
Version:        0.5.1
Release:        1%{?dist}
Summary:        A tool to use AWS IAM credentials to authenticate to a Kubernetes cluster
License:        ASL 2.0
URL:            https://%{provider_prefix}
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
install -D -p -m 0755 ./%{repo}  %{buildroot}%{_sbindir}/%{repo}
install -D -p -m 0755 ./aws-iam-authenticator %{buildroot}%{_bindir}/aws-iam-authenticator
install -d %{buildroot}%{_datadir}/%{repo}
install -d %{buildroot}%{_sharedstatedir}/%{repo}


%files
%copying LICENSE
%doc CHANGELOG.md CONTRIBUTING.md README.md
#doc Godeps/Godeps.json
%{_sbindir}/%{repo}
%{_bindir}/aws-iam-authenticator
%{_datadir}/%{repo}
%dir %attr(-, nobody, nobody) %{_sharedstatedir}/%{repo}

%changelog
* Wed Aug 26 2020 Illia Pshonkin <illia.pshonkin@percona.com> - 0.5.1-1
- Initial packaging for aws-iam-authenticator
