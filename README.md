# PMM Server packages
## CentOS/RHEL 7
* Prepare environment
```
sudo yum -y install https://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-8.noarch.rpm
sudo yum -y install mock rpm-build rpmdevtools git
sudo usermod -a -G mock $(id -un)
git clone https://github.com/Percona-Lab/pmm-server-packaging.git
ln -s $(pwd -P)/pmm-server-packaging/rhel ~/rpmbuild
```
* Download sources
```
ls ~/rpmbuild/SPECS/*.spec | xargs -n 1 spectool -g -C ~/rpmbuild/SOURCES
```
* Build SRPMS
```
rpmbuild -bs ~/rpmbuild/SPECS/*.spec
```
* Build Go programming language rpm (build dependency for other rpms)
```
mockchain -c -r epel-7-x86_64 -l ~/result-repo ~/rpmbuild/SRPMS/golang-1.7.3-*.src.rpm
```
* Build everything
```
mockchain -c -r epel-7-x86_64 -l ~/result-repo ~/rpmbuild/SRPMS/*.src.rpm
```
* Find results
```
ls ~/result-repo/results/epel-7-x86_64/*/*.rpm
```
