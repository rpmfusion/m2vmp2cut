Name: m2vmp2cut
Version: 0.86
Release: 7%{?dist}
Summary: MPEG2 frame accurate cutter
Summary(sv): MPEG2 bildprecis redigerare

License: GPLv2
URL: http://www.guru-group.fi/~too/sw/%{name}/
Source0: http://www.guru-group.fi/~too/sw/%{name}/%{name}-%{version}.tar.xz
Source1: %{name}.1
BuildRequires: libtool
BuildRequires: gtk2-devel
BuildRequires: libmpeg2-devel
BuildRequires: perl-generators

Requires: ProjectX
Requires: mjpegtools
Requires: perl-interpreter
Requires: python
Requires: xterm
Requires: bash
Requires: libmpeg2 >= 0.5.1
Requires: transcode

%{?filter_setup:
%filter_from_requires /perl(m2vmp2cut)/d
%filter_setup
}


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
a/v-synkroniseringen så bra som möjligt (maximal synkroniseringsskillnad
är runt 10-15 millisekunder).

%prep
%setup -q


%build
make %{?_smp_mflags} OPTFLAGS='%{optflags}'


%install
# Put dummy versions of a few commands the path.  At run time, the
# real programs will be used, the package requirements ensures that.
# At build time only their existence is tested.  With this trick we do
# not have to add a lot of essentially unused stuff as a
# BuildRequires.
mkdir dummybin
for command in projectx java mplex
do  touch dummybin/$command
    chmod +x dummybin/$command
done
PATH=$(pwd)/dummybin:$PATH make install PREFIX=%{_prefix} \
	LIBEXECDIR=%{_libexecdir}/%{name} DATAROOTDIR=%{_datadir} \
	DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_mandir}/man1
cp -p %{SOURCE1} %{buildroot}%{_mandir}/man1

%files
%if 0%{?_licensedir:1}
%license COPYING
%else
%doc COPYING
%endif
%doc ANNOUNCE NEWS README
%{_bindir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/doc/%{name}-%{version}
%{_mandir}/man1/%{name}.1.gz

%changelog
* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.86-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 15 2017 Paul Howarth <paul@city-fan.org> - 0.86-6
- Perl 5.26 rebuild
- Add perl-interpreter dependency
  (https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules)

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.86-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 25 2016 Paul Howarth <paul@city-fan.org> - 0.86-4
- BR: perl-generators for proper dependency generation
  (https://fedoraproject.org/wiki/Changes/Build_Root_Without_Perl)
- Use %%license where possible
- Drop %%defattr, redundant since rpm 4.4

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.86-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Oct 19 2012 Göran Uddeborg <goeran@uddeborg.se> 0.86-2
- The time stamp on the 0.86-1 changelog got wrong.  Corrected now.

* Thu Oct 18 2012 Göran Uddeborg <goeran@uddeborg.se> 0.86-1
- Upgrade to version 0.86.
- All patches have been included upstreams, in one way or another, and
  are removed from the RPM
- Remove "dev" directory suffix since this is an official release.
- More dummy programs needed during build.
- The manual page updated to match the current documentation.

* Tue Mar 20 2012 Göran Uddeborg <goeran@uddeborg.se> 0.79-10
- There should still be a guard around the perl filtering.

* Sun Mar 18 2012 Göran Uddeborg <goeran@uddeborg.se> 0.79-9
- Bug 1580 is fixed; move to new style perl requirement filtering.

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.79-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 13 2011 Göran Uddeborg <goeran@uddeborg.se> 0.79-7
- Apply a fix for a bug when giving a path to a file to demux.

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
