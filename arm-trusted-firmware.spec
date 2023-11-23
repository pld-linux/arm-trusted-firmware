Summary:	ARM Trusted Firmware
Name:		arm-trusted-firmware
Version:	2.10.0
Release:	1
License:	BSD
Group:		Base/Kernel
Source0:	https://git.trustedfirmware.org/TF-A/trusted-firmware-a.git/snapshot/trusted-firmware-a-%{version}.tar.gz
# Source0-md5:	a262a00bae874ce7cb355d30fbee6767
URL:		https://developer.arm.com/tools-and-software/open-source-software/firmware/trusted-firmware
BuildRequires:	crossarm-gcc
BuildRequires:	dtc
BuildRequires:	openssl-tools
BuildRequires:	rpmbuild(macros) >= 1.750
ExclusiveArch:	aarch64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		binutils_ver	%(rpm -q --qf=%%{V} binutils)

%description
ARM Trusted firmware is a reference implementation of secure world
software for ARMv8-A including Exception Level 3 (EL3) software. It
provides a number of standard ARM interfaces like Power State
Coordination (PSCI), Trusted Board Boot Requirements (TBBR) and Secure
Monitor.

Note: the contents of this package are generally just consumed by
bootloaders such as u-boot. As such the binaries aren't of general
interest to users.

%package -n arm-trusted-firmware-armv8
Summary:	ARM Trusted Firmware for ARMv8-A

%description -n arm-trusted-firmware-armv8
ARM Trusted Firmware binaries for various ARMv8-A SoCs.

Note: the contents of this package are generally just consumed by
bootloaders such as u-boot. As such the binaries aren't of general
interest to users.

Note: the contents of this package are generally just consumed by
bootloaders such as u-boot. As such the binaries aren't of general
interest to users.

%prep
%setup -q -n trusted-firmware-a-%{version}

%build
%if %{_ver_ge "%binutils_ver" "2.39"}
export TF_LDFLAGS="--no-warn-rwx-segments"
%endif
for soc in rk3399; do
%{__make} \
	V=1 \
	HOSTCC="%{__cc} %{rpmcflags}" \
	CROSS_COMPILE="" \
	M0_CROSS_COMPILE="arm-linux-gnueabi-" \
	PLAT="$soc" \
	bl31
done
%{__make} -C tools/fiptool \
	V=1 \
	HOSTCC="%{__cc}" \
	HOSTCCFLAGS="%{rpmcflags}" \
	CPPFLAGS="%{rpmcppflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}}

for soc in rk3399; do
	install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/$soc
	for file in bl31/bl31.elf m0/rk3399m0.bin m0/rk3399m0.elf; do
		if [ -f build/$soc/release/$file ]; then
			cp -p build/$soc/release/$file $RPM_BUILD_ROOT%{_datadir}/%{name}/$soc
		fi
	done
done

cp -p tools/fiptool/fiptool $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files -n arm-trusted-firmware-armv8
%defattr(644,root,root,755)
%doc readme.rst
%attr(755,root,root) %{_bindir}/fiptool
%{_datadir}/%{name}
