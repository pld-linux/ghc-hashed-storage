%define		pkgname	hashed-storage
Summary:	Hashed file storage support code
Name:		ghc-%{pkgname}
Version:	0.5.8
Release:	1
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	31abd73fc4566e04b056fc22acdec2aa
URL:		http://hackage.haskell.org/package/hashed-storage/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-binary
BuildRequires:	ghc-dataenc
BuildRequires:	ghc-mmap >= 1:0.5
BuildRequires:	ghc-zlib
BuildRequires:	rpmbuild(macros) >= 1.608
Requires:	ghc-binary
Requires:	ghc-dataenc
Requires:	ghc-zlib
%requires_eq	ghc
%requires_eq	ghc-mmap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
Support code for reading and manipulating hashed file storage (where
each file and directory is associated with a cryptographic hash, for
corruption-resistant storage and fast comparisons).

The supported storage formats include darcs hashed pristine, a plain
filesystem tree and an indexed plain tree (where the index maintains
hashes of the plain files and directories).

%package doc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname}.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc NEWS
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
