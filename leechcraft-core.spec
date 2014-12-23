%define product_name leechcraft
%define plugin_dir %{_libdir}/%{product_name}/plugins
%define translations_dir %{_datadir}/%{product_name}/translations
%define settings_dir %{_datadir}/%{product_name}/settings
%define full_version %{version}-%{release}

Name:           leechcraft-core
Summary:        A Cross-Platform Modular Internet-Client 
Version:        0.6.60
Release:        1%{?dist}
License:        GPLv2+
Url:            http://leechcraft.org
Source0:        http://downloads.sourceforge.net/project/leechcraft/LeechCraft/0.6.60/leechcraft-0.6.60.tar.xz
Source1:        %{product_name}.desktop
Patch0:         001-fix-plotitem-compilation-error.patch

BuildRequires:  cmake
BuildRequires:  boost-devel 
BuildRequires:  qt4-devel
BuildRequires:  qt-webkit-devel
BuildRequires:  bzip2-devel
BuildRequires:  desktop-file-utils
BuildRequires:  hicolor-icon-theme
BuildRequires:  oxygen-icon-theme

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
%setup -qn %{product_name}-%{version}
%patch0 -p 1


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
pwd
ls ../
%{cmake} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DLEECHCRAFT_VERSION="%{version}" \
    $(cat ../CMakeLists.txt | egrep "^option \(ENABLE" | awk '{print $2}' | sed 's/(//g;s/.*/-D\0=False/g' | xargs)
    ../src

popd
make %{?_smp_mflags} -C %{_target_platform} 

%install
rm -rf $RPM_BUILD_ROOT
make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}

desktop-file-install                                    \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications         \
  %{SOURCE1}

%find_lang leechcraft --with-qt --without-mo

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -n leechcraft -f leechcraft.lang
%doc README LICENSE INSTALL
%{_bindir}/%{product_name}
%{_bindir}/%{product_name}-add-file
%{settings_dir}/coresettings.xml
%dir %{settings_dir}
%dir %{translations_dir}
%dir %{plugin_dir}
%dir %{_datadir}/icons/hicolor/14x14
%dir %{_datadir}/icons/hicolor/14x14/apps
%dir %{_datadir}/%{product_name}
%dir %{_datadir}/%{product_name}/installed
%dir %{_datadir}/%{product_name}/scripts
%dir %{_datadir}/%{product_name}/qml
%dir %{_libdir}/%{product_name}
%{_datadir}/%{product_name}/global_icons
%{_datadir}/%{product_name}/sounds
%{_datadir}/applications/%{product_name}.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_libdir}/libleechcraft-util.so.0.5.0
%{_libdir}/libleechcraft-xsd.so.0.3.0
%doc %{_mandir}/man1/%{product_name}.1.gz

%files -n leechcraft-devel
%{_datadir}/%{product_name}/cmake
%{_datadir}/cmake/Modules/InitLCPlugin.cmake
%{_includedir}/%{product_name}
%{_libdir}/libleechcraft-util.so
%{_libdir}/libleechcraft-xsd.so

%changelog
* Mon Dec 22 2014 Minh Ngo <minh@fedoraproject.org> - 0.6.60-1
- 0.6.60
