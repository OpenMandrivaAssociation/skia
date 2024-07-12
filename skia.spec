# Build system can't handle debugsource generation
%undefine _debugsource_packages

%define libpackage %mklibname skia
%define devpackage %mklibname -d skia

Name: skia
Version: 20240711
Release: 1
# Source must be generated with package-source.sh due to insane
# amounts of internalized external libraries
Source0: skia-%{version}.tar.zst
Source1000: package-source.sh
Summary: The Skia 2D graphics library
URL: https://github.com/skia/skia
License: Apache-2.0
Group: System/Libraries
BuildRequires: gn
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libwebp)
BuildRequires: pkgconfig(bzip2)
BuildRequires: pkgconfig(libbrotlidec)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(graphite2)
BuildRequires: pkgconfig(libsharpyuv)
BuildRequires: pkgconfig(libpcre2-8)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(glesv1_cm)
BuildRequires: pkgconfig(glesv2)

%description
The Skia 2D graphics library

%package -n %{libpackage}
Summary: The Skia 2D graphics library

%description -n %{libpackage}
The Skia 2D graphics library

%package -n %{devpackage}
Summary: Development files for the Skia 2D graphics library
Requires: %{libpackage} = %{EVRD}

%description -n %{devpackage}
Development files for the Skia 2D graphics library

%prep
%autosetup -p1 -n skia
ln -s %{_bindir}/gn bin/

%conf
GN_DEFINES="ar=\"%{__ar}\""
GN_DEFINES+=" cc=\"%{__cc}\""
GN_DEFINES+=" cxx=\"%{__cxx}\""
#GN_DEFINES+=" extra_cflags=\"%{build_cflags}\""
#GN_DEFINES+=" extra_ldflags=\"%{build_ldflags}\""
GN_DEFINES+=" is_debug=false"
GN_DEFINES+=" is_official_build=true"
GN_DEFINES+=" is_component_build=true"
GN_DEFINES+=" skia_enable_graphite=true"
GN_DEFINES+=" skia_use_client_icu=true"
GN_DEFINES+=" skia_use_egl=true"
GN_DEFINES+=" skia_use_ffmpeg=true"
GN_DEFINES+=" skia_use_freetype_woff2=true"
GN_DEFINES+=" skia_use_freetype_zlib_bundled=false"
GN_DEFINES+=" skia_use_libjxl_decode=true"
GN_DEFINES+=" skia_use_system_expat=true"
GN_DEFINES+=" skia_use_system_freetype2=true"
GN_DEFINES+=" skia_use_system_harfbuzz=true"
GN_DEFINES+=" skia_use_system_icu=true"
GN_DEFINES+=" skia_use_system_libjpeg_turbo=true"
GN_DEFINES+=" skia_use_system_libpng=true"
GN_DEFINES+=" skia_use_system_libwebp=true"
GN_DEFINES+=" skia_use_system_zlib=true"
GN_DEFINES+=" skia_use_vulkan=true"
gn gen --args="${GN_DEFINES}" out/Release

%build
%ninja_build -C out/Release

%install
mkdir -p %{buildroot}%{_libdir} %{buildroot}%{_includedir}/skia
mv out/Release/*.so* %{buildroot}%{_libdir}/

find include out/Release -type f -and -\( -name "*.h" -or -name "*.hh" -or -name "*.hpp" -or -name "*.hxx" -or -name "*.inc" -\) -exec install -v -D -m644 {} %{buildroot}%{_includedir}/skia/{} \;
# We don't need headers that are specific to other OSes
rm -rf %{buildroot}%{_includedir}/skia/android

%files -n %{libpackage}
%{_libdir}/*

%files -n %{devpackage}
%{_includedir}/skia
