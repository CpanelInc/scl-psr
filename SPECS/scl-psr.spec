%define debug_package %{nil}
%define _enable_debug_packages %{nil}

%{?scl:%global _scl_prefix /opt/cpanel}
%{!?scl:%global pkg_name %{name}}

%scl_package %scl

# This makes the ea-php<ver>-build macro stuff work
%scl_package_override

# must redefine this in the spec file because OBS doesn't know how
# to handle macros in BuildRequires statements
%{?scl:%global scl_prefix %{scl}-}

# Package namespaces
%global ns_name ea
%global ns_dir /opt/cpanel
%global _scl_prefix %ns_dir

# OBS builds the 32-bit targets as arch 'i586', and more typical
# 32-bit architecture is 'i386', but 32-bit archive is named 'x86'.
# 64-bit archive is 'x86-64', rather than 'x86_64'.
%if "%{_arch}" == "i586" || "%{_arch}" == "i386"
%global archive_arch x86
%else
%if "%{_arch}" == "x86_64"
%global archive_arch x86-64
%else
%global archive_arch %{_arch}
%endif
%endif

Name:    %{?scl_prefix}php-psr
Vendor:  cPanel, Inc.
Summary: This PHP extension provides the interfaces from the PSR standards as established by the PHP-FIG group.
Version: 1.2.0
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 3
Release: %{release_prefix}%{?dist}.cpanel
License: PHP
Group:   Development/Languages
URL: https://github.com/jbboehr/php-psr

#### https://fedoraproject.org/wiki/Packaging:SourceURL?rd=Packaging/SourceURL#Git_Hosting_Services
#### Source: https://github.com/phalcon/cphalcon/archive/v%{version}.tar.gz
#### does not work :(
Source: jbboehr-php-psr-1.2.0-0-ge068927.tar.gz
Source1: psr.ini
BuildRequires: scl-utils-build
BuildRequires: %{?scl_prefix}scldevel
BuildRequires: %{?scl_prefix}build
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: automake, libtool

%if 0%{rhel} > 6
BuildRequires: autoconf
%else
BuildRequires: autotools-latest-autoconf
%endif

Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Requires:      %{scl} %{?scl_prefix}php-cli

%description
This PHP extension provides the interfaces from the PSR standards as established by the PHP-FIG group.

%prep
%setup -n jbboehr-php-psr-60193fd
#### ^^^ [GitHub]

%build

%{_scl_root}/usr/bin/phpize --php-config %{_scl_root}/usr/bin/php-config
./configure --with-php-config=%{_scl_root}/usr/bin/php-config
make
make test

%install

echo $RPM_BUILD_ROOT/%{php_extdir}
mkdir -p $RPM_BUILD_ROOT/%{php_extdir}
mkdir -p $RPM_BUILD_ROOT/%{_scl_root}/usr/include/php/ext/psr

install modules/psr.so $RPM_BUILD_ROOT/%{php_extdir}/psr.so

mkdir -p $RPM_BUILD_ROOT/%{_scl_root}/etc/php.d/
install %{SOURCE1} $RPM_BUILD_ROOT/%{_scl_root}/etc/php.d/20-psr.ini

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{php_extdir}/psr.so
%dir %{_scl_root}/usr/include/php/ext/psr
%config(noreplace) %attr(644,root,root) %{_scl_root}/etc/php.d/20-psr.ini

%changelog
* Wed May 17 2023 Dan Muey <dan@cpanel.net> - 1.2.0-3
- ZC-10950: Add debug_package nil back w/ second directive (3rd item will be ZC-10951)

* Wed May 10 2023 Brian Mendoza <brian.mendoza@cpanel.net> - 1.2.0-2
- ZC-10936: Clean up Makefile and remove debug-package-nil

* Mon Dec 13 2021 Cory McIntire <cory@cpanel.net> - 1.2.0-1
- EA-10351: Update scl-psr from v1.1.0 to v1.2.0

* Fri Apr 23 2021 Cory McIntire <cory@cpanel.net> - 1.1.0-1
- EA-9712: Update scl-psr from v1.0.1 to v1.1.0

* Sun Nov 29 2020 Cory McIntire <cory@cpanel.net> - 1.0.1-1
- EA-9452: Update scl-psr from v1.0.0 to v1.0.1

* Mon Apr 06 2020 Julian Brown <julian.brown@cpanel.net> - 1.0.0-2
- ZC-6345: Add PHP74

* Wed Mar 04 2020 Tim Mullin <tim@cpanel.net> - 1.0.0-1
- EA-8903: Update to v1.0.0

* Mon Aug 26 2019 Julian Brown <julian.brown@cpanel.net> - 0.7.0-2
- ZC-5473 no longer building for php70 and php71

* Tue Aug 20 2019 Julian Brown <julian.brown@cpanel.net> - 0.7.0-1
- ZC-5448 created from source

