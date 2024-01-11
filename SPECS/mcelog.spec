Summary:	Tool to translate x86-64 CPU Machine Check Exception data
Name:		mcelog
Version:	194
Release:	1%{?dist}
Epoch:		3
Group:		System Environment/Base
License:	GPLv2
URL:		https://github.com/andikleen/mcelog
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# note that this source OVERRIDES the one on the tarball above!
Source1:	mcelog.conf
Source2:	mcelog.service
Patch0:		mcelog-annocheck-gcc-flags.patch
ExclusiveArch:	i686 x86_64
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd

%description
mcelog is a utility that collects and decodes Machine Check Exception data
on x86-32 and x86-64 systems.

%prep
%autosetup

%build
%set_build_flags

# automatically populate the .os_version file so that "mcelog --version"
# returns a valid value instead of "unknown"
echo "%{version}-%{release}" > .os_version
make CFLAGS="$RPM_OPT_FLAGS -fpie -pie" %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man{5,8}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
install -p -m755 mcelog $RPM_BUILD_ROOT/%{_sbindir}/mcelog
install -p -m644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/mcelog.conf
install -p -m755 triggers/cache-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/cache-error-trigger
install -p -m755 triggers/dimm-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/dimm-error-trigger
install -p -m755 triggers/page-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/page-error-trigger
install -p -m755 triggers/socket-memory-error-trigger $RPM_BUILD_ROOT/%{_sysconfdir}/mcelog/triggers/socket-memory-error-trigger
install -p -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_unitdir}/mcelog.service
install -p -m644 mcelog*.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
install -p -m644 mcelog*.5 $RPM_BUILD_ROOT/%{_mandir}/man5/

%post
%systemd_post mcelog.service

%preun
%systemd_preun mcelog.service

%postun
%systemd_postun_with_restart mcelog.service

