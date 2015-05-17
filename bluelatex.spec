Name:		bluelatex
Version:	1.0.6
Release:	1%{?dist}
Summary:	Real-Time Collaborative Document Edition

Group:		Applications/Editors
License:	ASL 2.0
URL:		http://www.bluelatex.org	
Source0:	https://github.com/gnieh/bluelatex/archive/v%{version}.tar.gz
Source1:	build.sbt

BuildRequires:	sbt, java-devel >= 1.7, systemd
Requires:	couchdb, java >= 1.7
Requires:	texlive-collection-latexrecommended, texlive-collection-fontsrecommended
Requires:	texlive-xetex

%description
\BlueLaTeX provides a full-featured server that allows you to create, manage and
collaboratively edit documents written in \LaTeX.

%clean
rm -rf $RPM_BUILD_ROOT

%prep
%setup -q
cp %{SOURCE1} blue-dist/

%build
sbt 'project blue-dist' 'makeDistribution'

%pre
/usr/sbin/useradd -c "BlueLatex"  \
   -s /sbin/nologin -r -d /var/lib/bluelatex bluelatex 2> /dev/null || :

%install

# Creating install directories
install -d -m 0755 %{buildroot}%{_localstatedir}/log/bluelatex
install -d -m 0700 %{buildroot}%{_sharedstatedir}/bluelatex
install -d -m 0755 %{buildroot}%{_prefix}/lib/bluelatex
install -d -m 0755 %{buildroot}%{_sysconfdir}/bluelatex

# Copy stuff
pushd blue-dist/target/%{name}-%{version}

cp -r bin bundle %{buildroot}%{_prefix}/lib/bluelatex
cp -r conf/* %{buildroot}%{_sysconfdir}/bluelatex
cp -r data/* %{buildroot}%{_sharedstatedir}/bluelatex

# Systemd unit installation
install -d %{buildroot}/%{_unitdir}/
install -m 0755 init/systemd/bluelatex.service %{buildroot}/%{_unitdir}

%files
%defattr(-,root,root,-)
%dir %attr(0775,bluelatex,bluelatex)%{_localstatedir}/log/bluelatex
%attr(-,bluelatex,bluelatex)%{_sharedstatedir}/bluelatex
%config(noreplace) %attr(-,bluelatex,bluelatex)%{_sysconfdir}/bluelatex/*
%attr(-,root,root)%{_usr}/lib/bluelatex
%{_unitdir}/bluelatex.service
%doc

%changelog
* Sun May 17 2015 Olivier Bonhomme <obonhomme@nerim.net> 1.0.6-1
- Update to 1.0.6 upstream version
- Fix synchronization bug that may lead to data loss (issue #214)
- Fix file encoding bug (issue #209)

* Wed Apr 01 2015 Olivier Bonhomme <obonhomme@nerim.net> 1.0.5-1
- Update to 1.0.5 upstream version
- Fix synchronization bug that may lead to data loss (issue #188)
- Fix cursor appearing in multiple files (issue #196)
- Fix persistent cursor after an author left the paper (issue #195)
- Cleanup error and wraning upon compilation (issue #201)
- Improvements in the UI

* Sat Dec 06 2014 Olivier Bonhomme <obonhomme@nerim.net> 1.0.4-1
- Update to 1.0.4 upstream version
- Main fix: Fix Bug in the synchronization protocol on the server side, and improve the user experience on the client side.
- Fix the guarantee delivery part in case of disconnection or high latency network (issue #188)
- Hold the scroll position when several authors are editing a file concurrently (issue #185)
- Restore cursor position when changing file (issue #181)
- Fix script loading order to avoid display problems on slow networks (issue #189)
- Reenable use of standard key binings in web browser (issue #171)
- Fix PDF rendering on small displays (issue #182)

* Tue Nov 18 2014 Olivier Bonhomme <obonhomme@nerim.net> 1.0.3-1
- Update to 1.0.3 upstream version
- Add button to cleanup compilation directory (issue #173)
- Reload pdf file when compilation failed but produced a new pdf file (issue #168)
- Fix regression bug in web client making it impossible to modify user settings (issue #175)

* Wed Nov 05 2014 Olivier Bonhomme <obonhomme@nerim.net> 1.0.2-1
- Update to 1.0.2 upstream version
- Fix a regression in paper option (issue #156)
- Make 'clone' and 'report issue' links configurable (issue #161)
- Add an update script (issue #155)

* Sun Oct 12 2014 Olivier Bonhomme <obonhomme@nerim.net> 1.0.1-1 
- Update to 1.0.1 upstream version
- Improve messages (issues #138, #134)
- Disallow ":" in username (issue #139)
- Simplify the use of the web client (issue #135, #143, #146)
- Fix other small but annoying bugs
- Fix a lot of typo

* Wed Sep 24 2014 Olivier Bonhomme <obonhomme@nerim.net> 1.0.0-1 
- Initial RPM release
