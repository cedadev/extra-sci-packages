#!/bin/bash

#
# Builds a package. 
#
# The command line argument is the file stem of the spec file.
#

case "$1" in
    --no-install)
	install=no
	shift
	;;
    --install)
	install=yes
	shift
	;;
    *)
	install=ask
	;;
esac

spec_file_name=$1.spec
thisdir=`pwd`
topdir=$thisdir/rpmbuild
spec_file=$topdir/SPECS/$spec_file_name


build_srpm() {

    spec_file=$1

    echo "Packaging SRPM"

    output=$(rpmbuild --define "_topdir $topdir" -bs $spec_file)
    status=$?
    srpm=`echo "$output" | awk '/Wrote:/{print $2}'`

    if [ -z $srpm ]
    then
	status=1
    fi    
    if [ $status -ne 0 ]
    then
        echo "could not build srpm" >&2
    fi

    echo $srpm
    return $status
}


echo "Building from: $spec_file"

time_file=$topdir/buildtimes/${spec_file_name/spec/buildtime}
time_file_tmp=$time_file.tmp

if [ -e $time_file ]
then
    last_time=$(awk '/real/{print int($2)}' $time_file)
    echo "previous build of this package took $last_time seconds"
    end_time=$(date -d "+$last_time second")
    echo "estimated completion time: $end_time"
    echo "====================================="
    if [ $last_time -gt 60 ]
    then
        sleep 3  # give some time to read it before more output is printed
    fi
fi


buildtmp=_build_tmp.$$

#=============
# With mock would use "mock -r epel-7-x86_64" in place of "rpmbuild"
# but not is working.  Also mock requires building SRPM first and then 
# using "--rebuild <srpm>" in place of "-bb <spec>" and also has side 
# effect of removing source and spec file.  This is not used here.
#=============

/usr/bin/time -p -o $time_file_tmp \
    rpmbuild \
        --define "_topdir $topdir" \
        --define "scl jasmin-sci" \
        --define "%debug_package %{nil}" \
        -bb $spec_file \
        | tee $buildtmp
    
status=${PIPESTATUS[0]}

if [ $status -eq 0 ]
then
    echo "Build succeeded"

    mv $time_file_tmp $time_file
    rpms=$(perl -lane '/^Wrote: (.*\.rpm)/ && ! /debuginfo/ && print $F[1]' $buildtmp)
    echo "Binary rpms built:"
    echo $rpms | fmt -1

    # create source RPM only following on a successful build, in order to keep 
    # source and binary RPMs in sync (if the build was unsuccessful then 
    # the binary RPM from last successful build was not overwritten so don't update
    # the source RPM)
    build_srpm $spec_file

    if [ $install = ask ]
    then
	echo -n "Install binaries? "
	read ans
	ans=$(echo $ans | cut -b 1)
	if [ "$ans" = y -o "$ans" = Y ]
	then
	    install=yes
	else
	    install=no
	fi
    fi

    if [ $install = yes ]
    then
        sudo yum -y localinstall $rpms || sudo yum -y reinstall $rpms
        #./elogger.py -i builder.jc.rl.ac.uk $rpms
    fi    

else
    echo "Build failed"
    mv $time_file_tmp $time_file.lastfailed
fi

rm -f $buildtmp

exit $status
