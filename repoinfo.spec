Name:     repoinfo
Version:  1.0
Release:  2%{?dist}
Summary:  Available package information display
License:  GPL
URL:      http://gitlabxa.uniontech.com/
Source0:  https://gitlabxa.uniontech.com/%{name}-%{version}.tar.gz

Requires: python3

%description
When the user logs in using the terminal available package information display

%prep
%setup -q

%install
install -d -m755 $RPM_BUILD_ROOT/%{_unitdir}
install -d -m755 $RPM_BUILD_ROOT/%{_bindir}
install -d -m755 $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.config/autostart/

install -m644 scripts/repoinfo.desktop $RPM_BUILD_ROOT/%{_sysconfdir}/skel/.config/autostart/
install -m644 service/repoinfo.service $RPM_BUILD_ROOT/%{_unitdir}/
install -m755 src/repoinfo.py $RPM_BUILD_ROOT/%{_bindir}/repoinfo
install -m755 src/reponotify.py $RPM_BUILD_ROOT/%{_bindir}/reponotify

%postun
rm -f /run/infomation/msg.txt
if [ -d /root/.config/autostart/ ] ;then
	rm -f /root/.config/autostart/repoinfo.desktop
fi

%post
/usr/bin/systemctl enable  repoinfo.service
/usr/bin/systemctl start   repoinfo.service
if [ -d /root/.config/autostart/ ] ;then
	cp -rf %{_sysconfdir}/skel/.config/autostart/repoinfo.desktop /root/.config/autostart/
fi

%files
%attr(0755,root,root) %{_bindir}/repoinfo
%attr(0644,root,root) %{_unitdir}/repoinfo.service
%attr(0644,root,root) %{_sysconfdir}/skel/.config/autostart/repoinfo.desktop
%attr(0755,root,root) %{_bindir}/reponotify

%changelog
* Mon Jue 7 2021 heyitao <heyitao@uniontech.com> - 1.0-2
- Add desktop user notifycations
 
* Thu Jue 3 2021 heyitao <heyitao@uniontech.com> - 1.0-1
- first version 
