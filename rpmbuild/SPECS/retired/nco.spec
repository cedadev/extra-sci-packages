%define _name nco

%{?scl:%scl_package %{_name}}
Name:           %{?scl_pkg_name}%{?!scl_pkg_name:%{_name}}

Version: 5.1.9
Release: 1%{?dist}
License: GPL v3
Group: Scientific support	
Source: nco-%{version}.tar.gz	
#Patch0: nco-install_C_headers.patch
URL: http://nco.sourceforge.net/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gcc, gcc-c++, netcdf-devel, %{?scl:%{scl_prefix}}udunits-devel, antlr, antlr-C++, libcurl-devel, bison, byacc, flex, gsl-devel

Requires: netcdf, %{?scl:%{scl_prefix}}udunits, gsl
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Summary:  The netCDF Operators (NCO) perform a range of operations using netCDF files as input
Prefix: %{_prefix}
Packager: Alan Iwi <alan.iwi@stfc.ac.uk>
Vendor: Charlie Zender <zender@uci.edu>

%description					

The netCDF Operators (NCO) comprise about a dozen standalone,
command-line programs that take netCDF, HDF, and/or DAP files as
input, then operate (e.g., derive new fields, compute statistics,
print, hyperslab, manipulate metadata, regrid) and output the results
to screen or files in text, binary, or netCDF formats. NCO aids
analysis of gridded and unstructured scientific data. The
shell-command style of NCO allows users to manipulate and analyze
files interactively, or with expressive scripts that avoid some
overhead of higher-level programming environments.

Traditional geoscience data analysis requires users to work with
numerous flat (data in one level or namespace) files. In that paradigm
instruments or models produce, and then repositories archive and
distribute, and then researchers request and analyze, collections of
flat files. NCO works well with that paradigm, yet it also embodies
the necessary algorithms to transition geoscience data analysis from
relying solely on traditional (or “flat”) datasets to allowing newer
hierarchical (or “nested”) datasets.

The next logical step is to support and enable combining all
datastreams that meet user-specified criteria into a single or small
number of files that hold all the science-relevant data organized in
hierarchical structures. NCO (and no other software to our knowledge)
can do this now. We call the resulting data storage, distribution, and
analysis paradigm Group-Oriented Data Analysis and Distribution
(GODAD). GODAD lets the scientific question organize the data, not the
ad hoc granularity of all relevant datasets. The User Guide
illustrates GODAD techniques for climate data analysis:

   * ncap2 netCDF Arithmetic Processor (examples)
   * ncatted netCDF ATTribute EDitor (examples)
   * ncbo netCDF Binary Operator (addition, multiplication...) (examples)
   * ncclimo netCDF CLIMatOlogy Generator (examples)
   * nces netCDF Ensemble Statistics (examples)
   * ncecat netCDF Ensemble conCATenator (examples)
   * ncflint netCDF FiLe INTerpolator (examples)
   * ncks netCDF Kitchen Sink (examples)
   * ncpdq netCDF Permute Dimensions Quickly, Pack Data Quietly (examples)
   * ncra netCDF Record Averager (examples)
   * ncrcat netCDF Record conCATenator (examples)
   * ncremap netCDF REMAPer (examples)
   * ncrename netCDF RENAMEer (examples)
   * ncwa netCDF Weighted Averager (examples)

Note that the “averagers” (ncra and ncwa) are misnamed because they
perform many non-linear statistics as well, e.g., total, minimum,
RMS. Moreover, ncap2 implements a powerful domain language which
handles arbitrarily complex algebra, calculus, and statistics (using
GSL). The operators are as general as netCDF itself: there are no
restrictions on the contents of input file(s). NCO's internal routines
are completely dynamic and impose no limit on the number or sizes of
dimensions, variables, and files. NCO is designed to be used both
interactively and with large batch jobs. The default operator behavior
is often sufficient for everyday needs, and there are numerous command
line (i.e., run-time) options, for special cases.

# %package devel
# Group: Development/Libraries	
# Summary: Development libraries for NCO
# Requires: nco = %{version}, udunits, netcdf
# %description devel
# This package contains the libraries needed to build other code requiring 
# the library that comes with the netCDF operators (NCO).
# For further information see the description for the nco (non-devel) package.

%prep				
%setup -n %{_name}-%{version}
#%patch0 -p1 -b .install_C_headers

%build				
%configure
make


%install			
rm -rf $RPM_BUILD_ROOT		
make install DESTDIR=$RPM_BUILD_ROOT	

