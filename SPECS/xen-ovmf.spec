
%define GITDATE        20160905
%define GITCOMMIT      bc54e50e0
%define _libexecdir %{_libdir}

Name:           xen-ovmf
Version:        %{GITDATE}
Release:        1.git%{GITCOMMIT}%{?dist}
Summary:        UEFI firmware for 64-bit virtual machines

License:        BSD
URL:            http://www.tianocore.org
Source0:        edk2-bc54e50e0fe03c570014f363b547426913e92449.tar.gz

BuildRequires:  nasm gcc
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
# ls -d Build/OvmfX64/RELEASE_GCC48/X64/*Pkg
for pkg in FatPkg IntelFrameworkModulePkg MdeModulePkg MdePkg OptionRomPkg OvmfPkg PcAtChipsetPkg ShellPkg UefiCpuPkg; do
  copy_license $pkg/License.txt $pkg
done

install -D -m 644 Build/OvmfX64/RELEASE_GCC*/FV/OVMF.fd %{buildroot}/%{_libexecdir}/xen/boot/OVMF.fd


%files
%doc %{_docdir}/%{name}/Licenses/FatPkg-License.txt
%doc %{_docdir}/%{name}/Licenses/IntelFrameworkModulePkg-License.txt
%doc %{_docdir}/%{name}/Licenses/MdeModulePkg-License.txt
%doc %{_docdir}/%{name}/Licenses/MdePkg-License.txt
%doc %{_docdir}/%{name}/Licenses/OptionRomPkg-License.txt
%doc %{_docdir}/%{name}/Licenses/OvmfPkg-License.txt
%doc %{_docdir}/%{name}/Licenses/ShellPkg-License.txt
%doc %{_docdir}/%{name}/Licenses/PcAtChipsetPkg-License.txt
%doc %{_docdir}/%{name}/Licenses/UefiCpuPkg-License.txt

%{_libexecdir}/xen/boot/OVMF.fd


%changelog
* Wed Nov 29 2017 Anthony PERARD <anthony.perard@citrix.com> - 20160905-1.gitbc54e50e0
- New package, based on ovmf pkg and xen pkg

