Name:           libzen
Version:        0.4.28
Release:        3%{?dist}
Summary:        Shared library for libmediainfo and medianfo*
Summary(ru):    Разделяемая библиотека для libmediainfo and medianfo*

License:        zlib/libpng License
URL:            http://sourceforge.net/projects/zenlib
Group:          System Environment/Libraries
Source0:        http://downloads.sourceforge.net/zenlib/%{name}_%{version}.tar.bz2

BuildRequires:  dos2unix
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  automake
BuildRequires:  autoconf

%description
Files shared library for libmediainfo and medianfo-*.

%description -l ru
Файлы разделяемой библиотеки для libmediainfo and medianfo-*.

%package        devel
Summary:        Include files and mandatory libraries for development
Summary(ru):    Пакет с файлами для разработки %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Include files and mandatory libraries for development.

%description    devel -l ru
Файлы для разработки %{name}.

%prep
%setup -q -n ZenLib
dos2unix     *.txt Source/Doc/*.html
%__chmod 644 *.txt Source/Doc/*.html


%build
export CFLAGS="%{optflags}"
export CPPFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

pushd Source/Doc/
    doxygen Doxyfile
popd
cp Source/Doc/*.html ./

pushd Project/GNU/Library
    ./autogen
    %configure --disable-static --enable-shared

    %__make clean
    %__make %{?jobs:-j%{jobs}}
popd

%install
pushd Project/GNU/Library
    %__make install-strip DESTDIR=%{buildroot}
popd

# Zenlib headers and ZenLib-config
%__install -dm 755 %{buildroot}%{_includedir}/ZenLib
%__install -m 644 Source/ZenLib/*.h \
    %{buildroot}%{_includedir}/ZenLib
for i in HTTP_Client Format/Html Format/Http; do
    %__install -dm 755 %{buildroot}%{_includedir}/ZenLib/$i
    %__install -m 644 Source/ZenLib/$i/*.h \
        %{buildroot}%{_includedir}/ZenLib/$i
done

%__sed -i -e 's|Version: |Version: %{version}|g' \
    Project/GNU/Library/%{name}.pc
%__install -dm 755 %{buildroot}%{_libdir}/pkgconfig
%__install -m 644 Project/GNU/Library/%{name}.pc \
    %{buildroot}%{_libdir}/pkgconfig

find %{buildroot} -name '*.a' -exec rm -f {} ';'
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc History.txt License.txt ReadMe.txt
%{_libdir}/%{name}.so.*

%files    devel
%doc Documentation.html
%doc Doc/*
%{_bindir}/%{name}-config
%dir %{_includedir}/ZenLib
%{_includedir}/ZenLib/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Apr 08 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.28-3.R
- Spec prepared for review

* Mon Apr 08 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.28-2.R
- Clean spec

* Mon Sep 03 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.28-1.R
- Update to 0.4.28
- Drop patch

* Fri May 18 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.26-3.R
- Added libzen-config

* Thu May 17 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.26-2.R
- Corrected license
- removed *.a and *.la files

* Wed Apr 11 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.26-1.R
- Update to 0.4.26

* Tue Mar 20 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.25-1.R
- Update to 0.4.25

* Thu Feb 09 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.24-1.R
- Update to 0.4.24

* Tue Nov 22 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.23-2.R
- Added description in russian language

* Tue Nov 14 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.23-1.R
- Update to 0.4.23

* Tue Sep 27 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.22-1.R
- Update to 0.4.22

* Tue Aug 09 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.20-2.R
- Removed 0 from name

* Thu Aug 05 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.20-1.R
- Initial release
