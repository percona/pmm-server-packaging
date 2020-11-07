# PMM Server packages
[![CLA assistant](https://cla-assistant.percona.com/readme/badge/percona/pmm-server-packaging)](https://cla-assistant.percona.com/percona/pmm-server-packaging)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fpercona%2Fpmm-server-packaging.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fpercona%2Fpmm-server-packaging?ref=badge_shield)
## CentOS/RHEL 7
* Prepare environment
```
sudo yum -y install https://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-8.noarch.rpm
sudo yum -y install mock rpm-build rpmdevtools git
sudo usermod -a -G mock $(id -un)
```
* Download sources
```
ls rhel/SPECS/*.spec | xargs -n 1 spectool -g -C rhel/SOURCES
```
* Build SRPMS
```
rpmbuild --define "_topdir rhel" -bs rhel/SPECS/*.spec
```
* Build Go programming language rpm (build dependency for other rpms)
```
mockchain -c -r epel-7-x86_64 -l result-repo rhel/SRPMS/golang-1.7.3-*.src.rpm
```
* Build everything
```
mockchain -c -r epel-7-x86_64 -l result-repo rhel/SRPMS/*.src.rpm
```
* Find results
```
ls result-repo/results/epel-7-x86_64/*/*.rpm
```


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fpercona%2Fpmm-server-packaging.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fpercona%2Fpmm-server-packaging?ref=badge_large)