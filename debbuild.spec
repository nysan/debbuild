# $Id: debbuild.spec 201 2015-08-03 21:36:21Z kdeugau $
# Refer to the following for more info on .spec file syntax:
#   http://www.rpm.org/max-rpm/
#   http://www.rpm.org/max-rpm-snapshot/	(Updated version of above)
#   http://docs.fedoraproject.org/drafts/rpm-guide-en/
# More links may be available from http://www.rpm.org

%bcond_without signature

Name: debbuild
Summary: Build Debian-compatible .deb packages from RPM .spec files
Version: 18.12.0

Source: https://github.com/ascherer/debbuild/archive/%{name}-%{version}.tar.gz
URL: https://github.com/ascherer/debbuild
%if %{_vendor} == "debbuild"
Group: devel
%else
Group: Development/Tools/Building
%global dist ubuntu16.04
%undefine with_signature
%define __msgfmt /usr/bin/msgfmt
%define __pod2man /usr/bin/pod2man
%endif
License: GPLv2+
Packager: Andreas Scherer <https://ascherer.github.io/>
Release: ascherer.%{dist}

Requires: dpkg-dev, perl, fakeroot
%if %{_vendor} == "debbuild"
Requires: lsb-release, gettext
Recommends: bzip2, gzip, xz-utils, unzip, zip, zstd
Recommends: git, patch, pax, quilt
%if %{with signature}
BuildRequires: gnupg
Recommends: debsigs, debsig-verify
%endif
Suggests: rpm
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

%description
%{name} attempts to build Debian-friendly semi-native packages from
RPM spec files, RPM-friendly tarballs, and RPM source packages
(.src.rpm files).  It accepts most of the options rpmbuild does, and
should be able to interpret most spec files usefully.

Note that patch is not strictly required unless you have .spec files
with %patch directives, and RPM is not required unless you wish to
rebuild .src.rpm source packages as .deb binary packages.

%prep
# Steps to unpack and patch source as needed
%setup -q

%build
# Transfer $VERSION into the live system
%{__perl} -pe "s/\@VERSION\@/%{version}/" -i debbuild

%install
# Steps to install to a temporary location for packaging
%{__rm} -rf %{buildroot}

%{__install} -d %{buildroot}%{_bindir}
%{__install} debbuild %{buildroot}%{_bindir}

%{__install} -d %{buildroot}%{_libdir}/%{name}/macros.d
%{__install} -m 644 macros/macros.in %{buildroot}%{_libdir}/%{name}/macros
%{__install} -m 644 macros/macros.perl %{buildroot}%{_libdir}/%{name}/macros.d
%{__install} -m 644 config/debrc %{buildroot}%{_libdir}/%{name}

%{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{__install} -m 644 macros/macros.sysutils %{buildroot}%{_sysconfdir}/%{name}
%{__install} -m 644 macros/macros.texlive %{buildroot}%{_sysconfdir}/%{name}

%{__install} -d %{buildroot}%{_mandir}/man8
%{__pod2man} --utf8 --center="DeepNet Dev Tools" --section 8 \
	debbuild > %{buildroot}%{_mandir}/man8/debbuild.8

%{__install} -d %{buildroot}%{_datadir}/locale/de/LC_MESSAGES
%{__msgfmt} po/de/debbuild.po -o %{buildroot}%{_datadir}/locale/de/LC_MESSAGES/debbuild.mo

%if %{with signature}
%{__install} -d %{buildroot}%{_keyringpath}/%{_gpg_key_full} \
	%{buildroot}%{_policiespath}/%{_gpg_key_full}
%{__gpg_sign_cmd}
%{__install} -m 644 gpg/debsig.pol %{buildroot}%{_policiespath}/%{_gpg_key_full}
%endif

%files
# Fill in the pathnames to be packaged here
%{_bindir}/*
%{_mandir}/man8/*
%{_libdir}/%{name}/macros
%{_libdir}/%{name}/macros.d/*
%{_sysconfdir}/%{name}/macros.*
%{_libdir}/%{name}/debrc
%{_datadir}/locale/de/LC_MESSAGES/debbuild.mo

%if %{with signature}
%attr(664,root,root) %{_keyringpath}/%{_gpg_key_full}/debsig.gpg
%{_policiespath}/%{_gpg_key_full}/debsig.pol
%endif

%changelog
* Sun Nov 11 2018  Andreas Scherer <https://ascherer.github.io/>
- Install German language pack

* Sun Feb 19 2017  Andreas Scherer <https://ascherer.github.io/>
- Set up infrastructure for signing packages

* Sat Dec  3 2016  Neal Gompa <ngompa13@gmail.com>
- Integrate platform detection into macros
- Remove unnecessary scriptlet

* Fri Oct 28 2016  Neal Gompa <ngompa13@gmail.com>
- Add lsb-release as requirement

* Sat Dec 12 2015  Andreas Scherer <https://ascherer.github.io/>
- Centrally control and distribute the 'version' number

* Fri Dec  4 2015  Neal Gompa <ngompa13@gmail.com>
- Update spec and host/build auto-configure

* Tue Nov 17 2015  Andreas Scherer <andreas_tex@freenet.de>
- Auto-configure host/build environment

* Sat Nov 14 2015  Andreas Scherer <andreas_tex@freenet.de>
- Add debbuild's own set of macros

* Sun Jul 19 2015  Kris Deugau <kdeugau@deepnet.cx>
- Remove the stack of %if's determining the Debian dist;  use the recently
  refined %{dist} instead

* Thu Feb 28 2008  Kris Deugau <kdeugau@deepnet.cx> -1
- Initial package
