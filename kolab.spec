# TODO:
# - paths (it expects that all programs are installed under common prefix /kolab)
%define		_kolabd_ver 1.9.4
%define		_build_date 20050913
#
Summary:	Kolab Groupware Server
Summary(pl):	Serwer pracy grupowej Kolab
Name:		kolab
Version:	2.0.1
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons
Source0:	ftp://ftp.belnet.be/packages/kolab/server/release/kolab-server-%{version}/sources/%{name}d-%{_kolabd_ver}-%{_build_date}.src.rpm
NoSource:	0
# NoSource0-md5: ff290c9e410a4ec8740d1d626c17862d
# will be needed? maybe everything can start using their own scritps
#Source1:	%{name}.init
URL:		http://www.kolab.org/
BuildRequires:	%{_bindir}/rpm2cpio
Requires:	webserver = apache
Requires:	apache(mod_dav)
Requires:	apache(mod_dir)
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
Kolab is a secure, scalable and reliable groupware server. It is
formed by a number of well-known and proven components or the
standards tasks such as E-Mail, Directory Service and Web Service.

Kolab adds intelligent interaction between the components, a web
administration interface, management of free-busy lists etc.

Various clients can access Kolab, among them Kontact (KDE), Outlook
(Windows) and Horde (Web).

Major Features:
- Full seamless support of mixed clients environments
  (Outlook/KDE/Web)
- A web administration interface
- Supported languages: Deutsch, English, Francais, Neerlandais
- A shared address book with provision for mailbox users as well as
  contacts
- POP3 as well as IMAP4(rev1) access to mail
- Client-side full support of S/MIME E-Mail encryption possible
  (officially Sphinx-interoperable).

%description -l en
Kolab is a secure, scalable and reliable groupware server. It is
formed by a number of well-known and proven components or the
standards tasks such as E-Mail, Directory Service and Web Service.

Kolab adds intelligent interaction between the components, a web
administration interface, management of free-busy lists etc.

Various clients can access Kolab, among them Kontact (KDE), Outlook
(Windows) and Horde (Web).

Major Features:
- Full seamless support of mixed clients environments
  (Outlook/KDE/Web)
- A web administration interface
- Supported languages: Deutsch, English, Français, Néerlandais
- A shared address book with provision for mailbox users as well as
  contacts
- POP3 as well as IMAP4(rev1) access to mail
- Client-side full support of S/MIME E-Mail encryption possible
  (officially Sphinx-interoperable).

%description -l pl
Kolab to bezpieczny, skalowalny i wiarygodny serwer pracy grupowej.
Sk³ada siê z wielu dobrze znanych, sprawdzonych komponentów lub
standardowych zadañ, takich jak poczta elektroniczna, us³ugi
katalogowe i us³ugi WWW.

Kolab dodaje inteligentn± interakcjê pomiêdzy komponentami, interfejs
administracyjny przez WWW, zarz±dzanie listami wolny-zajêty itp.

Z Kolabem mo¿na wspó³pracowaæ przy u¿yciu ró¿nych klientów, w tym
Kontacta (KDE), Outlooka (Windows) i Horde (WWW).

G³ówne cechy:
- pe³na, przezroczysta obs³uga mieszanych ¶rodowisk klienckich
  (Outlook/KDE/WWW)
- interfejs administracyjny przez WWW
- obs³ugiwane jêzyki: niemiecki, angielski, francuski, holenderski
- wspó³dzielona ksi±¿ka adresowa z zarz±dzaniem u¿ytkownikami skrzynek
  i kontaktami
- dostêp do poczty przez POP3 oraz IMAP4(rev1)
- dostêpna pe³na obs³uga szyfrowania S/MIME dla poczty elektronicznej
  po stronie klienta (oficjalnie zgodna ze Sphinksem).

%package -n kolabd
Summary:	Kolab2 Groupware Server Daemon
Summary(pl):	Demon serwera pracy grupowej Kolab2
Group:		Applications/Mail
Version:	%{_kolabd_ver}

%description -n kolabd
Kolab is the KDE Groupware Server that provides full groupware
features to either KDE Kolab clients or Microsoft Outlook(TM) clients
using third party plugins and web clients in the future. In addition
it is a robust and flexible general IMAP mail server with LDAP
addressbooks.

