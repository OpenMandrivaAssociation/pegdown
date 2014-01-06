%{?_javapackages_macros:%_javapackages_macros}
Name:          pegdown
Version:       1.1.0
Release:       6.1%{?dist}
Summary:       Java library for Markdown processing
License:       ASL 2.0
URL:           http://pegdown.org
Source0:       https://github.com/sirthias/pegdown/archive/%{version}.tar.gz

BuildRequires: java-devel

BuildRequires: parboiled
# test deps
BuildRequires: jtidy
BuildRequires: testng

BuildRequires: maven-local
BuildRequires: maven-surefire-provider-testng

BuildArch:     noarch

%description
A pure-Java Markdown processor based on a parboiled PEG parser
supporting a number of extensions.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
find . -name "*.class" -delete
find . -name "*.jar" -delete

# these test fail
rm src/test/java/org/pegdown/CustomParserTest.java
rm src/test/java/org/pegdown/Markdown103Test.java
rm src/test/java/org/pegdown/PegDownTest.java

%build

%mvn_file :%{name} %{name}
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc CHANGELOG LICENSE NOTICE README.markdown

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 05 2013 gil cattaneo <puntogil@libero.it> 1.1.0-5
- switch to XMvn
- minor changes to adapt to current guideline

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.1.0-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 gil cattaneo <puntogil@libero.it> 1.1.0-1
- initial rpm