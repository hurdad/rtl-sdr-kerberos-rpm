Name:           rtl-sdr-kerberos
Version:        %{VERSION}
Release:        %{RELEASE}%{?dist}
Summary:        Osmocom RTL-SDR modified branch for KerberosSDR
License:        GNUv2
Group:          Development/Libraries/C and C++
Url:            https://github.com/rtlsdrblog/rtl-sdr-kerberos
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cmake
BuildRequires:	libusbx-devel

%description
Osmocom RTL-SDR modified branch for KerberosSDR

%package devel
Summary:    Development headers and library for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the development headers and library for %{name}.

%prep
%setup -n %{name}-%{version}

%build
mkdir build
pushd build
%cmake ../
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=%{buildroot}
popd

mkdir -p %{buildroot}/etc/udev/rules.d/
cp rtl-sdr.rules %{buildroot}/etc/udev/rules.d/

mkdir -p %{buildroot}/etc/modprobe.d/
echo 'blacklist dvb_usb_rtl28xxu' | tee %{buildroot}/etc/modprobe.d/blacklist-dvb_usb_rtl28xxu.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
ldconfig

%postun
ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/rtl*
%{_libdir}/librtlsdr.so.*
/etc/udev/rules.d/rtl-sdr.rules
/etc/modprobe.d/blacklist-dvb_usb_rtl28xxu.conf

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/librtlsdr.so
%{_libdir}/librtlsdr.a
%{_libdir}/pkgconfig/*.pc

%changelog