%description -n kolabd -l pl
Kolab to serwer pracy grupowej dla KDE udostêpniaj±cy pe³ne mo¿liwo¶ci
pracy grupowej klientom KDE Kolab i Microsoft Outlook(TM) przy u¿yciu
zewnêtrznnych wtyczek oraz w przysz³o¶ci klientów WWW. Ponadto jest to
mocny i elastyczny serwer poczty IMAP z ksi±¿kami adresowymi LDAP.

%prep
%setup -q -c -T
mkdir -p kolabd
rpm2cpio %{SOURCE0} | cpio -id
tar -C kolabd -zxf kolabd-%{_kolabd_ver}.tar.gz
patch -p1 -d kolabd < kolabquotawarn-issue851.patch

#find . -type d -name CVS | xargs rm -rf

%install
rm -rf $RPM_BUILD_ROOT

cd kolabd
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_initrddir},%{_vardir}/{log,www/{cgi-bin,freebusy,icons,locks}}}
%define l_shtool shtool
%define l_prefix %{_datadir}/kolab
%define l_value(sa) { %{?*} }
#define SOURCE() %{_sourcedir}/%1
%define SOURCE() ../%1

    %{l_shtool} install -d -m 755 \
$RPM_BUILD_ROOT%{l_prefix}%{_sysconfdir} \
        $RPM_BUILD_ROOT%{l_prefix}/etc/amavisd/templates/en_US \
        $RPM_BUILD_ROOT%{l_prefix}/etc/amavisd/templates/de \
$RPM_BUILD_ROOT%{l_prefix}%{_sysconfdir}/templates \
        $RPM_BUILD_ROOT%{l_prefix}/var/kolab/log \
        $RPM_BUILD_ROOT%{l_prefix}/var/kolab/www/cgi-bin \
        $RPM_BUILD_ROOT%{l_prefix}/var/kolab/www/icons \
        $RPM_BUILD_ROOT%{l_prefix}/var/kolab/www/freebusy \
        $RPM_BUILD_ROOT%{l_prefix}/sbin \
        $RPM_BUILD_ROOT%{l_prefix}/bin \
	$RPM_BUILD_ROOT%{l_prefix}/share/kolab/doc

    %{l_shtool} install -d -m 777 \
        $RPM_BUILD_ROOT%{l_prefix}/var/kolab/www/locks
    %{l_shtool} install -d -m 700 \
        $RPM_BUILD_ROOT%{l_prefix}/var/kolab/httpd_sessions

    %{l_shtool} install -c -m 755 %{l_value -s -a} \
        kolab_sslcert.sh kolab_ca.sh kolab kolab_bootstrap workaround.sh \
	kolabquotawarn \
$RPM_BUILD_ROOT%{l_prefix}%{_sysconfdir}/

    %{l_shtool} install -c -m 755 %{l_value -s -a} \
        kolabpasswd \
        $RPM_BUILD_ROOT%{l_prefix}/bin/

    %{l_shtool} install -c -m 755 %{l_value -s -a} \
	kolab_smtpdpolicy \
$RPM_BUILD_ROOT%{l_prefix}%{_sysconfdir}/

    %{l_shtool} install -c -m 644 %{l_value -s -a} \
        quotawarning.txt \
$RPM_BUILD_ROOT%{l_prefix}%{_sysconfdir}/

    %{l_shtool} install -c -m 600 %{l_value -s -a} \
        kolab.conf \
