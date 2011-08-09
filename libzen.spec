Name:           libzen
Version:        0.4.20
Release:        1%{?dist}.R
Summary:        Shared library for libmediainfo and medianfo*

License:        BSD
URL:            http://zenlib.sourceforge.net/
Group:          System/Libraries
Source0:        http://downloads.sourceforge.net/zenlib/%{name}_%{version}.tar.bz2
Patch0:         libzen-compile.patch
BuildRequires:  dos2unix
BuildRequires:  doxygen
BuildRequires:  gcc-c++   

%description
Shared library for libmediainfo and medianfo-*.

%package        devel
Summary:        Include files and mandatory libraries for development
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}

%description    devel
Include files and mandatory libraries for development.


%prep
%setup -q -n ZenLib
%patch0 -p1
dos2unix     *.txt Source/Doc/*.html
%__chmod 644 *.txt Source/Doc/*.html

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CPPFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"

pushd Source/Doc/
    doxygen Doxyfile
popd
cp Source/Doc/*.html ./

pushd Project/GNU/Library
    %__chmod +x autogen
    ./autogen
    %configure --enable-shared

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
for i in Base64 HTTP_Client Format/Html Format/Http TinyXml; do
    %__install -dm 755 %{buildroot}%{_includedir}/ZenLib/$i
    %__install -m 644 Source/ZenLib/$i/*.h \
        %{buildroot}%{_includedir}/ZenLib/$i
done

%__sed -i -e 's|Version: |Version: %{version}|g' \
    Project/GNU/Library/libzen.pc
%__install -dm 755 %{buildroot}%{_libdir}/pkgconfig
%__install -m 644 Project/GNU/Library/libzen.pc \
    %{buildroot}%{_libdir}/pkgconfig

%clean
[ -d "%{buildroot}" -a "%{buildroot}" != "" ] && %__rm -rf "%{buildroot}"

%post -n libzen -p /sbin/ldconfig

%postun -n libzen -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc History.txt License.txt ReadMe.txt
%{_libdir}/libzen.so.*

%files    devel
%defattr(-,root,root,-)
%doc Documentation.html
%doc Doc/*
%dir %{_includedir}/ZenLib
%{_includedir}/ZenLib/*
%{_libdir}/libzen.a
%{_libdir}/libzen.la
%{_libdir}/libzen.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Aug 09 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.20-2.R
- Removed 0 from name

* Thu Aug 05 2011 Vasiliy N. Glazov <vascom2@gmail.com> 0.4.20-1.R
- Initial release