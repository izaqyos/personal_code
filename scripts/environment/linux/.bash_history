ct lsstream
grep builtin runtime/prebuilt/lnx26/etc/centrifydc.conf 
cdacs_view
resume_edit ~/work/vim_sessions/ad_files 
crontab
ct lsstream
svs
ct pwv
list_COs 
ct lsco -all -me | grep yizaq.P3.P2.P1.FCS_5_3.int.acs5_0 | awk '{print }' | sed -e 's_"__g'
ci_all.sh 
hist update_5_3_p_1_files2replace
~/work/scripts/centrify/update_5_3_p_1_files2replace 
ls /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/runtime/flow/radius/radiusAuthenFlow/src/Debug/libRadiusRequestFlow.so
ls /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/runtime/flow/radius/radiusAuthenFlow/src/Debug/libRadiusAuthenFlow.so 
ls /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/runtime/flow/radius/radiusAuthenFlow/src/Debug/libRadiusRequestFlow.so
mc; mist
~/work/scripts/centrify/update_5_3_p_1_files2replace 
ls patches_5_3/5-3-0-40/files/CLI.war 
ls patches_5_3/5-3-0-40/files/cli-framework-5.3.0.40.100.war
ls patches_5_3/5-3-0-40/files/acs-db-5.3.0.40.B.839.jar
ls /ws/yizaq-csi/maven-repo/view/yizaq__yizaq.P1.FCS_5_3.int.acs5_0.lx/com/cisco/nm/acs/mgmt/cli/app/cli-framework/5.3.0.40.100/cli-framework-5.3.0.40.100.war
ls view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/view/modules/dataupgrade/target/dataupgrade-5.0.jar
~/work/scripts/centrify/update_5_3_p_1_files2replace 
~/work/scripts/centrify/update_5_3_p_1_files2replace 
ls /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs//mgmt/cli/app/cli-framework/5.3.0.40.100/cli-framework-5.3.0.40.100.war
ls /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/mgmt/cli/app/cli-framework/5.3.0.40.100/cli-framework-5.3.0.40.100.war
find . -name 'cli-framework-5.3.0.40.100.war'
ls /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/mgmt/cli/app/target/cli-framework-5.3.0.40.100.war 
~/work/scripts/centrify/update_5_3_p_1_files2replace 
ls /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs//mgmt/cli/app/target/cli-framework/5.3.0.40.100/cli-framework-5.3.0.40.100.war
ls /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/mgmt/cli/app/target/cli-framework/5.3.0.40.100/cli-framework-5.3.0.40.100.war
find . -name 'cli-framework-5.3.0.40.100.war'
~/work/scripts/centrify/update_5_3_p_1_files2replace 
~/work/scripts/centrify/update_5_3_p_1_files2replace 
hist pack
cd patches_5_3/
ls 5-3-0-40/
rm 5-3-0-40//5-3-0-40-1_AD*
./patch.sh  pack 5-3-0-40-3 5-3-0-40/
cd 5-3-0-40/
ls
ftp cd-acs-ftp
ls -l
sha1sum 5-3-0-40-3.tar.gpg 
grep builtin files/centrifydc.conf 
sha1sum files/centrifydc.conf
sha1sum files/libRadiusAuthenFlow.so 
sha1sum files/libRadiusRequestFlow.so 
cdacs_view
resume_edit ~/work/vim_sessions/ad_files 
AD_CLI_BINS=(adfinddomain     adkeytab     adsmb              fix_pam_rsh.sh  ldapdelete  adfixid          adleave      adupdate           ldapmodify  adcache           adflush          adobfuscate  ldapmodrdn  adcheck           adgpupdate       adpasswd     ldapsearch  adclient          adid             adquery      cdcexec            adinfo           adreload     cdcwatch           addns             adinfo_extra.sh  adrmlocal    ldapadd         adenv             adjoin           adsetgroups  ldapcompare     adlicense)
export CENT_4_5_349="/ws/yizaq-csi/temp/centrify/"
for c in ${AD_CLI_BINS[@]} ; do sha1sum `find $CENT_4_5_349 -type f -name $c ` $c >/dev/null; done
echo $CENT_4_5_349
for c in ${AD_CLI_BINS[@]} ; do find $CENT_4_5_349 -type f -name $c   ; done
for c in ${AD_CLI_BINS[@]} ; do sha1sum `find $CENT_4_5_349 -type f -name $c`   ; done
sha1sum  runtime/prebuilt/lnx26/bin/adcache 
sha1sum  patches_5_3/5-3-0-40/files/adcache
strings   runtime/prebuilt/lnx26/bin/adcache 
strings   runtime/prebuilt/lnx26/bin/adcache  | grep 4.5
strings   runtime/prebuilt/lnx26/bin/adreload 
cat   runtime/prebuilt/lnx26/bin/adreload 
sha1sum patches_5_3/5-3-0-40/files/libcapi*
sha1sum patches_5_3/5-3-0-40/files/libcapi* runtime/prebuilt/lnx26/lib/libcapi.so 
sha1sum patches_5_3/5-3-0-40/files/libcapi* runtime/prebuilt/lnx26/lib/libcapi.so 
sha1sum patches_5_3/5-3-0-40/files/libcapi* runtime/prebuilt/lnx26/lib/libcapi.so  | grep -v contrib
sha1sum patches_5_3/5-3-0-40/files/liblrpc* runtime/prebuilt/lnx26/lib/libcapi.so  | grep -v contrib
sha1sum patches_5_3/5-3-0-40/files/libcapi* runtime/prebuilt/lnx26/lib/libcapi.so  | grep -v contrib
g^libcapi^liblrpc^
sha1sum patches_5_3/5-3-0-40/files/libcapi* runtime/prebuilt/lnx26/lib/libcapi.so  | grep -v contrib
sha1sum patches_5_3/5-3-0-40/files/libcapi* runtime/prebuilt/lnx26/lib/libcapi.so  | grep -v contribsg^libcapi^liblrpc^
sha1sum patches_5_3/5-3-0-40/files/libcapi* runtime/prebuilt/lnx26/lib/libcapi.so  | grep -v contrib
sha1sum patches_5_3/5-3-0-40/files/libcapi* runtime/prebuilt/lnx26/lib/libcapi.so  | grep -v contribsg/libcapi/liblrpc/
sha1sum patches_5_3/5-3-0-40/files/libcapi* runtime/prebuilt/lnx26/lib/libcapi.so  | grep -v contrib
 sha1sum patches_5_3/5-3-0-40/files/libcapi* runtime/prebuilt/lnx26/lib/libcapi.so  | grep -v contribs/libcapi/liblrpc/g
