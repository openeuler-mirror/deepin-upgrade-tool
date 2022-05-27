Name:           UnionTech-repoinfo
Version:        2.0
Release:        1
Summary:        Available package information display
License:        GPL
URL:            http://gitlabxa.uniontech.com/
Source0:        https://gitlabxa.uniontech.com/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel python3dist(setuptools)
Requires:       python3 logrotate python3-PyQt5-base
%{?systemd_requires}
Provides:       repoinfo

%description
When the user logs in using the terminal available package information display

%prep
%autosetup -p1

%build
%py3_build

%install
%py3_install
install -d -m755 $RPM_BUILD_ROOT/%{_unitdir}
install -d -m755 $RPM_BUILD_ROOT/%{_presetdir}
install -d -m755 $RPM_BUILD_ROOT/%{_bindir}
install -d -m755 $RPM_BUILD_ROOT/%{_datarootdir}/repoinfo

install -d -m755 $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.config/autostart/
install -d -m755 $RPM_BUILD_ROOT/%{_datadir}/applications/
install -d -m755 $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/
install -d -m755 $RPM_BUILD_ROOT/root/.config/autostart/

install -m644 scripts/repoinfo.desktop   $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.config/autostart/
install -m644 scripts/repoinfo.desktop   $RPM_BUILD_ROOT/%{_datadir}/applications/
install -m644 scripts/repoinfo              $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/
install -m644 scripts/repoinfo.desktop   $RPM_BUILD_ROOT/root/.config/autostart/
install -m644 service/repoinfo.service   $RPM_BUILD_ROOT/%{_unitdir}/
install -m644 service/repoinfo.timer     $RPM_BUILD_ROOT/%{_unitdir}/
#install -m644 img/notify.png             $RPM_BUILD_ROOT/%{_datarootdir}/repoinfo/

install -m644 service/98-repoinfo.preset  $RPM_BUILD_ROOT/%{_presetdir}/
#install -m755 src/repoinfo.py $RPM_BUILD_ROOT/%{_bindir}/repoinfo
#install -m755 src/reponotify.py $RPM_BUILD_ROOT/%{_bindir}/reponotify

%post
%systemd_post repoinfo.timer

%preun
%systemd_preun repoinfo.timer
rm -f /var/infomation/msg.txt

%postun
%systemd_postun_with_restart repoinfo.timer

%files
#attr(0755,root,root) {_bindir}/repoinfo
#attr(0755,root,root) {_bindir}/reponotify

%attr(0644,root,root) %{_unitdir}/repoinfo.service
%attr(0644,root,root) %{_unitdir}/repoinfo.timer
%attr(0644,root,root) %{_presetdir}/98-repoinfo.preset
#attr(0644,root,root) {_datarootdir}/repoinfo/notify.png

%attr(0644,root,root) %{_sysconfdir}/skel/.config/autostart/repoinfo.desktop
%attr(0644,root,root) %{_datadir}/applications/repoinfo.desktop
%attr(0644,root,root) %{_sysconfdir}/logrotate.d/repoinfo
%attr(0644,root,root) /root/.config/autostart/repoinfo.desktop
%{_bindir}/*
%{python3_sitelib}/*

%changelog
* Thu Oct 21 2021 weidong <weidong@uniontech.com> - 2.0-1
- Update 2.0

* Fri Aug 27 2021 heyitao <heyitao@uniontech.com> - 1.0-2
- modify the title of the notify tip

* Thu Jue 3 2021 heyitao <heyitao@uniontech.com> - 1.0-1
- display repo infomation

