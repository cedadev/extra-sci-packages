#!/bin/sh

set -e


include_closed_source=1
while true
do
    case "$1" in
	--no-closed-source)
	    include_closed_source=0
	    ;;
	*)
	    break
    esac
    shift
done

#echo $include_closed_source
#exit

install_latest() {
    name=$1
    files=rpmbuild/RPMS/noarch/$name-[0-9]*
    latest=`ls -t1 $files | head -n 1`
    sudo yum -y localinstall $latest
}

#-------
# build the meta package but initially install the components
# needed for the build of the software packages

if [ $include_closed_source -eq 1 ]
then
    flag="--with closed_source"
else
    flag=""
fi
./build_package.sh --no-install $flag jasmin-sci


# remove any existing top-level meta as will prevent updating
# the runtime (will reinstall it at every end)
sudo yum -y remove jasmin-sci jasmin-sci-build

# install the runtime/build packages just built
install_latest jasmin-sci-runtime
install_latest jasmin-sci-build


# add any other build deps
sudo yum -y install netcdf-devel proj-devel # for mtk
sudo yum -y install gtk2-devel # for leafpad
sudo yum -y install hdf-devel ncompress # for hdfeos2 / mtk
sudo yum -y install eccodes-devel cmake # for emos (required by umutil)

# Now build the software packages.  Names on this list are the file
# stems of the spec files.

# When updating this, remember also to update the meta RPM spec 
# (rpmbuild/specs/jasmin-sci.spec) with the names of the packages
# themselves.

for spec_file_prefix in \
    xconv               \
    mo_unpack           \
    leafpad             \
    tkdiff              \
    ferret-bin          \
    ferret-datasets     \
    hdfeos2             \
    mtk                 \
    libdrs              \
    libcrayutil         \
    umutil              \
    filesystem

do
    ./build_package.sh --install $spec_file_prefix
done


# Now same again for any closed source packages if including them
# (but without building the spec files).
#
if [ $include_closed_source -eq 1 ]
then
    # install build deps
    sudo yum -y install libcap-devel # for withgroups

    # package build
    for spec_file_prefix in \
	withgroups
	
    do
	./build_package.sh --install --no-srpm $spec_file_prefix
    done
fi

#----------------
# now install the top-level package - should install cleanly if all 
# dependencies have been satisfied
install_latest jasmin-sci
