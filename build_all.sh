#!/bin/sh

set -e

install_latest() {
    name=$1
    files=rpmbuild/RPMS/noarch/$name-[0-9]*
    latest=`ls -t1 $files | head -n 1`
    sudo yum -y localinstall $latest
}

#-------
# build the meta package but initially install the components
# needed for the build of the software packages

./build_package.sh --no-install ceda-sci
install_latest ceda-sci-runtime
install_latest ceda-sci-build


# add any build deps
sudo yum -y install vte-devel intltool  # for lxterminal
sudo yum -y install hdf-devel ncompress # for hdfeos2 / mtk
sudo yum -y install eccodes-devel cmake # for emos (required by umutil)



# Now build the software packages.  Names on this list are the file
# stems of the spec files.

# When updating this, remember also to update the meta RPM spec 
# (rpmbuild/specs/ceda-sci.spec) with the names of the packages
# themselves.

for spec_file_prefix in "
    xconv
    mo_unpack
    lxterminal
    leafpad
    tkdiff
    nccmp
    ferret-bin
    ferret-datasets
    hdfeos2
    mtk
    diffuse
    emos
    libdrs
    libcrayutil
    umutil
"
do
    ./build_package.sh --install $spec_file_prefix
done

#----------------
# now install the top-level package - should install cleanly if all 
# dependencies have been satisfied
install_latest ceda-sci
