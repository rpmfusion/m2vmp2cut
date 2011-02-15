Name: m2vmp2cut
Version: 0.79
Release: 6%{?dist}
Summary: MPEG2 frame accurate cutter
Summary(sv): MPEG2 bildprecis redigerare

Group: Applications/Multimedia
License: GPLv2
URL: http://www.guru-group.fi/~too/sw/%{name}/
Source0: http://www.guru-group.fi/~too/sw/%{name}/%{name}-%{version}-dev.tar.gz
Source1: %{name}.1
Patch0: %{name}.optflags.patch
Patch1: %{name}.libexec.patch
Patch2: %{name}.help-in-share.patch
Patch3: %{name}.timestamps.patch
BuildRequires: libtool
BuildRequires: gtk2-devel
BuildRequires: libmpeg2-devel

Requires: ProjectX
Requires: mjpegtools
Requires: python
Requires: xterm
Requires: bash
Requires: libmpeg2 >= 0.5.1
Requires: transcode

# The current way to exclude requirements is like this:
# % filter_from_requires /perl(m2vmp2cut)/d
# % filter_setup

# However, because of bug http://bugzilla.rpmfusion.org/show_bug.cgi?id=1580
# that doesn't work.  Until fixed, I'll revert to the old style of exclusion.
cat << \EOF > %name-req
#!/bin/sh
%__perl_requires $* |\
sed -e '/perl(%name)/d'
EOF

%global __perl_requires %_builddir/%name-%version-dev/%name-req
chmod +x %__perl_requires


%description
m2vmp2cut is frame accurate (currently PAL) mpeg2 video (m2v file)
with accompanied mp2 audio (mp2 file) cutter.

Frame accuracy is achieved by re-encoding video around cutpoints.

Audio is cut from separate mp2 file at positions that keep a/v sync as
good as possible (maximum sync difference is around 10-15
milliseconds).

%description -l sv
m2vmp2cut är ett bildprecist redigeringsprogram för mpeg2 video (för
närvarande PAL, m2v-fil) med tillhörande mp2-audio (mp2-fil).

Bildprecision åstadkoms med omkodning av video runt snittpunkter.

Audio klipps från en separat mp2-fil på positions som håller
a/v-synkroniseringen så bra som möjligt (maximal synkroniseringskillnad
är runt 10-15 millisekunder).

%prep
%setup -q -n %{name}-%{version}-dev
# Insert optimizer flags where needed
%patch0
# Put helper programs in libexec
%patch1
# Put help files in /usr/share
%patch2
# Preserve timestamps when installing
%patch3

%build
unset CCACHE_UMASK
make %{?_smp_mflags} CFLAGS='%{optflags} $(LF_OPTS)'

%install
# Put a dummy projectx in the path.  At run time, the real projectx
# script will be used.  With this trick we do not have to have
# ProjectX as a BuildRequires.
mkdir dummybin
touch dummybin/projectx
chmod +x dummybin/projectx
PATH=$(pwd)/dummybin:$PATH make install PREFIX=%{buildroot}%{_prefix}
mkdir -p %{buildroot}%{_mandir}/man1
cp -p %{SOURCE1} %{buildroot}%{_mandir}/man1

%files
%defattr(-,root,root,-)
%doc ANNOUNCE COPYING HISTORY README TODO
%{_bindir}/%{name}
%{_libexecdir}/%{name}-%{version}-dev
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%changelog
* Tue Feb 15 2011 Göran Uddeborg <goeran@uddeborg.se> 0.79-6
- Revert to old style perl requirement exclusion, since bug 1580 seems
  to take a while to get fixed.

* Mon Dec 27 2010 Göran Uddeborg <goeran@uddeborg.se> 0.79-5
- Simplify optimization patch, by not modifying the makefile where it only
  does linking.

* Mon Dec 20 2010 Göran Uddeborg <goeran@uddeborg.se> 0.79-4
- Let rpm's optflags OVERRIDE rather than ADD TO the upstreams flags.
- Unset CCACHE_UMASK to avoid getting group writable binaries.

* Mon Dec 13 2010 Göran Uddeborg <goeran@uddeborg.se> 0.79-3
- Compile with optflags.
- Require transcode, it is strongly recommended even if not strictly required.
- License is GPLv2 only.
- Use a separate patch file to put helper programs in libexec.
- Put help files in /usr/share.
- Remove obsolete unused macro definitions.
- Filter perl requirements according to updated recommendations.
- Add disttag.
- Require the package xterm rather than the uxterm binary.
- Preserve timestamps when installing files.
- Add braces around variables.
- Include a simple manual pages, based on "m2vmp2cut help ."

* Sun Sep 19 2010 Göran Uddeborg <goeran@uddeborg.se> 0.79-2
- Added COPYING and doc/Examples to the documentation.
- Changed to "global" in definition of __perl_requires.
- Create a dummy projectx in the path, to avoid having ProjectX as a
  build requirement.

* Thu Apr  8 2010 Göran Uddeborg <goeran@uddeborg.se> 0.79-1
- Version 0.79.
- SPEC file updated to match Fedora packaging standards.

* Tue Feb 10 2009 Göran Uddeborg <goeran@uddeborg.se> 0.77-1
- Version 0.77 with fix for an A/V sync problem.

* Sat Feb  7 2009 Göran Uddeborg <goeran@uddeborg.se> 0.76-2
- Add missing perl quote in m2vmp2cut.pl

* Sat Feb  7 2009 Göran Uddeborg <goeran@uddeborg.se> 0.76-1
- Bump to new version.

* Tue Sep  9 2008 Göran Uddeborg <goeran@uddeborg.se> 0.72-2
- Patch for sync problem.

* Sun Aug 17 2008 Göran Uddeborg <goeran@uddeborg.se> 0.72-1
- Version bump
- Fix for offset type bug

* Mon Jul 28 2008 Göran Uddeborg <goeran@uddeborg.se> 0.68-1
- First RPM packaging