sha1sum patches_5_3/5-3-0-40/files/libcapi* runtime/prebuilt/lnx26/lib/libcapi.so  | grep -v contrib
sha1sum patches_5_3/5-3-0-40/files/libcapi* runtime/prebuilt/lnx26/lib/libcapi.so  | grep -v contrib
sha1sum patches_5_3/5-3-0-40/files/liblrpc* runtime/prebuilt/lnx26/lib/libcapi.so  | grep -v contribg
sha1sum patches_5_3/5-3-0-40/files/liblrpc* runtime/prebuilt/lnx26/lib/liblrpc.so  | grep -v contribg
sha1sum patches_5_3/5-3-0-40/files/libcapi* runtime/prebuilt/lnx26/lib/libcapi.so  | grep -v contrib
list_COs 
ct lsco -all -me | grep yizaq.P3.P2.P1.FCS_5_3.int.acs5_0 | awk '{print }' | sed -e 's_"__g' 
ci_all.sh 
cd patches_5_3/
ls 5-3-0-40/
rm 5-3-0-40//tar*
rm 5-3-0-40/*.tar*
./patch.sh  pack 5-3-0-40-3 5-3-0-40/
cd 5-3-0-40/
ls -ltr 
ftp cd-acs-ftp
ls -l files/adca
cp -r files/ $WS/temp
diff -r files/ /ws/yizaq-csi/temp/files/
cd ~/work/scripts/centrify/
./update_5_3_p_1_files2replace
cd -
sha1sum  files/adcache files/adreload 
ls
rm *.tar*
cd ..
./patch.sh  pack 5-3-0-40-3 5-3-0-40/
cd -
ftp cd-acs-ftp
cdacs_view
ci_all.sh 
diff -r patches_5_3/5-3-0-40/files/ /view/yizaq__P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/
find . -name '*.contrib' | xargs rm -f 
diff -r patches_5_3/5-3-0-40/files/ /view/yizaq__P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/
my_rebase
ct lsact
ct_diff_act_txt rebase.yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.20120401.154454
ct lsact rebase.yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.20120401.154454
ct lsact rebase.yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.20120401.154454@/vob/nmtgre
$ AD_CONFS=`ls runtime/prebuilt/lnx26/etc/`
AD_CONFS=`ls runtime/prebuilt/lnx26/etc/`
echo 
echo $AD_CONFS 
export CENT_4_5_350="/ws/yizaq-csi/temp/centrify/"
echo $CENT_4_5_350
cd runtime/prebuilt/lnx26/etc/
for c in ${AD_CONFS[@]} ; do if diff -q `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else tkdiff `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c; fi ; done
cd ../include/adagent/
 AD_HS=`\ls *.h`
echo $AD_HS 
for c in ${AD_HS[@]} ; do if diff -q `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else echo $c diff && diff `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c; fi ; done 
for c in ${AD_HS[@]} ; do if diff -q `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else echo $c diff && diff `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c; fi ; done  > ~/stam
cd ../../bin/
AD_CLI_BINS=(adfinddomain     adkeytab     adsmb              fix_pam_rsh.sh  ldapdelete  adfixid          adleave      adupdate           ldapmodify  adcache           adflush          adobfuscate  ldapmodrdn  adcheck           adgpupdate       adpasswd     ldapsearch  adclient          adid             adquery      cdcexec            adinfo           adreload     cdcwatch           addns             adinfo_extra.sh  adrmlocal    ldapadd         adenv             adjoin           adsetgroups  ldapcompare     adlicense) 
echo ${AD_CLI_BINS[@]} 
/lib/libc-2.3.4.so 
ldd adclient 
 /usr/lib/libstdc++.so.6 
echo ${AD_CLI_BINS[@]} 
for c in ${AD_CLI_BINS[@]} ; do sha1sum `find $CENT_4_5_349 -type f -name $c`   ; done
for c in ${AD_CLI_BINS[@]} ; do if diff -q `find $CENT_4_5_349 -type f -name $c ` $c >/dev/null ; then echo $c same; else echo $c differ; fi ; done
for c in ${AD_CLI_BINS[@]} ; do if diff -q `find $CENT_4_5_350 -type f -name $c ` $c >/dev/null ; then echo $c same; else echo $c differ; co $c; cp `find $CENT_4_5_350 -type f -name $c ` $c;  sha1sum `find $CENT_4_5_350 -type f -name $c ` $c ; fi ; done
ct lsact
ct mkact yizaq_INTEGRATE_CENTRIFY_4_5_0_350
for c in ${AD_CLI_BINS[@]} ; do if diff -q `find $CENT_4_5_350 -type f -name $c ` $c >/dev/null ; then echo $c same; else echo $c differ; co $c; cp `find $CENT_4_5_350 -type f -name $c ` $c;  sha1sum `find $CENT_4_5_350 -type f -name $c ` $c ; fi ; done
for c in ${AD_CLI_BINS[@]} ; do if diff -q `find $CENT_4_5_349 -type f -name $c ` $c >/dev/null ; then echo $c same; else echo $c differ; fi ; done
strings * | grep '4.5.0' 
vi ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash
ls
cd ../lib/
 ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash
cdacs_view
cdacs_view
cd runtime/idstores/activeDirectoryIDStore/
make sa SA_TEXT_ONLY=1
mc; mist; make sa SA_TEXT_ONLY=1
mc; mist; 
cdacs_view
mc; mist
cd -
make clean; make ; make sa SA_TEXT_ONLY=1
make clean; make ; 
cd ../..
cd ..
mc ; mist
cd -
cd idstores/activeDirectoryIDStore/
make sa SA_TEXT_ONLY=1
ls -lrt
/auto/ses/repository/sa10/static_analysis/static_logtohtml
make sa 
cat http://wwwin-ses.cisco.com/sa_html_results5/yizaq.3_14_2012.1__int.acs5_0.lx.1
wget http://wwwin-ses.cisco.com/sa_html_results5/yizaq.3_14_2012.1__int.acs5_0.lx.1
ls
cat index.html 
make sa SA_TEXT_ONLY=1
ls
cat acsRuntime.log 
ls
ls localStore/
find . -name '*.log'
cat src/ses_static_analysis_details.log 
cat src/ses_static_analysis.log 
cd ../..
make sa SA_TEXT_ONLY=1
cd -
rm src/ses_static_analysis.log 
make sa SA_TEXT_ONLY=1
make ; make sa SA_TEXT_ONLY=1
cat src/ses_static_analysis.log 
cd -
make clean; make ; make sa SA_TEXT_ONLY=1
cd dataAccess/
 make sa SA_TEXT_ONLY=1
make ;  make sa SA_TEXT_ONLY=1
cd $WS
export CENT_4_5_349="/ws/yizaq-csi/temp/centrify/"
echo $CENT_4_5_349 
export CENT_4_5_350="/ws/yizaq-csi/temp/centrify/"
echo $CENT_4_5_350
cd $CENT_4_5_350 
ls
rm -fr *
cp /ws/yizaq-csi/work/Acs/Centrify/4_5/350/* .
ls
for f in `ls` ; do extract_rpm $f . ; done
find . -name 'libc.so*'
find . -name 'libc'
find . -name libc
find . -name libgcc
find . -name libgcc*
find . -name 
find . -name 'libc*.so'
ldd ./usr/share/centrifydc/lib/libcapi.so
find . -name 'libstdc*.so'
sum ./usr/share/centrifydc/lib/libstdc++.so
md5sum ./usr/share/centrifydc/lib/libstdc++.so
ldd -v ./usr/share/centrifydc/lib/libcapi.so
find . -name 'liblrpc*'
ldd ./usr/share/centrifydc/lib/liblrpc.so
./usr/share/centrifydc/lib/liblrpc.so
find . -name 'libc*.so'
find . -name 'libc*'
cdacs_view
mc; mist
resume_edit ~/work/vim_sessions/ad_files 
ldd --version
ls -l /lib/libc-2.3.4.so 
elf /lib/libc-2.3.4.so
nm /lib/libc-2.3.4.so
nm /lib/libc-2.3.4.so | head
strings  /lib/libc-2.3.4.so 
strings  /lib/libc-2.3.4.so  | grep version
strings  /lib/libc-2.3.4.so  | grep version
ct lsact -cact
cdacs_view
ct lsact
my_rebase 
ct lsvtree -g runtime/prebuilt/lnx26/etc/centrifydc.conf 
ct mkact yizaq_CSCty60512
co runtime/prebuilt/lnx26/etc/centrifydc.conf
ci runtime/prebuilt/lnx26/etc/centrifydc.conf
mc; mist
ci_all.sh 
find . -name '*.rpm'
uninstall_acs_lnx 
rpm -ivh --no-md5 ./install/target/rpm/RPMS/i386/acs-5.4.0.18-100.i386.rpm
rpm -ivh --nomd5 ./install/target/rpm/RPMS/i386/acs-5.4.0.18-100.i386.rpm
sudo rpm -ivh --nomd5 ./install/target/rpm/RPMS/i386/acs-5.4.0.18-100.i386.rpm
cat /opt/CSCOacs/logs/acsDiskSpaceMgmt.log
acs_monit_start
acs_monit_summary 
acs_monit_restart
my_rebase 
deliver -graph
vi ~/.aliases 
ls
resume_edit ~/work/vim_sessions/cars_files 
ls
ls
stat cscope.files 
stat -s cscope.files 
stat -c cscope.files 
my_rebase 
ct lsact
ct lsstream
ct pwv
ct lsact yizaq_CSCtt13643
ct lsact yizaq_CSCtt13643@/vob/nmtgre
ct lsact -act q_CSCtt13643
ct lsact -act yizaq_CSCtt13643
ct lsact  yizaq_CSCtt13643
ct lsact  yizaq_5_4_NTPD_monit
ct lsact  yizaq_5_4_disk_space
grepa lsact ~/.aliases 
ct_lsact yizaq_5_4_disk_space
grep -C 6 _ct_ls_act ~/.aliases 
grep -C 6 _ct_lsact ~/.aliases 
ct lsact 
ct lsact | awk '{print $2}' 
for act in $( ct lsact | awk '{print $2}' ) do ; echo files changed in $act are; ct_lsact $act; done
for act in $( ct lsact | awk '{print $2}' ) ;do  echo files changed in $act are; ct_lsact $act; done
for act in $( ct lsact | awk '{print $2}' ) ;do  echo files changed in $act are; ct_lsact $act; done | grep .cpp
grep -C 6 _ct_lsact ~/.aliases 
for act in $( ct lsact | awk '{print $2}' ) ;do  echo files changed in $act are; ct_lsact $act; done | grep .cpp
cd $WS
cd temp/
wget http://acs-build1-lnx/auto/acs/acs_5.4_il/29/images/acs.tar.gz
ls
rm acs.tar.gz 
mv acs.tar.gz.1  acs.tar.gz
ftp cd-acs-ftp
ssh root@10.56.24.158
ct pwv
cdacs_view
ct lsact -cact
ct lsact
ct setact yizaq_CSCty31541
. ~/.aliases 
ct_diff_act_txt yizaq_CSCty31541
resume_edit ~/work/vim_sessions/cars_files 
ct_diff_act_txt yizaq_CSCty31541
ci_all.sh 
ct_diff_act_txt yizaq_CSCty31541
ct_diff_act_txt yizaq_CSCty31541 > ~/stam
search_in_files ADE
find -type f | xargs grep -sw ADE
cd $WS 
cd temp/
ls
rm acs.tar.gz 
wget http://acs-build1-lnx/auto/acs/acs_5.4_il/17/images/acs.tar.gz
tar -tzf acs.tar.gz 
tar -xvf acs.tar.gz ./manifest.xml
tar -xvf acs.tar.gz  manifest.xml
tar --extract --file=acs.tar.gz  manifest.xml
tar --extract --file=acs.tar.gz  ./manifest.xml
tar -xvf acs.tar.gz  manifest.xml
tar -xvf acs.tar.gz  ./manifest.xml
gunzip  acs.tar.gz 
tar xvf acs.tar
ct lsco -l -avobs -me
exit
svs
cdacs_view
resume_edit ~/work/vim_sessions/cars_files 
my_rebase 
search_in_files 'AUDIT_LOG.MaxBackupIndex=10'
svs
cdacs_view
mc; mist
mist
syncme
mist
mist
xts_small 
cdacs_view
my_rebase
deliver -graph
ct lsact
grepa diff
ct lsact
ct_diff_act_txt yizaq_CSCty31541
ct_diff_act_txt yizaq_CSCty31541 > ~/stam
code_review_info 
vncconfig &
cd install/
ls
cd ..
vncconfig &
search_in_files 'RuntimeDebugLog.config'
find . -name ManagementDebugLog.config
my_rebase 
deliver -graph
search_in_files  MaxBackupIndex
search_in_files  MaxBackupIndex | grep 10
svs
cdacs_view
my_rebase
deliver -graph
ct lsact
grepa diff
ct lsact
ct_diff_act_txt yizaq_CSCty31541
ct_diff_act_txt yizaq_CSCty31541 > ~/stam
code_review_info 
vncconfig &
cd install/
ls
cd ..
vncconfig &
search_in_files 'RuntimeDebugLog.config'
find . -name ManagementDebugLog.config
my_rebase 
deliver -graph
search_in_files  MaxBackupIndex
search_in_files  MaxBackupIndex | grep 10
svs
ct lsco ?
ct lsco help
ct lsco
ct lsco yizaq__yizaq.fcs5_1.int.acs5_0.lx
ct help
ct help | less
svs
echo $VIEWS
        Views=( ;                         "yizaq1__int.acs5_0.lx"   ;                         "yizaq__yizaq.fcs5_1.int.acs5_0.lx"   ;                         "yizaq__yizaq.FCS_5_2.int.acs5_0.lx"   ;                         "yizaq__FCS_5_3.int.acs5_0.lx";                         "yizaq__yizaq_5_4.int.acs5_0.lx";                         "yizaq__P1.FCS_5_3.int.acs5_0.lx";                         "yizaq__yizaq.P1.FCS_5_3.int.acs5_0.lx";                         "yizaq__P2.P1.FCS_5_3.int.acs5_0.lx";                         "yizaq__yizaq_5_4_centrify.int.acs5_0.lx";                         "yizaq__P3.P2.P1.FCS_5_3.int.acs5_0.lx";                         "yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx";                         )
echo $VIEWS
echo ${VIEWS[@]}
ct pwv
svs
cdacs_view
find . -name 'RuntimeDebugLog.config'
my_rebase 
deliver -graph
my_rebase 
deliver -graph
mc; mist
~/work/scripts/bash/end_my_views.sh 
~/work/scripts/bash/end_my_views.sh 
~/work/scripts/bash/end_my_views.sh 
vncconfig ^
vncconfig &
~/work/scripts/bash/end_my_views.sh 
pwd
cd /ws/yizaq-csi/
ll
ls -lstra
ls -lstra | grep yiza
ls | grep yizaq
ls -lstra | grep yiza | awk -F"/" '{print $1}'
ls | grep yiza | awk -F"/" '{print $1}'
ls | grep yiza | awk -F"/" '{print $1}' | tee /tmp/aaa
for i in `cat /tmp/aaa`; do cleartool lsview $i; done
alias list_COs 
vi ~/.aliases 
chmod +x /users/yizaq/work/scripts/bash/end_my_views.sh
fg
fg
fg
fg
d
fg
q
fg
ct pwv
fg
vnc1024 
vnc1280 
cdacs_view
sha1sum  patches_5_3/5-3-0-40/files/libeda.so.0 
sha1sum  patches_5_3/5-3-0-40/files/liblrpc.so.0.0.0 
sha1sum  patches_5_3/5-3-0-40/files/libcapi.so.0.0.0 
export CENT_4_5_350="/ws/yizaq-csi/temp/centrify/"
echo $CENT_4_5_350
ct lsact
ct lsact -cact
ct setact deliver.yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.20120402.174703
ct mkact yizaq_complete_4_5_350_deliver_binaries
for c in ${AD_CONFS[@]} ; do find $CENT_4_5_350 -name $c | sed -e '1p' ; done
for c in ${AD_CONFS[@]} ; do find $CENT_4_5_350 -name $c | sed -e '1p' ; done
cd runtime/prebuilt/lnx26/etc/
for c in ${AD_CONFS[@]} ; do if diff -q `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else tkdiff `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c; fi ; done
for c in ${AD_CONFS[@]} ; do if diff -q `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else tkdiff `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c; fi ; done
AD_CONFS=`ls`
for c in ${AD_CONFS[@]} ; do if diff -q `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else tkdiff `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c; fi ; done
for c in ${AD_CONFS[@]} ; do if diff -q `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else echo $c is different; fi ; done
cd ../include/adagent/
 AD_HS=`\ls *.h`
for c in ${AD_HS[@]} ; do if diff -q `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else echo $c differ; fi ; done
ls_dir 
cd ../adagent_capi/
for c in ${AD_HS[@]} ; do if diff -q `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else echo $c differ; fi ; done
cd ../../bin/
AD_CLI_BINS=(adfinddomain     adkeytab     adsmb              fix_pam_rsh.sh  ldapdelete  adfixid          adleave      adupdate           ldapmodify  adcache           adflush          adobfuscate  ldapmodrdn  adcheck           adgpupdate       adpasswd     ldapsearch  adclient          adid             adquery      cdcexec            adinfo           adreload     cdcwatch           addns             adinfo_extra.sh  adrmlocal    ldapadd         adenv             adjoin           adsetgroups  ldapcompare     adlicense)
 for c in ${AD_CLI_BINS[@]} ; do if diff -q `find $CENT_4_5_349 -type f -name $c ` $c >/dev/null ; then echo $c same; else echo $c differ; fi ; done
cd ../../../../patches_5_3/5-3-0-40/files/
 for c in ${AD_CLI_BINS[@]} ; do if diff -q `find $CENT_4_5_349 -type f -name $c ` $c >/dev/null ; then echo $c same; else echo $c differ; fi ; done
strings * | grep '4.5.0'
cd -
cd ../lib/
ls -lrt
ct ls liblrpc*
vi ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash
ls
 ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash
ct lsact
ct lsact -cact
co .
vi ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash
ls
 ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash
cd -
cd -
cd ../../../../patches_5_3/5-3-0-40/files/
diff -r /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/
diff -r . /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/
cdacs_view
list_COs 
ct lsco -all -me | grep P3.P2.P1.FCS_5_3.int.acs5_0 | awk '{print }' | sed -e 's_"__g'
cd patches_5_3/5-3-0-40/
ls files/
ls *.tar
ls
cd ..
./patch.sh  pack 5-3-0-40-3 5-3-0-40/
cd 5-3-0-40/
ftp cd-acs-ftp
ls
cd files/
ls
BINS=(adcache adcheck adclient addebug addns adenv adfinddomain adfixid adflush adgpupdate adid adinfo adinfo_extra.sh adinfo_extra.sh adjoin adkeytab adleave adlicense adpasswd adquery adreload adrmlocal adsetgroups adsmb adupdate cdcexec cdcwatch centrifydc centrifydc_init_d centrifydc_init_d fix_pam_rsh.sh ldapadd ldapcompare ldapdelete ldapmodify ldapmodrdn ldapsearch nscdrestart.sh upgradeconf)
echo $BINS
echo ${BINS[@]}
for f in ${BINS[@]}; do sha1sum $f; done
ls -l
ct ls -l
ct ls *
ls -l
ls -l  | grep '-r--r--r--'
ls -l  >  grep '-r--r--r--'
ls -l  
ls -l  | grep '-r--r--r--'
ls -l  | grep '\-r\-\-r\-\-r\-\-'
ls -l  | grep '\-r\-\-r\-\-r\-\-' | grep -v lib 
ls -l  | grep '\-r\-\-r\-\-r\-\-' | grep -v lib  | grep -v acs
ls -l  | grep '\-r\-\-r\-\-r\-\-' | grep -v lib  | grep -v acs | grep -v '.'
ls -l  | grep '\-r\-\-r\-\-r\-\-' | grep -v lib  | grep -v acs | grep -v '\.'
for file in `ls -l  | grep '\-r\-\-r\-\-r\-\-' | grep -v lib  | grep -v acs | grep -v '\.'` ; do echo file $file; done
ls -l  | grep '\-r\-\-r\-\-r\-\-' | grep -v lib 
ls -l  | grep '\-r\-\-r\-\-r\-\-' | grep -v lib  | grep -v acs | grep -v '\.'
ls -l  | grep '\-r\-\-r\-\-r\-\-' | grep -v lib  | grep -v acs | grep -v '\.' | awk '{print $NF}'
for file in `ls -l  | grep '\-r\-\-r\-\-r\-\-' | grep -v lib  | grep -v acs | grep -v '\.' | awk '{print $NF}'` ; do echo file $file; done
for file in `ls -l  | grep '\-r\-\-r\-\-r\-\-' | grep -v lib  | grep -v acs | grep -v '\.' | awk '{print $NF}'` ; do echo adding x to file $file; done
for file in `ls -l  | grep '\-r\-\-r\-\-r\-\-' | grep -v lib  | grep -v acs | grep -v '\.' | awk '{print $NF}'` ; do echo adding x to file $file; ct protect -chmod +x $file ; done
ls -l  | grep '\-r\-\-r\-\-r\-\-' | grep -v lib  | grep -v acs | grep -v '\.'
ls -l 
ls
cd ..
ls
rm *.tar.*
rm *.tar
cd ..
./patch.sh  pack 5-3-0-40-3 5-3-0-40/
ftp cd-acs-ftp
cd 5-3-0-40/
ftp cd-acs-ftp
ct lsact -cact
co .
hist iles2replace
cdacs_view
my_rebase 
cd patches_5_3/5-3-0-40/
diff -r . /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/
cd files/
diff -r . /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/
ct ls libgcc*
ct ls libgcc_s-3.4.6-20060404.so.1
cd ..
ct lsvtree -g files/
diff -r . /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/
cd -
diff -r . /view/yizaq__yizaq.P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/
ls -ltr
sha1sum libstdc++.so.6.0.3
sha1sum libgcc_s-3.4.6-20060404.so.1 
cd ..
rm *tar*
cd ..
cd -
cd -
./patch.sh  pack 5-3-0-40-3 5-3-0-40/
ls -l 5-3-0-40/files/
cd 5-3-0-40/
ftp cd-acs-ftp
ls *.jar files/
ct ls files/acs-internalcli-5.3.0.40.B.839.jar 
ct lsvtree  files/acs-internalcli-5.3.0.40.B.839.jar 
ct lsvtree  -g files/acs-internalcli-5.3.0.40.B.839.jar 
cdacs_view
list_COs 
ct lsco -all -me | grep yizaq.P3.P2.P1.FCS_5_3.int.acs5_0 | awk '{print }' | sed -e 's_"__g'
vncconfig &
~/work/scripts/centrify/update_5_3_p_1_files2replace
sha1sum  patches_5_3/5-3-0-40/files/libeda.so.0 
sha1sum  patches_5_3/5-3-0-40/files/liblrpc.so.0.0.0 
sha1sum  patches_5_3/5-3-0-40/files/libcapi.so.0.0.0 
ls -l patches_5_3/5-3-0-40/files/libcapi.so.0.0.0 
ct ls patches_5_3/5-3-0-40/files/libcapi.so.0.0.0
ls -l patches_5_3/5-3-0-40/files/liblrpc.so.0.0.0 
ct ls patches_5_3/5-3-0-40/files/liblrpc.so.0.0.0
ci_all.sh 
my
my_rebase 
deliver -graph
ct lsact
deliver -complete
cd patches_5_3/5-3-0-40/files/
ls
for file in `ls -l  | grep '\-r\-\-r\-\-r\-\-| grep -v lib  | grep -v acs | grep -v '\.' | awk '{print $NF}'` ; do echo adding x to file $file; ct protect -chmod +x $file ; done
for file in `ls -l  | grep '\-r\-\-r\-\-r\-\-| grep -v lib  | grep -v acs | grep -v '\.' | awk '{print $NF}'` ; do echo adding x to file $file;  done 
ls -l
for file in `ls -l  | grep '\-r\-\-r\-\-r\-\-| grep -v lib  | grep -v acs | grep -v '\.' | awk '{print $NF}'` ; do echo adding x to file $file;  done 
ls -l  | grep '\-r\-\-r\-\-r\-\-| grep -v lib  | grep -v acs | grep -v '\.' | awk '{print $NF}'
ls -l  | grep '\-r\-\-r\-\-r\-\-| grep -v lib  | grep -v acs
for file in `ls -l  | grep '\-r\-\-r\-\-r\-\-'| grep -v lib  | grep -v acs | grep -v '\.' | awk '{print $NF}'` ; do echo adding x to file $file;  done 
ls -l  | grep '\-r\-\-r\-\-r\-\-'| grep -v lib  | grep -v acs | grep -v '\.' | awk '{print $NF}'
ls -l  | grep '\-r\-\-r\-\-r\-\-'| grep -v lib  | grep -v acs | grep -v '\.' 
ls -l  | grep '\-r\-\-r\-\-r\-\-'| grep -v lib  | grep -v acs
ls -l  | grep '\-r\-\-r\-\-r\-\-'
los -l
ls -l
cdacs_view
resume_edit ~/work/vim_sessions/ad_files 
ct lsact
ct setact yizaq_INTEGRATE_CENTRIFY_4_5_0_350
ls runtime/prebuilt/lnx26/lib/adagent/libgcc*
ls runtime/prebuilt/lnx26/lib/adagent/libstd*
find runtime/prebuilt/lnx26/lib/ -name 'libgcc*'
my_rebase
my_rebase
rebase -complete
hist update_
~/work/scripts/centrify/update_5_3_p_1_files2replace
cd patches_5_3/5-3-0-40/files/
ls -lrt
rm libgcc_s-3.4.6-20060404.so.1
rm libstdc++.so.6.0.3
co .
ct lsact
ct setact yizaq_INTEGRATE_CENTRIFY_4_5_0_350
co .
ls -lrt
~/work/scripts/centrify/update_5_3_p_1_files2replace
cdacs_view
deliver -graph
ci_all.sh 
deliver -graph
svs
svs
xts_small 
reboot 
ct lsstream
exit
vnc1280 
vnc1024 
cdacs_view
ks
ls
cd ~/work/scripts/centrify/
ls -ltr
cp update_5_3_p_1_files2replace  update_5_3_p_3_files2replace 
vncconfig &
vi &
jobs
kill %1
vi update_5_3_p_3_files2replace 
reboot
hist mks
svs
mkstream -instream P3.P2.P1.FCS_5_3.int.acs5_0 yizaq2
which -instream
which mkstream
ls -ltr /auto/cwtools
pwd
pwd
mount
mount | grep cwtool
mount | grep cwtool
ls -ltr /auto/cwtools
mount | grep cwtool
xts_small 
vncconfig &
hist end
~/work/scripts/bash/end_my_views.sh 
svs
hist vi
chmod +x /users/yizaq/work/scripts/bash/end_my_views.sh
vi /users/yizaq/work/scripts/bash/end_my_views.sh
ls
vnc1024 
vnc1280 
vncconfig &
sudo cp /etc/resolv_cisco_IT.conf  /etc/resolv.conf 
cat /etc/resolv.conf
reboot
mkstream -instream P3.P2.P1.FCS_5_3.int.acs5_0 yizaq2
ls -ltr /auto/cwtools
cdacs_view
exit
cdacs_view
mc
exit
cdacs_view
resume_edit ~/work/vim_sessions/cars_files 
cd install/
ls
\ls
vi pre-install.sh 
ls
vi post-install.sh 
exit
cdacs_view
mc
exit
ls
cdacs_view
ct mkact yizaq_INTEGRATE_CENTRIFY_4_5_0_351
diff -r patches_5_3/5-3-0-40/files/ /view/yizaq__P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/
diff -r patches_5_3/5-3-0-40/files/ /view/yizaq__P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/
AD_CONFS=`ls runtime/prebuilt/lnx26/etc/`
echo $AD_CONFS 
for c in ${AD_CONFS[@]} ; do find $CENT_4_5_350 -name $c | sed -e '1p' ; done
export CENT_4_5_351="/ws/yizaq-csi/temp/centrify/"
for c in ${AD_CONFS[@]} ; do find $CENT_4_5_350 -name $c | sed -e '1p' ; done
cd runtime/prebuilt/lnx26/etc/
for c in ${AD_CONFS[@]} ; do if diff -q `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else tkdiff `find $CENT_4_5_350 -name $c | sed -ne '1p' ` $c; fi ; done
for c in `ls` ; do ifag yizaq__P2.P1.FCS_5_3.int.acs5_0.lx    
vi ~/.aliases 
ls
ct pwv
exit
xts_small 
vnc1024 
vnc1280 
cdacs_view
resume_edit ~/work/vim_sessions/cars_files 
mc; mist
my_rebase
my_rebase
cpwv
ct wpv
ct pwv
ct lsstream
id
syncme
alias my_rebase
rebase -gmerge -mkbl
which perl
ls -ltra /usr/local/bin/perl 
ls -ltra /usr/cisco/bin/perl
ls -ltra /usr/cisco 
ls -ltra /usr/cisco/bin
cdacs_view
find . -type f -iname '*template*'
find . -type f -iname '*template*' | xargs grep -s MaxBackupIndex
find . -type f -iname '*template*' | xargs grep -is MaxBackupIndex
find . -type f  | xargs grep -is MaxBackupIndex
cd mgmt/
find . -type f  | xargs grep -is MaxBackupIndex
cd ..
find . -type f  | xargs grep -is 'MaxBackupIndex=10'
cd mgmt/
find . -type f  | xargs grep -is 'MaxBackupIndex=10'
find . -type f  | xargs grep -s 'MaxBackupIndex=10'
find . -type f  | xargs grep -s 'MaxBackupIndex\=10'
find . -type f  | xargs grep -s 'MaxBackupIndex='
find . -type f  | xargs grep -s 'MaxBackupIndex=' | grep 10
ct lsact
ct setact yizaq_CSCty31541
list_COs 
cd ..
ct lsco -all -me | grep yizaq_5_4.int.acs5_0 | awk '{print }' | sed -e 's_"__g' 
exit
cdacs_view
mc;
gen_src_db 
syncme
mc; mist
export CENT_4_5_351="/ws/yizaq-csi/temp/centrify/"
echo $CENT_4_5_351
cd runtime/prebuilt/lnx26/bin/
 AD_CLI_BINS=(adfinddomain     adkeytab     adsmb              fix_pam_rsh.sh  ldapdelete  adfixid          adleave      adupdate           ldapmodify  adcache           adflush          adobfuscate  ldapmodrdn  adcheck           adgpupdate       adpasswd     ldapsearch  adclient          adid             adquery      cdcexec            adinfo           adreload     cdcwatch           addns             adinfo_extra.sh  adrmlocal    ldapadd         adenv             adjoin           adsetgroups  ldapcompare     adlicense) 
echo ${AD_CLI_BINS[@]} 
for c in ${AD_CLI_BINS[@]} ; do if diff -q `find $CENT_4_5_351 -type f -name $c ` $c >/dev/null ; then echo $c same; else echo $c differ; fi ; done
 for c in ${AD_CLI_BINS[@]} ; do if diff -q `find $CENT_4_5_351 -type f -name $c ` $c >/dev/null ; then echo $c same; else echo $c differ; co $c; cp `find $CENT_4_5_351 -type f -name $c ` $c;  sha1sum `find $CENT_4_5_351 -type f -name $c ` $c ; fi ; done
for c in ${AD_CLI_BINS[@]} ; do if diff -q `find $CENT_4_5_351 -type f -name $c ` $c >/dev/null ; then echo $c same; else echo $c differ; fi ; done


ls
vi ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash
ls
cd ../lib/
~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash
vi ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash
ls
diff -r /view/yizaq__yizaq_5_4_centrify.int.acs5_0.lx/vob/nm_acs/acs/runtime/prebuilt/lnx26/lib .
cd ../bin/
diff -r /view/yizaq__yizaq_5_4_centrify.int.acs5_0.lx/vob/nm_acs/acs/runtime/prebuilt/lnx26/bin .
cd ../..
cd ../..
find . -name '*.contrib*' | xargs rm -f
diff -r /view/yizaq__yizaq_5_4_centrify.int.acs5_0.lx/vob/nm_acs/acs/ .
find . -name '*.out' | xargs rm -f
diff -r /view/yizaq__yizaq_5_4_centrify.int.acs5_0.lx/vob/nm_acs/acs/ .
mc; mist
ls
cdacs_view
mc; mist
find . -type f  | xargs grep -s 'MaxBackupIndex=10' 
grep MaxBackupIndex mgmt/common/target/classes/templateForCli/ManagementDebugLog.config
grep MaxBackupIndex mgmt/./common/target/classes/ManagementDebugLog.config 
reboot
code_review_info 
cdacs_view

deliver -complete
cat ~/.m2/settings.xml 
cd $WS
cd maven-repo/
ls
cd view/
ls
cd yizaq1__int.acs5_0.lx/
ls
rm -fr *
cdacs_view
cdacs_view
my_rebase 
mc; mist
ct lsact
ct mkact yizaq_INTEGRATE_CENTRIFY_4_5_0_351_to_5_4
export CENT_4_5_351="/ws/yizaq-csi/temp/centrify/"
echo $CENT_4_5_351
AD_CONFS=`ls runtime/prebuilt/lnx26/etc/`
echo $AD_CONFS 
cd runtime/prebuilt/lnx26/etc/
for c in ${AD_CONFS[@]} ; do if diff -q `find $CENT_4_5_351 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else tkdiff `find $CENT_4_5_351 -name $c | sed -ne '1p' ` $c; fi ; done
ctlsvtree -g centrifydc.conf 
ct lsvtree -g centrifydc.conf 
ct_diff_t centrifydc.conf
cd ../include/adagent/
 AD_HS=`\ls *.h`
for c in ${AD_HS[@]} ; do if diff -q `find $CENT_4_5_351 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else echo $c differ; fi ; done
for c in ${AD_HS[@]} ; do if diff -q `find $CENT_4_5_351 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else echo $c differ; co $c; cp `find $CENT_4_5_351 -name $c | sed -ne '1p' ` $c; fi ; done
cd ../adagent_capi/
for c in ${AD_HS[@]} ; do if diff -q `find $CENT_4_5_351 -name $c | sed -ne '1p' ` $c >/dev/null ; then echo $c same; else echo $c differ; co $c; cp `find $CENT_4_5_351 -name $c | sed -ne '1p' ` $c; fi ; done
cd ../../bin/
 AD_CLI_BINS=(adfinddomain     adkeytab     adsmb              fix_pam_rsh.sh  ldapdelete  adfixid          adleave      adupdate           ldapmodify  adcache           adflush          adobfuscate  ldapmodrdn  adcheck           adgpupdate       adpasswd     ldapsearch  adclient          adid             adquery      cdcexec            adinfo           adreload     cdcwatch           addns             adinfo_extra.sh  adrmlocal    ldapadd         adenv             adjoin           adsetgroups  ldapcompare     adlicense) 
echo ${AD_CLI_BINS[@]} 
for c in ${AD_CLI_BINS[@]} ; do sha1sum `find $CENT_4_5_351 -type f -name $c`   ; done
 $ for c in ${AD_CLI_BINS[@]} ; do if diff -q `find $CENT_4_5_351 -type f -name $c ` $c >/dev/null ; then echo $c same; else echo $c differ; fi ; done
 for c in ${AD_CLI_BINS[@]} ; do if diff -q `find $CENT_4_5_351 -type f -name $c ` $c >/dev/null ; then echo $c same; else echo $c differ; fi ; done
 for c in ${AD_CLI_BINS[@]} ; do if diff -q `find $CENT_4_5_351 -type f -name $c ` $c >/dev/null ; then echo $c same; else echo $c differ; co $c; cp `find $CENT_4_5_351 -type f -name $c ` $c;  sha1sum `find $CENT_4_5_351 -type f -name $c ` $c ; fi ; done
strings * | grep '4.5.0' 
vi ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash
ls
 cd ../lib/
ls -l libcapi* liblrpc*
vi ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash
ls
 ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash 
ct unco .
ct lsvtree -g .
vi ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash
ls
 ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash 
sha1sum libcapi.so.0.4.5.0-351
cp libcapi.so.0.4.5.0-351 ~/temp/
co ~/temp/
co libcapi.so.0.4.5.0-351
ct ls
ct ls | grep eclips
mkdir /tmp/eclipsed
ls -ltr *-351
cp -r *-351 /tmp/eclipsed/
rm *-351
ct ls 
ct ls *-351
cp /tmp/eclipsed/libcapi.so.0.4.5.0-351  libcapi.so.0.4.5.0-351 
co libcapi.so.0.4.5.0-351
cp /tmp/eclipsed/libcapi.so.0.4.5.0-351  libcapi.so.0.4.5.0-351 
sha1sum libcapi.so.0.4.5.0-351
co liblrpc.so.0.4.5.0-351 
cp /tmp/eclipsed/liblrpc.so.0.4.5.0-351  liblrpc.so.0.4.5.0-351 
sha1sum liblrpc.so.0.4.5.0-351
cdacs_view
ci_all.sh 
my_rebase
mc; mist
hist mks
mkstream -instream int.acs5_0 yizaq2
hist eview
createview -stream int.acs5_0
vi ~/.aliases 
;s
. ~/.aliases 
svs
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             cdacs_view
ct lsact
date
ct lsact
syncme
cd patches_5_3/
ls
hist pack
rm -f 5-3-0-40/*.tar*
rm -f 5-3-0-40/*.tar
./patch.sh  pack 5-3-0-40-3 5-3-0-40/
cd 5-3-0-40/
ftp cd-acs-ftp
hist update_
vi ~/work/scripts/centrify/update_5_3_p_3_files2replace
ls
ls
md5sum 5-3-0-40-3.tar.gpg 
hist update_
vi ~/work/scripts/centrify/update_5_3_p_3_files2replace
tail ~/work/scripts/centrify/update_5_3_p_3_files2replace
ls
cdacs_view
cd patches_5_3/5-3-0-40/files/
ct ls CLI.war
ct unco CLI.war
ct unco acs-db-5.3.0.40.B.839.jar 
ct unco acs-bl-framework-5.3.0.40.B.839.jar
~/work/scripts/centrify/update_5_3_p_3_files2replace >& ~/stam
cdacs_view
ci_all.sh 
cd patches_5_3/5-3-0-40/files/
diff -r patches_5_3/5-3-0-40/files/ /view/yizaq__P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/
cd ../..
diff -r patches_5_3/5-3-0-40/files/ /view/yizaq__P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/
cd ..
diff -r patches_5_3/5-3-0-40/files/ /view/yizaq__P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/
diff -r patches_5_3/5-3-0-40/files/ /view/yizaq__P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/ > ~/stam
deliver -graph
diff -r patches_5_3/5-3-0-40/files/ /view/yizaq__P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/ > ~/stam
vi ~/stam
ls
diff -r patches_5_3/5-3-0-40/files/ /view/yizaq__P3.P2.P1.FCS_5_3.int.acs5_0.lx/vob/nm_acs/acs/patches_5_3/5-3-0-40/files/ 
mkstream -instream P3.P2.P1.FCS_5_3.int.acs5_0 yizaq2
cat /etc/readahead.early.files 
cat /etc/resolv.conf 
mkstream -instream P3.P2.P1.FCS_5_3.int.acs5_0 yizaq2
cd $WS
pwd
ls
cd workspace/
ls
cd ..
cd ~
pwd
#Cisco IT DNS
nameserver 144.254.71.184
nameserver 64.103.101.184
nameserver 144.254.10.123
nameserver 64.102.6.247
[yizaq@yizaq-lnx:Sun Apr 08:~]$ mkstream -instream P3.P2.P1.FCS_5_3.int.acs5_0 yizaq2
Preparing for mkstream
Identifying component 11 out of 11
Creating baselines on stream:P3.P2.P1.FCS_5_3.int.acs5_0@/vob/nmtgre_proj
Syncing /vob/nm_acs
Syncing /vob/nmtgre_proj
Processing 1 R/O baselines
Identifying the latest baselines
Processing baseline 11 out of 11
Creating the stream from following baseline(s)
baseline:hudson_co_22-sep-11_00_00_44.274@/vob/nmtgre_proj
baseline:ibf_nm_acs_BASE_ibf.nm_acs.acs5_0@/vob/nmtgre_proj
baseline:RE_HD09455794.acs.nm_acs.9817@/vob/nmtgre_proj
baseline:rebase.acs5_0.20110809_142432.5283@/vob/nmtgre_proj
baseline:rebase.acs5_0.20100215_151150.4263@/vob/nmtgre_proj
baseline:rebase.acs5_0.20091004_164801.3309@/vob/nmtgre_proj
baseline:hudson_co_11-jul-11_00_01_06.6303@/vob/nmtgre_proj
baseline:mkstream.acs5_0.20120408_151337.7731@/vob/nmtgre_proj
baseline:RE_HD09455794.acs.nm_acs.2487@/vob/nmtgre_proj
baseline:BUILD.acs5_0.20091216_113008.6559@/vob/nmtgre_proj
baseline:RE_CASE_HD7791367.acs5_0.20080317_210350@/vob/nmtgre_proj
Moving_to_PMBU_Nexus_sj-pmbu-maven01.3rdparty_tools.20101219_094958@/vob/nm_admin_proj
Updated policies on stream "yizaq2.P3.P2.P1.FCS_5_3.int.acs5_0".
 Created stream "yizaq2.P3.P2.P1.FCS_5_3.int.acs5_0".
[yizaq@yizaq-lnx:Sun Apr 08:~]$ cd $WS
cd $WS
df .
echo $WS
quotas
mount | grep yizaq
cd /ws/yizaq-csi 
du_1st_lvl
hist eview
createview -stream yizaq2.P3.P2.P1.FCS_5_3.int.acs5_0
svs
export CENT_4_5_351="/ws/yizaq-csi/temp/centrify/"
echo $CENT_4_5_351
cd $CENT_4_5_351 
ls
rm -fr *
cp /ws/yizaq-csi/work/Acs/Centrify/4_5/351/* .
ls
cp /ws/yizaq-csi/work/Acs/Centrify/4_5/350
for f in `ls` ; do extract_rpm $f . ; done
ct pwv
. ~/.aliases 
svs
cd $WS

vi ~/work/centrify/scripts/merge_4_5/relink_lib_snippet.bash
tail -f ~/stam
tail -f ~/stam
ls -l ~/stam
ls
tail -f ~/stam
tail -f ~/stam
ct pwv
svs
ls
svs
ct lsact
cdacs_view
ct lsact
exit
ct lsact
exit
deliver -status
deliver -cancel
deliver -exhelp
deliver -gmerge -to yizaq__int.acs5_0.lx
deliver -cancel
deliver -gmerge -to yizaq__int.acs5_0.lx
deliver -complete
hist find
grepa find
grepa search
search_in_files ADE | grep rotate
