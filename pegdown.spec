%{?_javapackages_macros:%_javapackages_macros}
Name:          pegdown
Version:       1.4.2
Release:       3.3
Summary:       Java library for Markdown processing
Group:		Development/Java
License:       ASL 2.0
URL:           http://pegdown.org
Source0:       https://github.com/sirthias/pegdown/archive/%{version}.tar.gz
# Newer release use sbt builder
Source1:       http://repo1.maven.org/maven2/org/pegdown/pegdown/%{version}/pegdown-%{version}.pom
# Forwarded upstream: https://github.com/sirthias/pegdown/pull/130
Patch0:        %{name}-rhbz1096735.patch

BuildRequires: java-devel
BuildRequires: mvn(org.parboiled:parboiled-java)
# test deps
BuildRequires: mvn(net.sf.jtidy:jtidy)
%if 0
BuildRequires: mvn(org.specs2:specs2_2.9.3)
%endif
BuildRequires: maven-local

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
%patch0 -p1

cp -p %{SOURCE1} pom.xml

%pom_xpath_inject "pom:project" "
<build>
  <plugins>

  </plugins>
</build>"

%pom_xpath_inject "pom:build" "
<resources>
  <resource>
    <directory>.</directory>
    <targetPath>\${project.build.outputDirectory}/META-INF</targetPath>
    <includes>
      <include>LICENSE</include>
      <include>NOTICE</include>
    </includes>
  </resource>
</resources>"

%pom_add_plugin org.apache.maven.plugins:maven-jar-plugin . "
<configuration>
  <archive>
    <manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
    <manifest>
      <addDefaultImplementationEntries>true</addDefaultImplementationEntries>
      <addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
    </manifest>
  </archive>
</configuration>"

%pom_add_plugin org.apache.felix:maven-bundle-plugin . "
<extensions>true</extensions>
<configuration>
  <instructions>
    <Built-By>\${user.name}</Built-By>
    <Bundle-SymbolicName>org.pegdown</Bundle-SymbolicName>
    <Bundle-Name>pegdown</Bundle-Name>
    <Bundle-Vendor>pegdown.org</Bundle-Vendor>
    <Bundle-Version>\${project.version}</Bundle-Version>
  </instructions>
</configuration>
<executions>
  <execution>
    <id>bundle-manifest</id>
    <phase>process-classes</phase>
    <goals>
      <goal>manifest</goal>
    </goals>
  </execution>
</executions>"

rm -r src/test/scala/*
%pom_remove_dep org.specs2:specs2_2.9.3

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
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.2-2
- Fix invalid HTML when serializing images
- Resolves: rhbz#1096735

* Thu Mar 20 2014 gil cattaneo <puntogil@libero.it> 1.4.2-1
- update to 1.4.2

* Tue Nov 26 2013 gil cattaneo <puntogil@libero.it> 1.4.1-1
- update to 1.4.1 rhbz#1034825

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

