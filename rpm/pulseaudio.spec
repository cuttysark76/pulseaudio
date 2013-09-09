# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.27
# 

Name:       pulseaudio

# >> macros
# << macros

Summary:    General purpose sound server
Version:    4.0
Release:    1
Group:      Multimedia/PulseAudio
License:    LGPLv2+
URL:        http://pulseaudio.org
Source0:    http://freedesktop.org/software/pulseaudio/releases/pulseaudio-%{version}.tar.xz
Source1:    90-pulse.conf
Source2:    pulseaudio.service
Source100:  pulseaudio.yaml
Patch0:     0001-build-Install-pulsecore-headers.patch
Patch1:     0002-Use-etc-boardname-to-load-a-hardware-specific-config.patch
Patch2:     0003-daemon-Disable-automatic-shutdown-by-default.patch
Patch3:     0004-daemon-Set-the-default-resampler-to-ffmpeg.patch
Requires:   udev
Requires:   libsbc >= 1.0
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(alsa) >= 1.0.24
BuildRequires:  pkgconfig(bluez) >= 4.99
BuildRequires:  pkgconfig(dbus-1) >= 1.4.12
BuildRequires:  pkgconfig(glib-2.0) >= 2.4.0
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(json) >= 0.9
BuildRequires:  pkgconfig(libasyncns) >= 0.1
BuildRequires:  pkgconfig(libsystemd-daemon)
BuildRequires:  pkgconfig(libsystemd-login)
BuildRequires:  pkgconfig(libudev) >= 143
BuildRequires:  pkgconfig(orc-0.4) >= 0.4.11
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(sndfile) >= 1.0.20
BuildRequires:  pkgconfig(speexdsp) >= 1.2
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb) >= 1.6
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(atomic_ops)
BuildRequires:  pkgconfig(sbc) >= 1.0
BuildRequires:  intltool
BuildRequires:  libcap-devel
BuildRequires:  libtool >= 2.4
BuildRequires:  libtool-ltdl-devel
BuildRequires:  fdupes

%description
PulseAudio is a layer between audio devices and applications. It removes
the need for applications to care about the details of the hardware.
PulseAudio is responsible for:
 * automatically converting the audio format between applications and sound
   devices
 * mixing audio streams, which allows multiple applications to use the same
   sound device at the same time
 * handling device and application volumes
 * routing audio to the right place without requiring applications to care
   about the routing
 * providing an unified view of all audio devices, regardless of whether
   they are ALSA-supported sound cards, Bluetooth headsets, remote sound
   cards in the local network or anything else
 * and more...


%package module-x11
Summary:    PulseAudio components needed for starting x11 User session
Group:      Multimedia/PulseAudio
Requires:   %{name} = %{version}-%{release}
Requires:   /bin/sed

%description module-x11
Description: %{summary}

%package devel
Summary:    PulseAudio Development headers and libraries
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Description: %{summary}

%package esound
Summary:    ESound compatibility
Group:      Multimedia/PulseAudio
Requires:   %{name} = %{version}-%{release}

%description esound
Makes PulseAudio a drop-in replacement for ESound.

%package kde
Summary:    KDE specific configuration for PulseAudio
Group:      Multimedia/PulseAudio
Requires:   %{name} = %{version}-%{release}

%description kde
Loads module-device-manager automatically at user session
initialization time. module-device-manager makes it possible for Phonon
to manage the devices in PulseAudio.


%prep
%setup -q -n %{name}-%{version}/pulseaudio

# 0001-build-Install-pulsecore-headers.patch
%patch0 -p1
# 0002-Use-etc-boardname-to-load-a-hardware-specific-config.patch
%patch1 -p1
# 0003-daemon-Disable-automatic-shutdown-by-default.patch
%patch2 -p1
# 0004-daemon-Set-the-default-resampler-to-ffmpeg.patch
%patch3 -p1
# >> setup
# << setup

%build
# >> build pre
echo "%{version}" > .tarball-version
NOCONFIGURE=1 ./bootstrap.sh
# << build pre

%configure --disable-static \
    --disable-neon-opt

make %{?jobs:-j%jobs}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
install -d %{buildroot}/etc/security/limits.d
cp -a %{SOURCE1} %{buildroot}/etc/security/limits.d
install -d %{buildroot}/usr/lib/systemd/user
cp -a %{SOURCE2} %{buildroot}/usr/lib/systemd/user
# << install post

%find_lang pulseaudio

