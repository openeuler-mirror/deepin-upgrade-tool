Name:           com.deepin.upgrade
Version:        1.1
Release:        2
Summary:        Deepin upgrade tool
License:        GPLv3
URL:            http://gitlabxa.uniontech.com/
Source0:        https://gitlabxa.uniontech.com/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel python3dist(setuptools)
Requires:       python3 logrotate python3-PyQt5-base python3dist(psutil) dde
%{?systemd_requires}
Provides:       UnionTech-repoinfo
Obsoletes:      UnionTech-repoinfo

%description
Deepin upgrade tool, when the user logs in, an updatable application pop-up window
will pop up. Through the pop-up window, you can open the Software Updater and select
the software to update

%prep
%autosetup -p1

%build
%py3_build

%install
%py3_install
install -d -m755 $RPM_BUILD_ROOT/%{_unitdir}
install -d -m755 $RPM_BUILD_ROOT/%{_presetdir}
install -d -m755 $RPM_BUILD_ROOT/%{_bindir}
install -d -m755 $RPM_BUILD_ROOT/%{_datarootdir}/pkgs_upgrade_info

install -d -m755 $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.config/autostart/
install -d -m755 $RPM_BUILD_ROOT/%{_datadir}/applications/
install -d -m755 $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/
install -d -m755 $RPM_BUILD_ROOT/root/.config/autostart/

install -m644 scripts/pkgs_upgrade_notify.desktop   $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.config/autostart/
install -m644 scripts/pkgs_upgrade_notify.desktop   $RPM_BUILD_ROOT/%{_datadir}/applications/
install -m644 scripts/pkgs_upgrade_window.desktop   $RPM_BUILD_ROOT/%{_datadir}/applications/

install -m644 scripts/com_deepin_upgrade              $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/
install -m644 scripts/pkgs_upgrade_notify.desktop   $RPM_BUILD_ROOT/root/.config/autostart/
install -m644 service/pkgs-upgrade-info.service   $RPM_BUILD_ROOT/%{_unitdir}/
install -m644 service/pkgs-upgrade-info.timer     $RPM_BUILD_ROOT/%{_unitdir}/

install -m644 service/98-pkgs-upgrade-info.preset  $RPM_BUILD_ROOT/%{_presetdir}/

%post
%systemd_post pkgs-upgrade-info.timer

%preun
%systemd_preun pkgs-upgrade-info.timer
if [ -f "/var/infomation/msg.txt" ];then
	rm -f /var/infomation
fi



%postun
%systemd_postun_with_restart pkgs-upgrade-info.timer

%files
%attr(0644,root,root) %{_unitdir}/pkgs-upgrade-info.service
%attr(0644,root,root) %{_unitdir}/pkgs-upgrade-info.timer
%attr(0644,root,root) %{_presetdir}/98-pkgs-upgrade-info.preset

%attr(0644,root,root) %{_sysconfdir}/skel/.config/autostart/pkgs_upgrade_notify.desktop
%attr(0644,root,root) %{_datadir}/applications/pkgs_upgrade_notify.desktop
%attr(0644,root,root) %{_datadir}/applications/pkgs_upgrade_window.desktop

%attr(0644,root,root) %{_sysconfdir}/logrotate.d/com_deepin_upgrade
%attr(0644,root,root) /root/.config/autostart/pkgs_upgrade_notify.desktop
%{_bindir}/*
%{_datadir}/*
%{python3_sitelib}/*

%changelog
* Mon Nov 22 2021 weidong <weidong@uniontech.com> - 1.1-2
- Support internationalization
- Optimize security selection window

* Thu Oct 21 2021 weidong <weidong@uniontech.com> - 1.1-1
- Update 1.1
- Add update window

* Fri Aug 27 2021 heyitao <heyitao@uniontech.com> - 1.0-2
- modify the title of the notify tip

* Thu Jue 3 2021 heyitao <heyitao@uniontech.com> - 1.0-1
- display repo infomation

