# TODO:
# - paths (it expects that all programs are installed under common prefix /kolab)
Summary:	Kolab Groupware Server
Summary(pl):	Serwer pracy grupowej Kolab
Name:		kolab
Version:	1.0
Release:	0.1
License:	GPL
Group:		Networking/Daemons
# they say ftp://ftp.kde.org/pub/kde/unstable/server/kolab/kolab-current/ but it doesn't exist
# extracted from ftp://ftp.kde.org/pub/kde/unstable/server/kolab/kolab-server-1.0/src/kolab-1.0-1.0.3.src.rpm
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	df137e588ba7a6d23b552891391eaf81
# will be needed? maybe everything can start using their own scritps
#Source1:	%{name}.init
URL:		http://kolab.org/
Requires:	apache
Requires:	apache-mod_dav
Requires:	apache-mod_dir
Requires:	cyrus-sasl
Requires:	cyrus-imapd
Requires:	openldap
Requires:	perl-ldap
Requires:	postfix
Requires:	proftpd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/kolab
%define		_vardir		/var/lib/kolab
# to be eliminated
%define		kprefix		%{nil}

%description
Kolab is the KDE Groupware Server that provides full groupware
features to either KDE Kolab clients or Microsoft Outlook(TM) clients
running on Windows(TM) using the Konsec Konnector
(http://www.konsec.com/). In addition it is a robust and flexible
general IMAP mail server with LDAP addressbook and nice web GUI for
administration.

%description -l pl
Kolab to serwer KDE Groupware udostêpniaj±ce pe³ne mo¿liwo¶ci pracy
grupowej (groupware) klientom KDE Kolaba lub Microsoft Outlooka(TM)
pracuj±cym pod Windows(TM) z u¿yciem Konsec Konnectora
(http://www.konsec.com/). Ponadto jest to potê¿ny i elastyczny serwer
IMAP ogólnego przeznaczenia z ksi±¿k± adresow± LDAP i mi³ym graficznym
interfejsem do administrowania.

%prep
%setup -q -c

find . -type d -name CVS | xargs rm -rf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_initrddir},%{_vardir}/{log,www/{cgi-bin,freebusy,icons,locks}}}

#install %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/kolab

install {smtpd.conf,virtual,transport,aliases}.template \
	imapd.group.template \
	kolab.conf kolab.schema \
	master.cf.template php.ini.template \
	saslauthd.conf.template session_vars.php.template \
	$RPM_BUILD_ROOT%{_sysconfdir}

for f in kolab_sslcert.sh \
	cyrus.conf.template legacy.conf.template imapd.conf.template \
	kolab kolab_bootstrap \
	slapd.conf.template workaround.sh ; do
    sed -e 's,@@@kolab_prefix@@@,%{kprefix},g' $f > $RPM_BUILD_ROOT%{_sysconfdir}/$f
done
sed -e 's,@@@kolab_prefix@@@,%{kprefix},g;s,@l_nusr@,http,g;s,@l_ngrp@,http,g' httpd.conf.template \
	> $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf.template
sed -e 's,@@@kolab_prefix@@@,%{kprefix},g;s,@l_musr@,postfix,g;s,@l_rgrp@,maildrop,g;s,@l_nusr@,nobody,g' \
	main.cf.template > $RPM_BUILD_ROOT%{_sysconfdir}/main.cf.template
sed -e 's,@@@kolab_prefix@@@,%{kprefix},g;s,@l_nusr@,ftp,g;s,@l_nuid@,14,g;s,@l_ngrp@,ftp,g;s,@l_ngid@,50,g' \
	proftpd.conf.template > $RPM_BUILD_ROOT%{_sysconfdir}/proftpd.conf.template

cp -rf admin $RPM_BUILD_ROOT%{_vardir}/www

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "For a fresh install please initialize Kolab and run '%{_sysconfdir}/kolab_bootstrap -b'."
echo "If you upgraded from a previous version simply refresh Kolab and run '%{_sysconfdir}/kolab -o -v'."
echo "In every case execute '%{_initrddir}/kolab restart'"

%files
%defattr(644,root,root,755)
#%attr(754,root,root) %{_initrddir}/kolab
%dir %{_sysconfdir}
%attr(744,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/kolab_sslcert.sh
%attr(744,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/kolab
%attr(744,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/kolab_bootstrap
%attr(744,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/workaround.sh
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/smtpd.conf.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/virtual.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/aliases.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/transport.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/cyrus.conf.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd.conf.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/legacy.conf.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/imapd.conf.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/imapd.group.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/kolab.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/kolab.schema
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/main.cf.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/master.cf.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/php.ini.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/proftpd.conf.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/saslauthd.conf.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/session_vars.php.template
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/slapd.conf.template

%dir %{_vardir}
%dir %{_vardir}/log
%dir %{_vardir}/www
%{_vardir}/www/admin
%dir %{_vardir}/www/cgi-bin
%attr(775,http,http) %dir %{_vardir}/www/freebusy
%dir %{_vardir}/www/icons
%attr(775,http,http) %dir %{_vardir}/www/locks
