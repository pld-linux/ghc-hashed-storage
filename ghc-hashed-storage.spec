Summary:	Hashed file storage support code
Name:		haskell-hashed-storage
Version:	0.4.3
Release:	0.1
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/hashed-storage/0.4.3/hashed-storage-%{version}.tar.gz
# Source0-md5:	a8427578dc13006689158cd9f2c90e56
URL:		http://hackage.haskell.org/package/hashed-storage/
BuildRequires:	haskell
BuildRequires:	haskell-binary
BuildRequires:	haskell-dataenc
BuildRequires:	haskell-mmap
BuildRequires:	haskell-zlib
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Support code for reading and manipulating hashed file storage (where
each file and directory is associated with a cryptographic hash, for
corruption-resistant storage and fast comparisons).

The supported storage formats include darcs hashed pristine, a plain
filesystem tree and an indexed plain tree (where the index maintains
hashes of the plain files and directories).

%prep
%setup -q -n hashed-storage-%{version}

%build
runhaskell Setup.hs configure --prefix=%{_prefix}
runhaskell Setup.hs build

%install
rm -rf $RPM_BUILD_ROOT
runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS
