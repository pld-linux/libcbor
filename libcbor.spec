#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	CBOR protocol implementation
Summary(pl.UTF-8):	Implementacja protokołu CBOR
Name:		libcbor
Version:	0.9.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/PJK/libcbor/releases
Source0:	https://github.com/PJK/libcbor/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	265643416bedb4fa33a1937501dae36a
URL:		http://libcbor.org/
BuildRequires:	cmake >= 3.2
%if %{with apidocs}
BuildRequires:	python3-breathe
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libcbor is a C library for parsing and generating CBOR (RFC 7049), the
general-purpose schema-less binary data format.

%description -l pl.UTF-8
libcbor to biblioteka C do analizy i generowania formatu danych CBOR
(RFC 7049) - pozbawionego schematu binarnego formatu danych ogólnego
przeznaczenia.

%package devel
Summary:	Header files for libcbor library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libcbor
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libcbor library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libcbor.

%package apidocs
Summary:	API documentation for libcbor library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libcbor
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libcbor library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libcbor.

%prep
%setup -q

%build
install -d build
cd build
# expects CMAKE_INSTALL_LIBDIR relative to prefix
%cmake .. \
	-DCMAKE_INSTALL_LIBDIR=%{_lib}

%{__make}
cd ..

%if %{with apidocs}
%{__make} -C doc html \
	SPHINXBULD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE.md README.md
%attr(755,root,root) %{_libdir}/libcbor.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcbor.so.0.9

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcbor.so
%{_includedir}/cbor
%{_includedir}/cbor.h
%{_pkgconfigdir}/libcbor.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_static,api,*.html,*.js}
%endif
