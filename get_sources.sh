#!/bin/sh

topdir=`dirname $0`
rpmbuild_dir=$topdir/rpmbuild

# symlink any locally provided sources
ls $rpmbuild_dir/sources/ | while read name
do
    link_path=$rpmbuild_dir/SOURCES/$name
    if [ ! -e $link_path ]
    then
	ln -s ../sources/$name $link_path
    fi
done


# download and link any other sources
grep -v '^#' $topdir/source_urls | egrep . | while read url local_name
do
    if [ -z $local_name ]
    then
	local_name=`basename $url`
    fi

    download_path=$rpmbuild_dir/downloads/$local_name
    link_path=$rpmbuild_dir/SOURCES/$local_name

    if [ ! -e $download_path ]
    then
	wget -O $download_path $url
    fi
    if [ ! -e $link_path ]
    then
	ln -s ../downloads/$local_name $link_path
    fi
done
