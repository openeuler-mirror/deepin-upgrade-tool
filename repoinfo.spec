Name:     repoinfo
Version:  1.0
Release:  1%{?dist}
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

install -m644 service/repoinfo.service $RPM_BUILD_ROOT/%{_unitdir}/
install -m755 src/repoinfo.py $RPM_BUILD_ROOT/%{_bindir}/repoinfo

%postun
rm -f /run/infomation/msg.txt

%post
/usr/bin/systemctl enable  repoinfo.service
/usr/bin/systemctl start   repoinfo.service

%files
%attr(0755,root,root) %{_bindir}/repoinfo
%attr(0644,root,root) %{_unitdir}/repoinfo.service

%changelog
* Thu Jue 3 2021 heyitao <heyitao@uniontech.com> - 1.0-1
- first version 
