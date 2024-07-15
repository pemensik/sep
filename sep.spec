%global forgeurl0 https://github.com/kbarbary/sep

%bcond_without tests

Version: 1.2.1
%forgemeta

Name: sep
# Ensure higher version than the last build of python-sep is used
Release: %autorelease -b 4
Summary: Astronomical source extraction and photometry in Python and C

# Code from photutils is BSD (src/overlap.h)
# Code from sextractor is LGPLv3+
# Python wrapper is MIT (sex.pyx)
License: MIT and LGPL-3 and BSD-3-Clause

URL: http://sep.readthedocs.org/
Source0: %forgesource0

BuildRequires: gcc
BuildRequires: cmake
BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: sed
%if %{with tests}
BuildRequires: tox
%endif

%global common_desc %{expand:
SEP makes available some of the astronomical source extraction and 
photometry algorithms in Source Extractor as stand-alone 
functions and classes. These operate directly on in-memory numpy arrays 
(no FITS files, configuration files, etc). It’s derived directly from 
(and tested against) the Source Extractor code base.}

%description
%{common_desc}

Native code shared library.

%package devel
Summary: Astronomical source extraction and photometry development files
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
%{common_desc}

Development header and library in native code.

%package -n python3-%{name}
Summary: Astronomical source extraction and photometry in Python
%{?python_provide:%python_provide python3-%{name}}

BuildRequires: %{py3_dist Cython}
BuildRequires: %{py3_dist setuptools}
BuildRequires: %{py3_dist numpy}

%description -n python3-%{name}
%{common_desc}


%generate_buildrequires
%if %{with tests}
  %pyproject_buildrequires -t
%else
  %pyproject_buildrequires
%endif
#

%prep
%forgeautosetup -p1
sed -e 's/"oldest-supported-numpy"/"numpy"/' -i pyproject.toml

%build
%cmake
%cmake_build
%pyproject_wheel

%install
%cmake_install
%pyproject_install
%pyproject_save_files %{name}

%check
%if %{with tests}
  %tox run
%endif

%files
%doc AUTHORS.md README.md CHANGES.md
%license licenses/MIT_LICENSE.txt licenses/LGPL_LICENSE.txt licenses/BSD_LICENSE.txt
%{_libdir}/libsep.so.0*

%files devel
%{_libdir}/libsep.so
%{_includedir}/sep.h

%files -n python3-%{name} -f %{pyproject_files}
%doc AUTHORS.md README.md CHANGES.md
%license licenses/MIT_LICENSE.txt licenses/LGPL_LICENSE.txt licenses/BSD_LICENSE.txt

%changelog
%autochangelog
