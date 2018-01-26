
%define GITDATE        20170920
%define GITCOMMIT      947f3737a
%define _libexecdir %{_libdir}

Name:           xen-ovmf
Version:        %{GITDATE}
Release:        1.git%{GITCOMMIT}%{?dist}
Summary:        UEFI firmware for 64-bit virtual machines

License:        BSD
URL:            http://www.tianocore.org
Source0:        edk2-947f3737abf65fda63f3ffd97fddfa6986986868.tar.gz

BuildRequires:  nasm >= 2.10
BuildRequires:  gcc
BuildRequires:  libuuid-devel
BuildRequires:  /usr/bin/iasl


%description
OVMF (Open Virtual Machine Firmware) is a project to enable UEFI support for
Virtual Machines. This package contains a 64-bit UEFI firmware for Xen.


%prep
%setup -q -n edk2


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
* Thu Jan 25 2018 Anthony PERARD <anthony.perard@citrix.com> - 20170920-1.git947f3737a
- Bump with OVMF from Xen 4.10

* Wed Nov 29 2017 Anthony PERARD <anthony.perard@citrix.com> - 20160905-1.gitbc54e50e0
- New package, based on ovmf pkg and xen pkg