# not providing devel package (see comment in changelog below),
# so static libraries are of no use without the headers 
# (and cause packaging errors) - remove these
rm $RPM_BUILD_ROOT/%{_libdir}/libnco.{a,la}


%post
if test `whoami` == root; then
   echo "Running /sbin/ldconfig"
   /sbin/ldconfig
fi


%clean				
rm -rf $RPM_BUILD_ROOT		

%postun
if test `whoami` == root; then
   echo "Running /sbin/ldconfig"
   /sbin/ldconfig
fi

%files				
%defattr(0755,root,root)
%{_bindir}/ncap2
%{_bindir}/ncatted
%{_bindir}/ncbo
%{_bindir}/ncclimo
%{_bindir}/ncdiff
%{_bindir}/ncea
%{_bindir}/ncecat
%{_bindir}/nces
%{_bindir}/ncflint
%{_bindir}/ncks
%{_bindir}/ncpdq
%{_bindir}/ncra
%{_bindir}/ncrcat
%{_bindir}/ncremap
%{_bindir}/ncrename
%{_bindir}/ncwa
%defattr(0644,root,root)			
%{_libdir}/libnco-%{version}.so
#%{_libdir}/libnco_c++-%{version}.so
#%{_libdir}/libnco_c++.so
%{_libdir}/libnco.so
%doc %{_datadir}/info/nco.info.gz
%doc %{_datadir}/info/nco.info-1.gz
%doc %{_datadir}/info/nco.info-2.gz
%doc %{_datadir}/info/nco.info-3.gz
%doc %{_datadir}/info/nco.info-4.gz
#%doc %{_datadir}/info/nco.info-5.gz
%exclude %{_datadir}/info/dir
#%doc %{_mandir}/man1/ncap.1.gz
%doc %{_mandir}/man1/ncap2.1.gz
%doc %{_mandir}/man1/ncatted.1.gz
%doc %{_mandir}/man1/ncbo.1.gz
%doc %{_mandir}/man1/ncclimo.1.gz
%doc %{_mandir}/man1/ncecat.1.gz
%doc %{_mandir}/man1/nces.1.gz
%doc %{_mandir}/man1/ncflint.1.gz
%doc %{_mandir}/man1/ncks.1.gz
%doc %{_mandir}/man1/nco.1.gz
%doc %{_mandir}/man1/ncpdq.1.gz
%doc %{_mandir}/man1/ncra.1.gz
%doc %{_mandir}/man1/ncrcat.1.gz
%doc %{_mandir}/man1/ncremap.1.gz
%doc %{_mandir}/man1/ncrename.1.gz
%doc %{_mandir}/man1/ncwa.1.gz

# %files devel
# %defattr(0644,root,root)			
# %{_includedir}/libnco_c++.hh
# %{_includedir}/nco_att.hh
# %{_includedir}/nco_dmn.hh
# %{_includedir}/nco_fl.hh
# %{_includedir}/nco_hgh.hh
# %{_includedir}/nco_utl.hh
# %{_includedir}/nco_var.hh
# %{_libdir}/libnco.a
# %{_libdir}/libnco_c++.a
# %{_libdir}/libnco_c++.la
# %{_libdir}/libnco.la

%changelog
* Tue Jun 7 2022  <alan.iwi@stfc.ac.uk> - 5.0.7
- later version and adapt for SCL
- remove devel package per https://github.com/nco/nco/blob/22723199484a4d7e897cc582353a3afa536f5c57/src/nco/Makefile.in#L783-L786

* Sat Mar 31 2018  <builderdev@builder.jc.rl.ac.uk> - 4.7.3-1.ceda
- bump version (tweak file lists)

* Thu Apr  7 2016  <builderdev@builder.jc.rl.ac.uk> - 4.5.5-1.ceda
- update to 4.5.5 - tweak file list

* Wed Feb  5 2014  <builderdev@builder.jc.rl.ac.uk> - 4.4.1-1.ceda
- upgrade to 4.4.1 (some additions to file list, particularly nces)

* Tue Aug 20 2013  <builderdev@builder.jc.rl.ac.uk> - 4.3.4-2.ceda
- devel depends on explicit version of nco

* Tue Aug 20 2013  <builderdev@builder.jc.rl.ac.uk> - 4.3.4-1.ceda
- migrate to 4.3.4, tidy spec file, add gsl dependency
			
* Mon Aug 13 2012 Alan Iwi
alan.iwi@stfc.ac.uk 4.2.1
- Created initial RPM for netCDF 4.2.1 (modelled on RPM for HDF5 1.8.9)
