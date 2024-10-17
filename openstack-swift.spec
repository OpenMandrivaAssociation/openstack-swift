%global with_doc 1

%define bzr_rev 239
Name:             openstack-swift
Version:          1.2.99.%{bzr_rev}
Release:          3
Summary:          OpenStack Object Storage (swift)
Group:            Development/Python
License:          ASL 2.0
URL:              https://launchpad.net/swift
Source0:          http://hudson.openstack.org/job/swift-tarball/lastSuccessfulBuild/artifact/dist/swift-1.3-dev+bzr%{bzr_rev}.tar.gz
#Source0:          http://launchpad.net/swift/1.2/1.2.0/+download/swift-1.2.0.tar.gz
Source1:          %{name}-functions
Source2:          %{name}-account.init
Source3:          %{name}-auth.init
Source4:          %{name}-container.init
Source5:          %{name}-object.init
Source6:          %{name}-proxy.init
Source20:         %{name}-create-man-stubs.py
BuildRoot:        %{_tmppath}/swift-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    fdupes
BuildRequires:    dos2unix
BuildRequires:    python-devel
BuildRequires:    python-setuptools
Requires:         python-configobj
Requires:         python-eventlet >= 0.9.8
Requires:         python-greenlet >= 0.3.1
Requires:         python-simplejson
Requires:         python-webob
Requires:         pyxattr
Requires:         python-netifaces
Requires(pre):    shadow-utils

%description
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.
Objects are written to multiple hardware devices in the data center, with the
OpenStack software responsible for ensuring data replication and integrity
across the cluster. Storage clusters can scale horizontally by adding new
nodes, which are automatically configured. Should a node fail, OpenStack works
to replicate its content from other active nodes. Because OpenStack uses
software logic to ensure data replication and distribution across different
devices, inexpensive commodity hard drives and servers can be used in lieu of
more expensive equipment.

%package          account
Summary:          A swift account server
Group:            System/Cluster
Requires:         %{name} = %{version}-%{release}

%description      account
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} account server.

%package          auth
Summary:          A swift auth server
Group:            System/Cluster 
Requires:         %{name} = %{version}-%{release}

%description      auth
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} auth server.

%package          container
Summary:          A swift container server
Group:            System/Cluster
Requires:         %{name} = %{version}-%{release}

%description      container
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} container server.

%package          object
Summary:          A swift object server
Group:            System/Cluster 
Requires:         %{name} = %{version}-%{release}

%description      object
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} object server.

%package          proxy
Summary:          A swift proxy server
Group:            System/Cluster
Requires:         %{name} = %{version}-%{release}
Requires:         memcached

%description      proxy
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains the %{name} proxy server.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for %{name}
Group:            Books/Computer books
BuildRequires:    python-sphinx
# Required for generating docs
BuildRequires:    python-eventlet
BuildRequires:    python-simplejson
BuildRequires:    python-webob
BuildRequires:    pyxattr
BuildRequires:    python-xmldiff
BuildRequires:    python-netaddr
BuildRequires:    python-netifaces


%description      doc
OpenStack Object Storage (swift) aggregates commodity servers to work together
in clusters for reliable, redundant, and large-scale storage of static objects.

This package contains documentation files for %{name}.
%endif

%prep
%setup -q -n swift-1.3-dev
# Fix wrong-file-end-of-line-encoding warning
dos2unix LICENSE

%build
CFLAGS="%{optflags}" python setup.py build
# Build docs
%if 0%{?with_doc}
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html source build/html
popd
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif
# Build man stubs
%{__python} %{SOURCE20} --mandir=./man

%install
%{__python} setup.py install --root $RPM_BUILD_ROOT --install-purelib=%{python_sitelib}
# Init helper functions
install -p -D -m 644 %{SOURCE1} %{buildroot}/usr/share/%{name}/functions
# Init scripts
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}-account
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/%{name}-auth
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_initrddir}/%{name}-container
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/%{name}-object
install -p -D -m 755 %{SOURCE6} %{buildroot}%{_initrddir}/%{name}-proxy
# Install man stubs
for name in $( ls ./man ); do
    mkdir -p "%{buildroot}%{_mandir}/$name"
    cp "./man/$name/"*.gz "%{buildroot}%{_mandir}/$name"
done
# Remove tests
rm -fr %{buildroot}/%{python_sitelib}/test
# Misc other
install -d -m 755 %{buildroot}%{_sysconfdir}/swift
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/account-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/auth-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/container-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/object-server
install -d -m 755 %{buildroot}%{_sysconfdir}/swift/proxy-server
# /var/run is not allowed in 11.3 or later because of tmpfs support
%if 0%{?suse_version} < 1130
# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/account-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/auth-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/container-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/object-server
install -d -m 755 %{buildroot}%{_localstatedir}/run/swift/proxy-server
%endif
fdupes %{buildroot}%{python_sitelib}/swift
%clean
rm -rf %{buildroot}

%pre
getent group swift >/dev/null || groupadd -r swift
getent passwd swift >/dev/null || \
useradd -r -g swift -d %{_sharedstatedir}/swift -s /sbin/nologin \
-c "OpenStack Swift Daemons" swift
exit 0

%post account
%_post_service openstack-swift-account

%preun account
%_preun_service openstack-swift-account

%post auth
%_post_service openstack-swift-auth

%preun auth
%_preun_service openstack-swift-auth

%post container
%_post_service openstack-swift-container

%preun container
%_preun_service openstack-swift-container

%post object
%_post_service openstack-swift-object

%preun object
%_preun_service openstack-swift-object

%post proxy
%_post_service openstack-swift-proxy

