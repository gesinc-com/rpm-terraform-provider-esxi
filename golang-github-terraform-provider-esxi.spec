%global	owner	josenk
%global	repo	terraform-provider-esxi
%global	host	github.com
%global	archive	v%{version}.tar.gz
%global	dir	%{repo}-%{version}
%global	namespace github.com/%{owner}/%{repo}

%global	version	1.8.1
%global	release	0.1

# emulate mock bubblewrap dependency; delete with proper source
%if %{?rhel:0}%{!?rhel:1}
%global rhel	%(rpm -qf --qf "%{version}" /etc/issue)
%endif
%if %{?dist:0}%{!?dist:1}
%global dist	el%{?rhel}%{!?rhel:0}
%endif

# Actually, don't strip at all since we are not even building debug packages
%define	__strip /bin/true
%global	debug_package	%{nil}

Name:		golang-github-%{repo}
Summary:	Terraform provider for ESXi

Version:	%{version}
Release:	%{release}
Epoch:		0

Group:		Applications/System
License:	GPL3; https://github.com/josenk

URL:		https://%{host}/%{owner}/%{repo}
Source0:	%{url}/archive/%{archive}

BuildRequires: golang make golang-golangorg-text-devel
Requires:      terraform
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Terraform provider for vSphere



%prep
%setup -q -n %{dir}

%build
export GOPATH=$PWD
export GOOS=linux
export GOARCH=amd64
#export GOFLAGS="${GOFLAGS} -modcacherw"
mkdir -p src/%{namespace}/

shopt -s extglob dotglob
mv !(src) src/%{namespace}/
shopt -u extglob dotglob
pushd src/%{namespace}/
#go get %{namespace}/something
#go get github.com/Sirupsen/logrus

make build
# overcome bizarre decision to lock files that KILLs consistency
popd ||:
chmod -fR u+rw pkg

%install
[ "%{buildroot}" = "/" ] || [ ! -d %{buildroot} ] || rm -rf %{buildroot}
install -d -m 755 %{buildroot}
install -d -m 755 %{buildroot}%{_bindir}

# install binary
%{__install} \
	src/%{namespace}/%{repo}_v%{version} \
	%{buildroot}%{_bindir}/%{repo}

%clean
[ "%{buildroot}" = "/" ] || [ ! -d %{buildroot} ] || rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
#doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/*


%changelog
# %(date +"%a %b %d %Y") $Author: build $ %{version}-%{release}
#
#  $Log$
