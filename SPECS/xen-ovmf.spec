
# edk2-stable201905
%define GITDATE        201905
%define GITCOMMIT      20d2e5a12
%define _libexecdir %{_libdir}

Name:           xen-ovmf
Version:        %{GITDATE}
Release:        1.git%{GITCOMMIT}%{?dist}
Summary:        UEFI firmware for 64-bit virtual machines

License:        BSD
URL:            http://www.tianocore.org
Source0:        edk2-20d2e5a125e34fc8501026613a71549b2a1a3e54.tar.gz
Source1:        openssl-c3656cc594daac8167721dde7220f0e59ae146fc.tar.gz

BuildRequires:  nasm >= 2.10
BuildRequires:  gcc
BuildRequires:  libuuid-devel
BuildRequires:  /usr/bin/iasl

ExclusiveArch: x86_64

%description
OVMF (Open Virtual Machine Firmware) is a project to enable UEFI support for
Virtual Machines. This package contains a 64-bit UEFI firmware for Xen.


%prep
%setup -q -n edk2
%{__tar} -C ${RPM_BUILD_DIR} -zxf %{SOURCE1}


%build
# make %{?_smp_mflags}, how to use that with ovmf?
smp_flags="%{?_smp_mflags}"
if [[ "$smp_flags" = -j* ]]; then
  smp_flags="-n ${smp_flags#-j}"
elif [ -n "%{?jobs}" ]; then
  smp_flags="-n %{?jobs}"
else
  smp_flags=''
fi
OvmfPkg/build.sh -a X64 -b RELEASE $smp_flags


%install
rm -rf $RPM_BUILD_ROOT

copy_license() {
    install -D -m 644 $1 $RPM_BUILD_ROOT%{_docdir}/%{name}/Licenses/$2-License.txt
}
install -D -m 644 License.txt $RPM_BUILD_ROOT%{_docdir}/%{name}/Licenses/License.txt
copy_license OvmfPkg/License.txt OvmfPkg

install -D -m 644 Build/OvmfX64/RELEASE_GCC*/FV/OVMF.fd %{buildroot}/%{_libexecdir}/xen/boot/OVMF.fd


%files
%doc %{_docdir}/%{name}/Licenses/License.txt
%doc %{_docdir}/%{name}/Licenses/OvmfPkg-License.txt

%{_libexecdir}/xen/boot/OVMF.fd


%changelog
* Tue May 26 2020 Anthony PERARD <anthony.perard@citrix.com> - 201905-1.git20d2e5a12
- Bump with OVMF from Xen 4.13

* Thu Jan 24 2019 Anthony PERARD <anthony.perard@citrix.com> - 20180825-1.gitef529e6ab
- Bump with OVMF from Xen 4.12

* Thu Jan 25 2018 Anthony PERARD <anthony.perard@citrix.com> - 20170920-1.git947f3737a
- Bump with OVMF from Xen 4.10

* Wed Nov 29 2017 Anthony PERARD <anthony.perard@citrix.com> - 20160905-1.gitbc54e50e0
- New package, based on ovmf pkg and xen pkg

