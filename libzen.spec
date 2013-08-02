Name:           libzen
Version:        0.4.29
Release:        2%{?dist}
Summary:        Shared library for libmediainfo and medianfo*
Summary(ru):    Разделяемая библиотека для libmediainfo и medianfo*

License:        zlib
URL:            http://sourceforge.net/projects/zenlib
Group:          System Environment/Libraries
Source0:        http://downloads.sourceforge.net/zenlib/%{name}_%{version}.tar.bz2

BuildRequires:  doxygen
BuildRequires:  libtool
BuildRequires:  automake
BuildRequires:  autoconf

%description
Files shared library for libmediainfo and medianfo-*.

%description -l ru
Файлы разделяемой библиотеки для libmediainfo и medianfo-*.

%package        doc
Summary:        Documentation for %{name}
Summary(ru):    Пакет с документацией для %{name}
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    doc
Documentation files.

%description    doc -l ru
Файлы документации %{name}.

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
#Correct documentation encoding and permissions
sed -i 's/.$//' *.txt
chmod 644 *.txt Source/Doc/Documentation.html

chmod 644 Source/ZenLib/*.h Source/ZenLib/*.cpp \
    Source/ZenLib/Format/Html/*.h Source/ZenLib/Format/Html/*.cpp \
    Source/ZenLib/Format/Http/*.h Source/ZenLib/Format/Http/*.cpp

pushd Project/GNU/Library
    autoreconf -i
popd

%build
#Make documentation
pushd Source/Doc/
    doxygen -u Doxyfile
    doxygen Doxyfile
popd
cp Source/Doc/*.html ./

pushd Project/GNU/Library
    %configure --disable-static --enable-shared

    make clean
    make %{?_smp_mflags}
popd

%install
pushd Project/GNU/Library
    %make_install
popd

#Install headers and ZenLib-config
install -p -dm 755 %{buildroot}%{_includedir}/ZenLib
install -p -m 644 Source/ZenLib/*.h \
    %{buildroot}%{_includedir}/ZenLib
for i in HTTP_Client Format/Html Format/Http; do
    install -p -dm 755 %{buildroot}%{_includedir}/ZenLib/$i
    install -p -m 644 Source/ZenLib/$i/*.h \
        %{buildroot}%{_includedir}/ZenLib/$i
done

sed -i -e 's|Version: |Version: %{version}|g' \
    Project/GNU/Library/%{name}.pc
install -p -dm 755 %{buildroot}%{_libdir}/pkgconfig
install -p -m 644 Project/GNU/Library/%{name}.pc \
    %{buildroot}%{_libdir}/pkgconfig

rm %{buildroot}%{_libdir}/%{name}.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc History.txt License.txt ReadMe.txt
%{_libdir}/%{name}.so.*

%files doc
%doc Documentation.html
%doc Doc

%files devel
%{_bindir}/%{name}-config
%{_includedir}/ZenLib
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Aug 02 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.29-2
- Corrected build flags
- Use more macros

* Fri May 31 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.29-1
- update to 0.4.29

* Tue Apr 23 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.28-7
- Corrected shebang
- Removed dos2unix from BR
- Correcting encoding for all files
- Corrected config and build

* Mon Apr 15 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.28-6
- Added doc subpackage
- Removed gcc-c++ from BR

* Mon Apr 08 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.28-5
- Corrected license
- Added comments
- Corrected make on smp

* Mon Apr 08 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.28-4
- Spec prepared for review again

* Mon Apr 08 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.28-3
- Spec prepared for review

* Mon Apr 08 2013 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.28-2
- Clean spec

* Mon Sep 03 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.28-1
- Update to 0.4.28
- Drop patch

* Fri May 18 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.26-3
- Added libzen-config

* Thu May 17 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.26-2
- Corrected license
- removed *.a and *.la files

* Wed Apr 11 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.26-1
- Update to 0.4.26

* Tue Mar 20 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.25-1
- Update to 0.4.25

* Thu Feb 09 2012 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.24-1
- Update to 0.4.24

* Tue Nov 22 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.23-2
- Added description in russian language

* Mon Nov 14 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.23-1
- Update to 0.4.23

* Tue Sep 27 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.22-1
- Update to 0.4.22

* Tue Aug 09 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.20-2
- Removed 0 from name

* Fri Aug 05 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.20-1
- Initial release
