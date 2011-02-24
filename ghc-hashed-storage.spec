%define		pkgname	hashed-storage
Summary:	Hashed file storage support code
Name:		ghc-%{pkgname}
Version:	0.5.2
Release:	2
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	9173f18fc672dab4e05d38092d5e7dc6
URL:		http://hackage.haskell.org/package/hashed-storage/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-binary
BuildRequires:	ghc-dataenc
BuildRequires:	ghc-mmap >= 1:0.5
BuildRequires:	ghc-zlib
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_releq	ghc
Requires:	ghc-binary
Requires:	ghc-dataenc
%requires_releq	ghc-mmap
Requires:	ghc-zlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Support code for reading and manipulating hashed file storage (where
each file and directory is associated with a cryptographic hash, for
corruption-resistant storage and fast comparisons).

The supported storage formats include darcs hashed pristine, a plain
filesystem tree and an indexed plain tree (where the index maintains
hashes of the plain files and directories).

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_defaultdocdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version} %{name}-%{version}-doc

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
%doc %{name}-%{version}-doc/html
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}
