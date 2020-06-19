%global debug_package %{nil}

%global gitea_user gitea

Name:           gitea
Version:        1.12.0
Release:        1%{?dist}
Summary:        Git with a cup of tea, painless self-hosted git service

License:        MIT
URL:            https://gitea.io
Source0:        %{name}-src-%{version}.tar.gz

Source10:       %{name}.service
Source11:       %{name}-sysusers.conf

BuildRequires:  systemd
BuildRequires:  golang
BuildRequires:  npm

BuildRequires:  pam-devel

Requires(pre):  shadow-utils
Requires:       git

Recommends:     git-lfs


%description
Git with a cup of tea, painless self-hosted git service.


%prep
%autosetup -c

# Change default user in sample config
sed -i "s|RUN_USER = git|RUN_USER = %{gitea_user}|" custom/conf/app.ini.sample


%build
TAGS="bindata pam sqlite sqlite_unlock_notify" %make_build


%install
install -m 0755 -Dp %{name}                     %{buildroot}%{_bindir}/%{name}
install -m 0755 -dp                             %{buildroot}%{_sharedstatedir}/%{name}

install -m 0644 -Dp custom/conf/app.ini.sample  %{buildroot}%{_sysconfdir}/%{name}/app.ini.sample
touch                                           %{buildroot}%{_sysconfdir}/%{name}/app.ini

install -m 0644 -Dp %{SOURCE10}                 %{buildroot}%{_unitdir}/%{name}.service
install -m 0644 -Dp %{SOURCE11}                 %{buildroot}%{_sysusersdir}/%{name}.conf


%pre
%sysusers_create_package %{name} %{SOURCE11}


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service



%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.conf
%config %attr(664, root, %{gitea_user}) %{_sysconfdir}/gitea/app.ini.sample
%config(noreplace) %attr(664, root, %{gitea_user}) %{_sysconfdir}/gitea/app.ini
%dir %attr(755, %{gitea_user}, %{gitea_user}) %{_sharedstatedir}/%{name}



%changelog
* Fri Jun 19 2020 ElXreno <elxreno@gmail.com> - 1.12.0-1
- Updated to version 1.12.0.
  Built with repacked original archive with fixed vendor.

* Sun May 31 2020 ElXreno <elxreno@gmail.com> - 1.11.6-1
- Updated to version 1.11.6

* Sun May 10 2020 ElXreno <elxreno@gmail.com> - 1.11.5-1
- Updated to version 1.11.5

* Mon May 04 2020 ElXreno <elxreno@gmail.com>
- Initial packaging
