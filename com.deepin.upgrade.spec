%global         pypi_name  com_deepin_upgrade
Name:           com.deepin.upgrade
Version:        1.2
Release:        1
Summary:        Deepin upgrade tool
License:        GPL-3.0-only
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel python3dist(setuptools) desktop-file-utils gettext systemd
Requires:       python3 logrotate python3-PyQt5-base python3dist(psutil) dde-control-center
%{?systemd_requires}
Provides:       UnionTech-repoinfo
Obsoletes:      UnionTech-repoinfo <= 1.0

%description
Deepin upgrade tool, when the user logs in, an updatable application pop-up window
will pop up. Through the pop-up window, you can open the Software Updater and select
the software to update.

%prep
%autosetup -p1

%build
%py3_build
%{make_build}

%install
%py3_install
%{make_install}

%find_lang %{name}

%post
%systemd_post pkgs-upgrade-info.timer
systemctl start pkgs-upgrade-info.timer >/dev/null 2>&1 || :
%preun
%systemd_preun repoinfo.timer >/dev/null 2>&1 || :
%systemd_preun pkgs-upgrade-info.timer
%{__rm} -rf /var/infomation

%postun
%systemd_postun_with_restart pkgs-upgrade-info.timer


%files -f %{name}.lang
%{_sysconfdir}/logrotate.d/%{pypi_name}
%{_sysconfdir}/skel/.config/autostart/pkgs_upgrade_notify.desktop
/root/.config/autostart/pkgs_upgrade_notify.desktop
%{_bindir}/pkgs_install_tool
%{_bindir}/pkgs_upgrade_count
%{_bindir}/pkgs_upgrade_info
%{_bindir}/pkgs_upgrade_notify
%{_bindir}/pkgs_upgrade_window
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}*egg*
%{_presetdir}/98-pkgs-upgrade-info.preset
%{_unitdir}/pkgs-upgrade-info.service
%{_unitdir}/pkgs-upgrade-info.timer
%{_datadir}/applications/pkgs_upgrade_window.desktop
%{_datadir}/polkit-1/actions/org.deepin.pkexec.deepin-upgrade.policy
%{_sharedstatedir}/pkgs_upgrade


%changelog
* Thu Jul 31 2025 zhouyuanyuan <2535682878@qq.com> - 1.2-1
- Update 1.2

* Wed Jan 05 2022 weidong <weidong@uniontech.com> - 1.1-5
- Delete reminder desktop
- Optimize DBUS judgment

* Tue Dec 28 2021 weidong <weidong@uniontech.com> - 1.1-4
- Bugfix bug-view-109558 bug-view-109559

* Mon Dec 13 2021 weidong <weidong@uniontech.com> - 1.1-3
- Update installation dependencies
- Update readme package name
- Add pkexec reminder configuration

* Mon Nov 22 2021 weidong <weidong@uniontech.com> - 1.1-2
- Support internationalization
- Optimize security selection window
- Optimize directory structure

* Thu Oct 21 2021 weidong <weidong@uniontech.com> - 1.1-1
- Update 1.1
- Add update window

* Fri Aug 27 2021 heyitao <heyitao@uniontech.com> - 1.0-2
- modify the title of the notify tip

* Thu Jue 3 2021 heyitao <heyitao@uniontech.com> - 1.0-1
- display repo infomation

