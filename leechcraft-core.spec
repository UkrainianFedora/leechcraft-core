%define product_name leechcraft
%define plugin_dir %{_libdir}/%{product_name}/plugins
%define translations_dir %{_datadir}/%{product_name}/translations
%define settings_dir %{_datadir}/%{product_name}/settings
%define full_version %{version}-%{release}
%define git_version 3466-g864bd1a

Name:           leechcraft-core
Summary:        A Cross-Platform Modular Internet-Client
Version:        0.6.70
Release:        1%{?dist}
License:        GPLv2+
Url:            http://leechcraft.org
Source0:        http://dist.leechcraft.org/LeechCraft/0.6.75/leechcraft-%{version}-%{git_version}.tar.xz

Patch0:         001-fix-qwt-cmake-script.patch

BuildRequires:  cmake
BuildRequires:  boost-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  bzip2-devel
BuildRequires:  desktop-file-utils
BuildRequires:  pcre-devel


%description
Core executable of Leechcraft

Leechcraft is a free modular "internet client" application.
Leechcraft allows to browse the web, read RSS/Atom feeds, download
files via bit-torrent, HTTP, FTP and DC, automatically stream,
download or play podcast a other media files and much more.

features can be easily added via plugins that can be integrated with
each other with no effort while staying abstract from the exact
implementation.

This package contains the main leechcraft executable, which connects
all the plugins with each other, routes requests between them, tracks
dependencies and performs several other housekeeping tasks.


%package -n leechcraft
Summary:    A Cross-Platform Modular Internet-Client

%description -n leechcraft
%{description}

%package -n leechcraft-devel
Summary:    Leechcraft Development Files
Requires:   %{product_name}%{?_isa} = %{full_version}

%description -n leechcraft-devel
This package contains header files required to develop new modules for
LeechCraft.

%prep
%setup -qn %{product_name}-%{version}-%{git_version}
%patch0 -p 0


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}

%{cmake} \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DLEECHCRAFT_VERSION="%{version}" \
  -DUSE_QT5=True \
  -DUSE_CPP14=True \
  $(cat ../src/CMakeLists.txt | egrep "^(cmake_dependent_)?option \(ENABLE" | awk '{print $2}' | sed 's/^(/-D/;s/$/=False/;' | xargs) \
  ../src

popd
make %{?_smp_mflags} -C %{_target_platform} 

%install
rm -rf $RPM_BUILD_ROOT
make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}

%find_lang leechcraft --with-qt --without-mo

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -n leechcraft -f leechcraft.lang
%doc README LICENSE INSTALL
%{_bindir}/*
%{settings_dir}/coresettings.xml
%dir %{settings_dir}
%dir %{translations_dir}
%dir %{_datadir}/icons/hicolor/14x14
%dir %{_datadir}/icons/hicolor/14x14/apps
%dir %{_datadir}/%{product_name}
%{_datadir}/%{product_name}/qml/*
%{_datadir}/%{product_name}/qml5/*
%{_datadir}/%{product_name}/themes/*
%{_datadir}/%{product_name}/global_icons
%{_datadir}/applications/%{product_name}-qt5.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_libdir}/libleechcraft-*-qt5.so.*
%doc %{_mandir}/man1/*.1.gz

%files -n leechcraft-devel
%{_datadir}/%{product_name}/cmake
%{_datadir}/cmake/Modules/InitLCPlugin.cmake
%{_includedir}/%{product_name}
%{_libdir}/libleechcraft-*-qt5.so

%changelog
* Fri May 29 2015 Minh Ngo <minh@fedoraproject.org> - 0.6.75-1
- Qt5, 0.6.75

* Sat Dec 27 2014 Minh Ngo <minh@fedoraproject.org> - 0.6.70-2
- Refactoring in the cmake script.
- Removing icon themes from build dependencies

* Wed Dec 24 2014 Minh Ngo <minh@fedoraproject.org> - 0.6.70-1
- 0.6.70

* Mon Dec 22 2014 Minh Ngo <minh@fedoraproject.org> - 0.6.60-1
- 0.6.60