%fdupes  %{buildroot}/%{_datadir}
%fdupes  %{buildroot}/%{_includedir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f pulseaudio.lang
%defattr(-,root,root,-)
# >> files
%doc GPL LGPL LICENSE README
%doc %{_mandir}/man1/pacat.1.gz
%doc %{_mandir}/man1/pacmd.1.gz
%doc %{_mandir}/man1/pactl.1.gz
%doc %{_mandir}/man1/padsp.1.gz
%doc %{_mandir}/man1/paplay.1.gz
%doc %{_mandir}/man1/pasuspender.1.gz
%doc %{_mandir}/man1/pulseaudio.1.gz
%doc %{_mandir}/man5/*.5.gz
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/pulseaudio-system.conf
%config(noreplace) %{_sysconfdir}/pulse/*.conf
%config(noreplace) %{_sysconfdir}/pulse/*.pa
%config(noreplace) %{_sysconfdir}/security/limits.d/90-pulse.conf
%{_sysconfdir}/bash_completion.d/pulseaudio-bash-completion.sh
%{_libdir}/systemd/user/pulseaudio.service
/lib/udev/rules.d/90-pulseaudio.rules
%{_bindir}/pacat
%{_bindir}/pacmd
%{_bindir}/pactl
%{_bindir}/padsp
%{_bindir}/pamon
%{_bindir}/paplay
%{_bindir}/parec
%{_bindir}/parecord
%{_bindir}/pasuspender
%{_bindir}/pulseaudio
%{_bindir}/start-pulseaudio
%{_libdir}/*.so.*
%{_libdir}/libpulsecore-%{version}.so
%{_libdir}/pulse-%{version}/modules/libalsa-util.so
%{_libdir}/pulse-%{version}/modules/libbluetooth-util.so
%{_libdir}/pulse-%{version}/modules/libcli.so
%{_libdir}/pulse-%{version}/modules/liboss-util.so
%{_libdir}/pulse-%{version}/modules/libprotocol-cli.so
%{_libdir}/pulse-%{version}/modules/libprotocol-http.so
%{_libdir}/pulse-%{version}/modules/libprotocol-native.so
%{_libdir}/pulse-%{version}/modules/libprotocol-simple.so
%{_libdir}/pulse-%{version}/modules/librtp.so
%{_libdir}/pulse-%{version}/modules/module-alsa-card.so
%{_libdir}/pulse-%{version}/modules/module-alsa-sink.so
%{_libdir}/pulse-%{version}/modules/module-alsa-source.so
%{_libdir}/pulse-%{version}/modules/module-always-sink.so
%{_libdir}/pulse-%{version}/modules/module-augment-properties.so
%{_libdir}/pulse-%{version}/modules/module-bluetooth-device.so
%{_libdir}/pulse-%{version}/modules/module-bluetooth-discover.so
%{_libdir}/pulse-%{version}/modules/module-bluetooth-proximity.so
%{_libdir}/pulse-%{version}/modules/module-bluetooth-policy.so
%{_libdir}/pulse-%{version}/modules/module-card-restore.so
%{_libdir}/pulse-%{version}/modules/module-cli-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-cli-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-cli.so
%{_libdir}/pulse-%{version}/modules/module-combine-sink.so
%{_libdir}/pulse-%{version}/modules/module-combine.so
%{_libdir}/pulse-%{version}/modules/module-console-kit.so
%{_libdir}/pulse-%{version}/modules/module-dbus-protocol.so
%{_libdir}/pulse-%{version}/modules/module-default-device-restore.so
%{_libdir}/pulse-%{version}/modules/module-detect.so
%{_libdir}/pulse-%{version}/modules/module-device-manager.so
%{_libdir}/pulse-%{version}/modules/module-device-restore.so
%{_libdir}/pulse-%{version}/modules/module-echo-cancel.so
%{_libdir}/pulse-%{version}/modules/module-esound-sink.so
%{_libdir}/pulse-%{version}/modules/module-filter-apply.so
%{_libdir}/pulse-%{version}/modules/module-filter-heuristics.so
%{_libdir}/pulse-%{version}/modules/module-hal-detect.so
%{_libdir}/pulse-%{version}/modules/module-http-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-http-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-intended-roles.so
%{_libdir}/pulse-%{version}/modules/module-ladspa-sink.so
%{_libdir}/pulse-%{version}/modules/module-loopback.so
%{_libdir}/pulse-%{version}/modules/module-match.so
%{_libdir}/pulse-%{version}/modules/module-mmkbd-evdev.so
%{_libdir}/pulse-%{version}/modules/module-native-protocol-fd.so
%{_libdir}/pulse-%{version}/modules/module-native-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-native-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-null-sink.so
%{_libdir}/pulse-%{version}/modules/module-null-source.so
%{_libdir}/pulse-%{version}/modules/module-oss.so
%{_libdir}/pulse-%{version}/modules/module-pipe-sink.so
%{_libdir}/pulse-%{version}/modules/module-pipe-source.so
%{_libdir}/pulse-%{version}/modules/module-position-event-sounds.so
%{_libdir}/pulse-%{version}/modules/module-remap-sink.so
%{_libdir}/pulse-%{version}/modules/module-rescue-streams.so
%{_libdir}/pulse-%{version}/modules/module-role-cork.so
%{_libdir}/pulse-%{version}/modules/module-rtp-recv.so
%{_libdir}/pulse-%{version}/modules/module-rtp-send.so
%{_libdir}/pulse-%{version}/modules/module-rygel-media-server.so
%{_libdir}/pulse-%{version}/modules/module-simple-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-simple-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-sine-source.so
%{_libdir}/pulse-%{version}/modules/module-sine.so
%{_libdir}/pulse-%{version}/modules/module-stream-restore.so
%{_libdir}/pulse-%{version}/modules/module-suspend-on-idle.so
%{_libdir}/pulse-%{version}/modules/module-systemd-login.so
%{_libdir}/pulse-%{version}/modules/module-switch-on-port-available.so
%{_libdir}/pulse-%{version}/modules/module-switch-on-connect.so
%{_libdir}/pulse-%{version}/modules/module-tunnel-sink.so
%{_libdir}/pulse-%{version}/modules/module-tunnel-source.so
%{_libdir}/pulse-%{version}/modules/module-udev-detect.so
%{_libdir}/pulse-%{version}/modules/module-virtual-sink.so
%{_libdir}/pulse-%{version}/modules/module-virtual-source.so
%{_libdir}/pulse-%{version}/modules/module-virtual-surround-sink.so
%{_libdir}/pulse-%{version}/modules/module-volume-restore.so
%{_libdir}/pulse-%{version}/modules/module-remap-source.so
%{_libdir}/pulse-%{version}/modules/module-role-ducking.so
%{_libdir}/pulseaudio/*.so
%{_libexecdir}/pulse/proximity-helper
%{_datadir}/pulseaudio/alsa-mixer/paths/*.conf
%{_datadir}/pulseaudio/alsa-mixer/paths/*.common
%{_datadir}/pulseaudio/alsa-mixer/profile-sets/*.conf
# << files

%files module-x11
%defattr(-,root,root,-)
# >> files module-x11
%doc %{_mandir}/man1/pax11publish.1.gz
%doc %{_mandir}/man1/start-pulseaudio-x11.1.gz
%config %{_sysconfdir}/xdg/autostart/pulseaudio.desktop
%{_bindir}/pax11publish
%{_bindir}/start-pulseaudio-x11
%{_libdir}/pulse-%{version}/modules/module-x11-bell.so
%{_libdir}/pulse-%{version}/modules/module-x11-cork-request.so
%{_libdir}/pulse-%{version}/modules/module-x11-publish.so
%{_libdir}/pulse-%{version}/modules/module-x11-xsmp.so
# << files module-x11

%files devel
%defattr(-,root,root,-)
# >> files devel
%{_includedir}/pulse/*.h
%{_includedir}/pulsecore/*.h
%{_libdir}/cmake/PulseAudio/*.cmake
%{_libdir}/libpulse-mainloop-glib.so
%{_libdir}/libpulse-simple.so
%{_libdir}/libpulse.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/vala/vapi/*.deps
%{_datadir}/vala/vapi/*.vapi
# << files devel

%files esound
%defattr(-,root,root,-)
# >> files esound
%doc %{_mandir}/man1/esdcompat.1.gz
%{_bindir}/esdcompat
%{_libdir}/pulse-%{version}/modules/libprotocol-esound.so
%{_libdir}/pulse-%{version}/modules/module-esound-compat-spawnfd.so
%{_libdir}/pulse-%{version}/modules/module-esound-compat-spawnpid.so
%{_libdir}/pulse-%{version}/modules/module-esound-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-esound-protocol-unix.so
# << files esound

%files kde
%defattr(-,root,root,-)
# >> files kde
%doc %{_mandir}/man1/start-pulseaudio-kde.1.gz
%config %{_sysconfdir}/xdg/autostart/pulseaudio-kde.desktop
%{_bindir}/start-pulseaudio-kde
# << files kde