%preun proxy
%_preun_service openstack-swift-proxy

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README
%dir /usr/share/%{name}/functions
%if 0%{?suse_version} < 1130
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift
%endif
%dir %{_sysconfdir}/swift
%dir %{python_sitelib}/swift
%dir /usr/share/openstack-swift
%{_bindir}/st
%{_bindir}/swift-account-audit
%{_bindir}/swift-drive-audit
%{_bindir}/swift-get-nodes
%{_bindir}/swift-init
%{_bindir}/swift-ring-builder
%{_bindir}/swift-stats-populate
%{_bindir}/swift-stats-report
# TODO: check if this is the correct subpackage
%{_bindir}/swift-bench
%{_bindir}/swift-log-stats-collector
%{_bindir}/swift-log-uploader
# ENDTODO
%{_mandir}/man8/st.8.*
%{_mandir}/man8/swift-account-audit.8.*
%{_mandir}/man8/swift-drive-audit.8.*
%{_mandir}/man8/swift-get-nodes.8.*
%{_mandir}/man8/swift-init.8.*
%{_mandir}/man8/swift-ring-builder.8.*
%{_mandir}/man8/swift-stats-populate.8.*
%{_mandir}/man8/swift-stats-report.8.*
%{python_sitelib}/swift/*.py*
%{python_sitelib}/swift/common
# TODO: check if this is the correct subpackage
%{python_sitelib}/swift/stats
# ENDTODO
%{python_sitelib}/swift-1.*.egg-info

%files account
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample
%dir %{_initrddir}/%{name}-account
%if 0%{?suse_version} < 1130
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/account-server
%endif
%dir %{_sysconfdir}/swift/account-server
%{_bindir}/swift-account-auditor
%{_bindir}/swift-account-reaper
%{_bindir}/swift-account-replicator
%{_bindir}/swift-account-server
# TODO: check if this is the correct subpackage
%{_bindir}/swift-account-stats-logger
# ENDTODO
%{_mandir}/man8/swift-account-auditor.8.*
%{_mandir}/man8/swift-account-reaper.8.*
%{_mandir}/man8/swift-account-replicator.8.*
%{_mandir}/man8/swift-account-server.8.*
%{python_sitelib}/swift/account

%files auth
%defattr(-,root,root,-)
%doc etc/auth-server.conf-sample
%dir %{_initrddir}/%{name}-auth
%if 0%{?suse_version} < 1130
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/auth-server
%endif
%dir %{_sysconfdir}/swift/auth-server
#%{_bindir}/swift-auth-create-account
%{_bindir}/swift-auth-recreate-accounts
%{_bindir}/swift-auth-server
# TODO: check if this is the correct subpackage
%{_bindir}/swift-auth-add-user
%{_bindir}/swift-auth-to-swauth
%{_bindir}/swift-auth-update-reseller-prefixes
%{_bindir}/swauth-add-account
%{_bindir}/swauth-add-user
%{_bindir}/swauth-cleanup-tokens
%{_bindir}/swauth-delete-account
%{_bindir}/swauth-delete-user
%{_bindir}/swauth-list
%{_bindir}/swauth-prep
%{_bindir}/swauth-set-account-service
# ENDTODO
%{_mandir}/man8/swift-auth-create-account.8.*
%{_mandir}/man8/swift-auth-recreate-accounts.8.*
%{_mandir}/man8/swift-auth-server.8.*
%{python_sitelib}/swift/auth

%files container
%defattr(-,root,root,-)
%doc etc/container-server.conf-sample
%dir %{_initrddir}/%{name}-container
%if 0%{?suse_version} < 1130
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/container-server
%endif
%dir %{_sysconfdir}/swift/container-server
%{_bindir}/swift-container-auditor
%{_bindir}/swift-container-server
%{_bindir}/swift-container-replicator
%{_bindir}/swift-container-updater
%{_mandir}/man8/swift-container-auditor.8.*
%{_mandir}/man8/swift-container-server.8.*
%{_mandir}/man8/swift-container-replicator.8.*
%{_mandir}/man8/swift-container-updater.8.*
%{python_sitelib}/swift/container

%files object
%defattr(-,root,root,-)
%doc etc/account-server.conf-sample etc/rsyncd.conf-sample
%dir %{_initrddir}/%{name}-object
%if 0%{?suse_version} < 1130
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/object-server
%endif
%dir %{_sysconfdir}/swift/object-server
%{_bindir}/swift-object-auditor
%{_bindir}/swift-object-info
%{_bindir}/swift-object-replicator
%{_bindir}/swift-object-server
%{_bindir}/swift-object-updater
%{_mandir}/man8/swift-object-auditor.8.*
%{_mandir}/man8/swift-object-info.8.*
%{_mandir}/man8/swift-object-replicator.8.*
%{_mandir}/man8/swift-object-server.8.*
%{_mandir}/man8/swift-object-updater.8.*
%{python_sitelib}/swift/obj

%files proxy
%defattr(-,root,root,-)
%doc etc/proxy-server.conf-sample
%dir %{_initrddir}/%{name}-proxy
%if 0%{?suse_version} < 1130
%dir %attr(0755, swift, root) %{_localstatedir}/run/swift/proxy-server
%endif
%dir %{_sysconfdir}/swift/proxy-server
%{_bindir}/swift-proxy-server
%{_mandir}/man8/swift-proxy-server.8.*
%{python_sitelib}/swift/proxy

%if 0%{?with_doc}
%files doc
%defattr(-,root,root,-)
%doc LICENSE doc/build/html
%endif



%changelog
* Thu Jun 09 2011 Antoine Ginies <aginies@mandriva.com> 1.2.99.239-1mdv2011.0
+ Revision: 683496
- fix doc group
- fix group in subpackage
- import openstack-swift


* Thu Jun 9 2011 Antoine Ginies <aginies@mandriva.com> 2011.1
- first release for Mandriva based on OpenSUSE SRPM

