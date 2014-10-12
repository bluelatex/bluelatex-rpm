Name:		bluelatex
Version:	1.0.1
Release:	1%{?dist}
Summary:	Real-Time Collaborative Document Edition

Group:		Applications/Editors
License:	ASL 2.0
URL:		http://www.bluelatex.org	
Source0:	https://github.com/gnieh/bluelatex/archive/v1.0.1.tar.gz
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
* Sun Oct 12 2014 Olivier Bonhomme <obonhomme@nerim.net> 1.0.1-1 
- Update to 1.0.1 upstream version
- Improve messages (issues #138, #134)
- Disallow ":" in username (issue #139)
- Simplify the use of the web client (issue #135, #143, #146)
- Fix other small but annoying bugs
- Fix a lot of typo

* Wed Sep 24 2014 Olivier Bonhomme <obonhomme@nerim.net> 1.0.0-1 
- Initial RPM release
