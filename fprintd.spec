%define long_hash  04fd09cfa88718838e02f4419befc1a0dd4b5a0e
%define short_hash 04fd09cfa

Name:		fprintd
Version:	0.1
Release:	19.git%{short_hash}%{?dist}
Summary:	D-Bus service for Fingerprint reader access

Group:		System Environment/Daemons
License:	GPLv2+
# git clone git://projects.reactivated.net/~dsd/fprintd.git
# cd fprintd
# git reset --hard %{long_hash}
# ./autogen.sh && make distcheck
# mv fprintd-0.1.tar.bz2 fprintd-0.1-%{short_hash}.tar.bz2
Source0:	fprintd-0.1-%{short_hash}.tar.bz2
Patch1:		0001-Detect-when-a-device-is-disconnected.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=498368
Patch2:		polkit1.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=543194
Patch3:		0001-Remove-all-use-of-g_error.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=553224
Patch4:		0001-Add-man-page-for-the-command-line-utilities.patch
# http://bugzilla.redhat.com/614573
Patch5:         dont-call-g-source-remove.patch

Url:		http://www.reactivated.net/fprint/wiki/Fprintd
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch:    s390 s390x

BuildRequires:	dbus-glib-devel
BuildRequires:	pam-devel
BuildRequires:	libfprint-devel >= 0.1.0
BuildRequires:	polkit-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:  autoconf automake libtool

%description
D-Bus service to access fingerprint readers.

%package pam
Summary:	PAM module for fingerprint authentication
Requires:	%{name} = %{version}-%{release}
Group:		System Environment/Base
License:	GPLv2+

%description pam
PAM module that uses the fprintd D-Bus service for fingerprint
authentication.

%package devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	gtk-doc
Group:		Development/Libraries
License:	GFDL
BuildArch:	noarch

%description devel
Development documentation for fprintd, the D-Bus service for
fingerprint readers access.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1 -b .polkit1
%patch3 -p1 -b .g_error
%patch4 -p1 -b .man
%patch5 -p1 -b .dont-call-g-source-remove

autoreconf -i -f

%build
%configure --libdir=/%{_lib}/ --enable-gtk-doc --enable-pam

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/fprint

rm -f $RPM_BUILD_ROOT/%{_lib}/security/pam_fprintd.{a,la,so.*}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README COPYING AUTHORS TODO
%{_bindir}/fprintd-*
%{_libexecdir}/fprintd
# FIXME This file should be marked as config when it does something useful
%{_sysconfdir}/fprintd.conf
%{_sysconfdir}/dbus-1/system.d/net.reactivated.Fprint.conf
%{_datadir}/dbus-1/system-services/net.reactivated.Fprint.service
%{_datadir}/polkit-1/actions/net.reactivated.fprint.device.policy
%{_localstatedir}/lib/fprint
%{_mandir}/man1/*.1.gz

%files pam
%defattr(-,root,root,-)
%doc pam/README
/%{_lib}/security/pam_fprintd.so

%files devel
%defattr(-,root,root,-)
%{_datadir}/gtk-doc/html/fprintd
%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.Device.xml
%{_datadir}/dbus-1/interfaces/net.reactivated.Fprint.Manager.xml

%changelog
* Tue Jul 27 2010 Ray Strode <rstrode@redhat.com> 0.1-19.git04fd09cfa
- Fix screensaver unlock for some users
  Resolves: #614573

* Wed May 26 2010 Bastien Nocera <bnocera@redhat.com> 0.1-18.git04fd09cfa
- Remove pam_fprint obsolete, was never shipped
- Fix devel package license
Related: rhbz#595755

* Tue Feb 16 2010 Bastien Nocera <bnocera@redhat.com> 0.1-17.git04fd09cfa
- Add man page
Related: rhbz#553224

* Wed Dec 09 2009 Bastien Nocera <bnocera@redhat.com> 0.1-16.git04fd09cfa
- Remove use of g_error(), or people think that it crashes when we actually
  abort() (#543194)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-15.git04fd09cfa
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Bastien Nocera <bnocera@redhat.com> 0.1-14.git04fd09cfa
- Merge polkit patch and fix for polkit patch

* Tue Jul 21 2009 Bastien Nocera <bnocera@redhat.com> 0.1-13.git04fd09cfa
- Make the -devel package noarch (#507698)

* Thu Jul  9 2009 Matthias Clasen <mclasen@redhat.com> 0.1-12.git04fd09cfa
- Fix the pam module (#510152)

* Sat Jun 20 2009 Bastien Nocera <bnocera@redhat.com> 0.1-11.git04fd09cfa
- Remove obsolete patch

* Tue Jun 9 2009 Matthias Clasen <mclasen@redhat.com> 0.1-10.git04fd09cfa
- Port to PolicyKit 1

* Thu May 07 2009 Bastien Nocera <bnocera@redhat.com> 0.1-9.git04fd09cfa
- Add /var/lib/fprint to the RPM to avoid SELinux errors (#499513)

* Tue Apr 21 2009 Karsten Hopp <karsten@redhat.com> 0.1-8.git04fd09cfa.1
- Excludearch s390 s390x, as we don't have libusb1 on mainframe, we can't build
  the required libfprint package

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-8.git04fd09cfa
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 - Bastien Nocera <bnocera@redhat.com> - 0.1-7.git04fd09cfa
- Add a patch to handle device disconnects

* Mon Jan 26 2009 - Bastien Nocera <bnocera@redhat.com> - 0.1-6.git04fd09cfa
- Update to latest git, fixes some run-time warnings

* Wed Dec 17 2008 - Bastien Nocera <bnocera@redhat.com> - 0.1-5.git43fe72a2aa
- Add patch to stop leaking a D-Bus connection on failure

* Tue Dec 09 2008 - Bastien Nocera <bnocera@redhat.com> - 0.1-4.git43fe72a2aa
- Update D-Bus config file for recent D-Bus changes

* Thu Dec 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.1-3.git43fe72a2aa
- Update following comments in the review

* Sun Nov 23 2008 - Bastien Nocera <bnocera@redhat.com> - 0.1-2.gitaf42ec70f3
- Update to current git master, and add documentation

* Tue Nov 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.1-1
- First package