$RPM_BUILD_ROOT%{l_prefix}%{_sysconfdir}/

    %{l_shtool} install -c -m 644 %{l_value -s -a} \
        templates/*.template \
$RPM_BUILD_ROOT%{l_prefix}%{_sysconfdir}/templates/

    %{l_shtool} install -c -m 644 %{l_value -s -a} \
        rootDSE.ldif \
$RPM_BUILD_ROOT%{l_prefix}%{_sysconfdir}/

    %{l_shtool} install -d -m 755 \
        $RPM_BUILD_ROOT%{l_prefix}/etc/openldap/schema \
        $RPM_BUILD_ROOT%{l_prefix}/libexec/kolab

    %{l_shtool} install -c -m 744 %{l_value -s -a} \
        namespace/kolab \
        $RPM_BUILD_ROOT%{l_prefix}/bin/

    %{l_shtool} install -c -m 744 %{l_value -s -a} \
        namespace/libexec/services \
	namespace/libexec/newconfig \
	namespace/libexec/adduser \
	namespace/libexec/deluser \
	namespace/libexec/listusers \
	namespace/libexec/showuser \
	namespace/libexec/newconfig \
	namespace/libexec/showlog \
	namespace/libexec/start \
	namespace/libexec/stop \
        $RPM_BUILD_ROOT%{l_prefix}/libexec/kolab/

    %{l_shtool} install -c -m 744 %{l_value -s -a} \
	-e 's;@kolab_version@;%{kolab_version};g' \
        kolabd kolabconf kolabcheckperm \
        $RPM_BUILD_ROOT%{l_prefix}/sbin/

    %{l_shtool} install -c -m 644 %{l_value -s -a} \
        kolab.globals \
$RPM_BUILD_ROOT%{l_prefix}%{_sysconfdir}/

    %{l_shtool} install -c -m 644 %{l_value -s -a} \
        kolab2.schema rfc2739.schema \
        $RPM_BUILD_ROOT%{l_prefix}/etc/openldap/schema/

    %{l_shtool} install -c -m 644 %{l_value -s -a} \
        amavisd/en_US/* \
        $RPM_BUILD_ROOT%{l_prefix}/etc/amavisd/templates/en_US/

    %{l_shtool} install -c -m 644 %{l_value -s -a} \
        amavisd/de/* \
        $RPM_BUILD_ROOT%{l_prefix}/etc/amavisd/templates/de/

    %{l_shtool} install -c -m 644 %{l_value -s -a} \
        doc/README.* \
        $RPM_BUILD_ROOT%{l_prefix}/share/kolab/doc/

    #   install run-command script
    %{l_shtool} mkdir -f -p -m 755 \
        $RPM_BUILD_ROOT%{l_prefix}/etc/rc.d
    %{l_shtool} install -c -m 755 %{l_value -s -a} \
        -e 's;@kolab_daemon@;/sbin/kolabd;' \
        %{SOURCE rc.kolabd} $RPM_BUILD_ROOT%{l_prefix}/etc/rc.d/

    #   generate file list
#    %{l_rpmtool} files -v -ofiles -r$RPM_BUILD_ROOT %{l_files_std} \
#	%dir '%defattr(-,%{l_nusr},%{l_ngrp})' %{l_prefix}/var/kolab/httpd_sessions \
#        '%config %{l_prefix}/etc/kolab/*.pem' \
#        '%config %{l_prefix}/etc/kolab/*.schema' \
#        '%config %{l_prefix}/etc/kolab/kolab.conf' \
#	'%config %{l_prefix}/etc/kolab/quotawarning.txt' \
#	'%config %{l_prefix}/etc/kolab/templates/*.template'

%define l_movedir() \
	install -d $RPM_BUILD_ROOT%2; \
	mv $RPM_BUILD_ROOT{%{l_prefix}/%1/*,%2}; \
	ln -sf %2 $RPM_BUILD_ROOT/%{l_prefix}/%1

	%{l_movedir etc/kolab %{_sysconfdir}}
	%{l_movedir share/kolab/doc %{_docdir}/%{name}-%{version}}
	%{l_movedir sbin %{_sbindir}}
	%{l_movedir libexec/kolab %{_libdir}/%{name}}
	%{l_movedir etc/openldap/schema %{_datadir}/openldap/schema}
	%{l_movedir etc/amavisd /etc/amavisd}
	%{l_movedir bin %{_bindir}}
	%{l_movedir etc/rc.d /etc/rc.d}

exit 0


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
%attr(744,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kolab_sslcert.sh
%attr(744,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kolab
%attr(744,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/kolab_bootstrap
%attr(744,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/workaround.sh

%dir /etc/amavisd/templates
%dir /etc/amavisd/templates/de
/etc/amavisd/templates/de/charset
/etc/amavisd/templates/de/template-dsn.txt
/etc/amavisd/templates/de/template-spam-admin.txt
/etc/amavisd/templates/de/template-spam-sender.txt
/etc/amavisd/templates/de/template-virus-admin.txt
/etc/amavisd/templates/de/template-virus-recipient.txt
/etc/amavisd/templates/de/template-virus-sender.txt
/etc/amavisd/templates/en_US/charset
/etc/amavisd/templates/en_US/template-dsn.txt
/etc/amavisd/templates/en_US/template-spam-admin.txt
/etc/amavisd/templates/en_US/template-spam-sender.txt
/etc/amavisd/templates/en_US/template-virus-admin.txt
/etc/amavisd/templates/en_US/template-virus-recipient.txt
/etc/amavisd/templates/en_US/template-virus-sender.txt
%{_sysconfdir}/kolab.conf
%{_sysconfdir}/kolab.globals
%{_sysconfdir}/kolab_ca.sh
%{_sysconfdir}/kolab_smtpdpolicy
%{_sysconfdir}/kolabquotawarn
%{_sysconfdir}/quotawarning.txt
%{_sysconfdir}/rootDSE.ldif
%dir %{_sysconfdir}/templates
%{_sysconfdir}/templates/DB_CONFIG.slapd.template
%{_sysconfdir}/templates/amavisd.conf.template
%{_sysconfdir}/templates/clamd.conf.template
%{_sysconfdir}/templates/cyrus.conf.template
%{_sysconfdir}/templates/fbview.conf.template
%{_sysconfdir}/templates/freebusy.conf.template
%{_sysconfdir}/templates/freshclam.conf.template
%{_sysconfdir}/templates/httpd.conf.template
%{_sysconfdir}/templates/httpd.local.template
%{_sysconfdir}/templates/imapd.conf.template
%{_sysconfdir}/templates/imapd.group.template
%{_sysconfdir}/templates/kolab.conf.template
%{_sysconfdir}/templates/ldap.conf.template
%{_sysconfdir}/templates/main.cf.template
%{_sysconfdir}/templates/master.cf.template
%{_sysconfdir}/templates/php.ini.template
%{_sysconfdir}/templates/proftpd.conf.template
%{_sysconfdir}/templates/rc.conf.template
%{_sysconfdir}/templates/resmgr.conf.template
%{_sysconfdir}/templates/saslauthd.conf.template
%{_sysconfdir}/templates/session_vars.php.template
%{_sysconfdir}/templates/slapd.conf.template
%{_sysconfdir}/templates/slapd.replicas.template
%{_sysconfdir}/templates/smtpd.conf.template
%{_sysconfdir}/templates/transport.template
%{_sysconfdir}/templates/virtual.template
/etc/rc.d/rc.kolabd
%attr(755,root,root) %{_bindir}/kolab
%attr(755,root,root) %{_bindir}/kolabpasswd
%{_libdir}/kolab/adduser
%{_libdir}/kolab/deluser
%{_libdir}/kolab/listusers
%{_libdir}/kolab/newconfig
%{_libdir}/kolab/services
%{_libdir}/kolab/showlog
%{_libdir}/kolab/showuser
%{_libdir}/kolab/start
%{_libdir}/kolab/stop
%attr(755,root,root) %{_sbindir}/kolabcheckperm
%attr(755,root,root) %{_sbindir}/kolabconf
%attr(755,root,root) %{_sbindir}/kolabd
%{_datadir}/doc/kolab-1.9.4/README.amavisd
%{_datadir}/doc/kolab-1.9.4/README.ldapdelete
%{_datadir}/doc/kolab-1.9.4/README.outlook
%{_datadir}/doc/kolab-1.9.4/README.sieve
%{_datadir}/doc/kolab-1.9.4/README.webgui
%{_datadir}/openldap/schema/kolab2.schema
%{_datadir}/openldap/schema/rfc2739.schema

%dir %{_vardir}
%dir %{_vardir}/log
%dir %{_vardir}/www
#%{_vardir}/www/admin
%dir %{_vardir}/www/cgi-bin
%attr(775,http,http) %dir %{_vardir}/www/freebusy
%dir %{_vardir}/www/icons
%attr(775,http,http) %dir %{_vardir}/www/locks