%files
%{_sbindir}/mcelog
%dir %{_sysconfdir}/mcelog
%{_sysconfdir}/mcelog/triggers
%config(noreplace) %{_sysconfdir}/mcelog/mcelog.conf
%{_unitdir}/mcelog.service
%{_mandir}/*/*

%changelog
* Thu Jun  8 2023 Prarit Bhargava <prarit@redhat.com> - 3:194.1
- Add tests
* Mon Jun  5 2023 Prarit Bhargava <prarit@redhat.com> - 3:194.0
- Add support for EMR
* Fri Sep  2 2022 Prarit Bhargava <prarit@redhat.com> - 3:189-0
- Add support for RPL-P, RPL-S, ADL-N
* Fri Jun 24 2022 Prarit Bhargava <prarit@redhat.com> - 3:182-1
- Update local copy of mcelog.conf [2094574]
* Mon Jun 13 2022 Prarit Bhargava <prarit@redhat.com> - 3:182-0
- Change CE threshhold from 10/day to 2/day [2094574]
* Wed Mar  9 2022 Prarit Bhargava <prarit@redhat.com> - 3:180-0
- update to v180 [1971908]
* Mon Oct 11 2021 Prarit Bhargava <prarit@redhat.com> - 3:176-1
- update to v179 [1971908]
* Tue Aug  3 2021 Prarit Bhargava <prarit@redhat.com> - 3:175-1
- Rebuild for binutils [1954439]
* Wed Apr  7 2021 Prarit Bhargava <prarit@redhat.com> - 3:175-0
- Update to v175 [1921751]
- adds support for Sapphire Rapids [1838392]
* Mon Nov 16 2020 Prarit Bhargava <prarit@redhat.com> - 3:173-0
- Update to v173
- adds support for Tigerlake, Rocketlake, Alderlake, Lakefield
- adds support for CometLake, Icelake server, Icelake-D, and Snow Ridge
* Mon Jun  1 2020 Prarit Bhargava <prarit@redhat.com> - 3:166-0
- Add support for Icelake Server [1783101]
* Tue Dec 10 2019 Prarit Bhargava <prarit@redhat.com> - 3:165-0
- Add support for Icelake [1485541]
* Mon Apr  1 2019 Prarit Bhargava <prarit@redhat.com> - 3:162-2
- Fix version string [1692974]
* Fri Mar 29 2019 Prarit Bhargava <prarit@redhat.com> - 3:160-1
- Deduce channel number for Haswell/Broadwell/Skylake systems [1641046]
- Add decoding for Optane DC persistent memory mode [1645344]
* Mon Sep 24 2018 Prarit Bhargava <prarit@redhat.com> - 3:159-2
- fix annocheck gcc failures [1624140]

* Thu Aug 02 2018 Prarit Bhargava <prarit@redhat.com> - 3:159-1
- update to v159

* Mon Aug 21 2017 Prarit Bhargava <prarit@redhat.com> - 3:153-1
- Update to v153

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:137-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:137-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:137-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu May 26 2016 Adam Williamson <awilliam@redhat.com> - 3:137-1
- update to latest upstream release tag

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3:119-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3:119-1
- Update to latest upstream tag
- Drop cron job (#1066659)
- Remove double starting of daemon

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:101-2.9bfaad8f92c5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Dec 18 2014 Prarit Bhargava <prarit@redhat.com> 3:101-1.9bfaad8f92c5
- Update to 101 (#1175832)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2:1.0-0.13.f0d7654
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2:1.0-0.12.f0d7654
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Prarit Bhargava <prarit@redhat.com> 2:1.0-0.11.f0d7654
- remaining scriptlets replaced with new systemd macros (#850199)

* Mon Aug 12 2013 Prarit Bhargava <prarit@redhat.com> 2:1.0-0.10.f0d7654
- updated to latest mcelog
- removed mcelog-fix-trigger-path-and-cacheing.patch. AFAICT triggers are
  correctly installed
- added mcelog-disable-cron-job.patch as mcelog runs in daemon mode by
  default in Fedora
* Sun Aug  4 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2:1.0-0.9.6e4e2a00
- Fix FBTFS, modernise spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.8.6e4e2a00
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.7.6e4e2a00
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.6.6e4e2a00
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Jon Ciesla <limburgher@gmail.com> - 2:1.0-0.5.6e4e2a00
- Merge review fixes, BZ 226132.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.4.6e4e2a00
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Prarit Bhargava <prarit@redhat.com> 2:1.0-0.3.6e4e2a00
- Updated sources to deal with various warning issues [701083] [704302]
- Update URL for new location of Andi's mcelog tree
- Update n-v-r to include latest git hash

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-0.3.pre3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 10 2010 Jon Masters <jcm@redhat.com> 2:1.0-0.2.pre3
- Rework mcelog to use daemon mode and systemd.

* Tue Nov 09 2010 Jon Masters <jcm@redhat.com> 2:1.0-0.1.pre3
- Bump epoch and use standard Fedora Packaging Guidelines for NVR.
- Switch to using signed bz2 source and remove dead patch.

* Fri Sep 17 2010 Dave Jones <davej@redhat.com> 1:1.0pre3-0.1
- Update to upstream mcelog-1.0pre3

* Mon Oct 05 2009 Orion Poplawski <orion@cora.nwra.com> - 1:0.9pre1-0.1
- Update to 0.9pre1
- Update URL
- Add patch to update mcelog kernel record length (bug #507026)

* Tue Aug 04 2009 Adam Jackson <ajax@redhat.com> 0.7-5
- Fix %%install for new buildroot cleanout.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.7-2
- fix license tag
- clean this package up

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:0.7-1.22
- Autorebuild for GCC 4.3

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com>
- Rebuild.

* Fri Jun 30 2006 Dave Jones <davej@redhat.com>
- Rebuild. (#197385)

* Wed May 17 2006 Dave Jones <davej@redhat.com>
- Update to upstream 0.7
- Change frequency to hourly instead of daily.

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Wed Feb  8 2006 Dave Jones <davej@redhat.com>
- Update to upstream 0.6

* Mon Dec 19 2005 Dave Jones <davej@redhat.com>
- Update to upstream 0.5

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Wed Feb  9 2005 Dave Jones <davej@redhat.com>
- Update to upstream 0.4

* Thu Jan 27 2005 Dave Jones <davej@redhat.com>
- Initial packaging.

