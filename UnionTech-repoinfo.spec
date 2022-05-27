Name:     UnionTech-repoinfo
Version:  1.0
Release:  1
Summary:  Available package information display
License:  GPL
URL:      http://gitlabxa.uniontech.com/
Source0:  https://gitlabxa.uniontech.com/%{name}-%{version}.tar.gz

Requires: python3 logrotate
%{?systemd_requires}
Provides: repoinfo

%description
When the user logs in using the terminal available package information display

%prep
%setup -q

%install
install -d -m755 $RPM_BUILD_ROOT/%{_unitdir}
install -d -m755 $RPM_BUILD_ROOT/%{_presetdir}
install -d -m755 $RPM_BUILD_ROOT/%{_bindir}
install -d -m755 $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.config/autostart/
install -d -m755 $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/
install -d -m755 $RPM_BUILD_ROOT/root/.config/autostart/

install -m644 %{name}-%{version}/scripts/repoinfo.desktop   $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.config/autostart/
install -m644 %{name}-%{version}/scripts/repoinfo   	    $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/
install -m644 %{name}-%{version}/scripts/repoinfo.desktop   $RPM_BUILD_ROOT/root/.config/autostart/
install -m644 %{name}-%{version}/service/repoinfo.service   $RPM_BUILD_ROOT/%{_unitdir}/
install -m644 %{name}-%{version}/service/repoinfo.timer     $RPM_BUILD_ROOT/%{_unitdir}/

install -m644 %{name}-%{version}/service/98-repoinfo.preset  $RPM_BUILD_ROOT/%{_presetdir}/
install -m755 %{name}-%{version}/src/repoinfo.py $RPM_BUILD_ROOT/%{_bindir}/repoinfo
install -m755 %{name}-%{version}/src/reponotify.py $RPM_BUILD_ROOT/%{_bindir}/reponotify

%post
%systemd_post repoinfo.timer

%preun
%systemd_preun repoinfo.timer
rm -f /run/infomation/msg.txt

%postun
%systemd_postun_with_restart repoinfo.timer

%files
%attr(0755,root,root) %{_bindir}/repoinfo
%attr(0755,root,root) %{_bindir}/reponotify

%attr(0644,root,root) %{_unitdir}/repoinfo.service
%attr(0644,root,root) %{_unitdir}/repoinfo.timer
%attr(0644,root,root) %{_presetdir}/98-repoinfo.preset

%attr(0644,root,root) %{_sysconfdir}/skel/.config/autostart/repoinfo.desktop
%attr(0644,root,root) %{_sysconfdir}/logrotate.d/repoinfo
%attr(0644,root,root) /root/.config/autostart/repoinfo.desktop

%changelog
 Thu Jue 3 2021 heyitao <heyitao@uniontech.com> - 1.0-1
- display repo infomation
