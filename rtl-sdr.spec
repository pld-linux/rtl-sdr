# TODO:
# - some sane perm/group in udev rules
%define	snap	20140111
Summary:	SDR utilities for Realtek RTL2832 based DVB-T dongles
Name:		rtl-sdr
Version:	0
Release:	0.%{snap}.1
License:	GPL v2+
Group:		Applications/Communications
URL:		http://sdr.osmocom.org/trac/wiki/rtl-sdr
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	137b28d8f48a3db8fa0ae7c1fc2a0522
BuildRequires:	cmake
BuildRequires:	libusb-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package can turn your RTL2832 based DVB-T dongle into a SDR
receiver.

%package devel
Summary:	Development files for rtl-sdr
Group:		Applications/Communications
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for rtl-sdr.

%prep
%setup -q -n %{name}
rm -rf src/getopt

%build
install -d build
cd build
%cmake \
	-DINSTALL_UDEV_RULES=ON \
	..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# remove static libs
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING
%attr(755,root,root) %{_bindir}/rtl_*
%attr(755,root,root) %{_libdir}/librtlsdr.so.*.*
%attr(755,root,root) %ghost %{_libdir}/librtlsdr.so.0
%{_sysconfdir}/udev/rules.d/rtl-sdr.rules

%files devel
%defattr(644,root,root,755)
%{_includedir}/rtl*.h
%attr(755,root,root) %{_libdir}/librtlsdr.so
%{_pkgconfigdir}/librtlsdr.pc
