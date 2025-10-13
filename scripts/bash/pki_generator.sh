#!/bin/bash

############################################################################################
#           Following bash script is used to generate full package of certificates required #
#           for stress testing under protocols that are required PKI infrastructure        #
############################################################################################

function help ()
 {
  echo "Usage is: \"$0 [ Options ] \" "
	echo " Options are : "
	echo "   -Cm, --CA_mode [Options] allowed values are \"noCA\",\"CA\",\"subCA\""
	echo "   -CAname , --CA_name [Options] allowed values [any alphanumeric strings]"
   echo "   -SVname , --Server_name [Options] allowed values [any alphanumeric strings]"
	echo "   -Noc, --number_of_certificates [Options] allowerd values are [0-99999...]*"
	echo "   -Norc, --number_of_revoked_certificates [Options] allowed values are [0-99999...]"
	echo "   -up, --username_pattern [Options] allowed values [any alphanumeric strings]"
	echo "   -mp, --machinename_pattern [Options] allowed values [any alphanumeric strings]"
	echo "   -dp, --domainame_pattern [Options] allowed values [any alphanumeric strings]"
	echo "   -CAexp, --CA_experation [Options] allowed values are [0-99999...]"
   echo "   -policyCaexp, --policyCa_experation [Options] allowed values are [0-99999...]"
   echo "   -issuingCaexp, --issuingCa_experation [Options] allowed values are [0-99999...]"
   echo "   -SERexp, --Server_experation [Options] allowed values are [0-99999...]"
   echo "   -CLTexp, --Client_experation [Options] allowed values are [0-99999...]"
   echo "   -CLRexp , --CRL_experation [Options] allowed values are [0-99999...]"
   echo "   -CLTFexp, --Client_fast_experation [Options] allowed values are [0-99999...]"
   echo "   -hash, --hash_type [Options] allowed values are [sha256,sha384,sha512,sha1, md5]"
   echo "   -keysz, --key_size [Options] allowed values are [512,1024,2048,4096,8192]"
   echo "   -bcpt , --basic_constrains_path_length [Options] allowed values are [0-max]"   
   echo "   -cn_max_size , --common_name_max_size [Options] allowed values are [0-999]"
   echo "   -em_max_size , --email_max_size [Options] allowed values are [0-999]"
   echo "   -san , --SAN_complexity [Options] allowed values are [0-3]"  
   echo "   -RndSn, --Random_Serial_Number - creates certificate with random serial numbers " 
   echo "   -ncnt , --name_constrains - adds name constrains to CA certificates"

	echo "-------------------------------------------"
	echo "Examples of configuration:"
	echo " $0 -Cm CA -Noc 1000 -Norc 5 -up user -mp machine -dp cisco.com  -CAexp 365 -policyCaexp 365 -issuingCaexp 365 -SERexp 365 -CLTexp 365 -hash md5 -keysz 1024 -RndSn"
	echo "   - will create :"
	echo "        * 1000 user[0-999] certificates where CN will have following format:"
	echo "        * cn=user0,cn=user1... and SAN user0@cisco.com,user1@cisco.com..."
	echo "        * 1000 machine[0-999] certificates where CN will have following format:"
	echo "        * cn=machine0.cisco.com,cn=machine1... and SAN DNS: user0.cisco.com..."
	echo "        * one server certificate+private key"
	echo "        * one CA certificate+private key"
	echo "        * 5 revoked certificate"
	echo "        * every certificate will be valid for 365 days"
   echo "        * signature algorithm to be used is MD5"
   echo "        * key size will be 1024 bit"
	echo " $0 -Cm noCA -Noc 100 user"
   echo "   - will create :"
	echo "        * scripts to insert users in CSDB and Active Directory only."
	echo "        * No certificates will be created"
	echo "Note: "
	echo "Default password used for all certificates is : 1234"
	echo "Root CA , Policy Ca and Issuing CA certificate are being generated regardless of switch settings"
        echo "When generating 1 client certificate, no index value will be added to the pattern"
	echo "--------------------------------------------"
	echo "At the end following hierarchy will be created:"
	echo "sslcert\\"
	echo "        acs <- Contains scripts to insert users in CSDB and Active Directory"
	echo "        ca  <- Contains CA certificate (install it on ACS and on client side)"
	echo "        policyCa <- Contains policyCa certificate"
   echo "        issuingCa <- Contains issuingCa certificate"
	echo "        certs <- Contains pem format certificates"
	echo "        clients <- Contains clients\user certificates in *.pvk, *.pem"
	echo "        clients_der <- Contains certificates in *.der format for ldap usage"
	echo "        clients_p12 <- Contains certificates in *.pfx format for windows supplicant installation"
	echo "        crl <- Contains list of revoked certificates"
	echo "        server <- Server side certificare"
	echo "--------------------------------------------"
	echo "certificates.tar.gz is being generated to hold all the created data as package"
}

# Shows version of the application

function version ()
  {
  	  echo "+--------------------------+"
  	  echo "| PKI Generator ver 1.1.7  +--+"
	  echo "| by Alexander Atlas       | #|"
	  echo "| for Cisco Systems        | #|"
	  echo "+--------------------------+ #|"
     echo "  |###########################|" 
	  echo "  +---------------------------+"
  }

# Initial difinition part


i=0
USER_CSR_CONFIG="user-cert-req.conf"
MACHINE_CSR_CONFIG="machine-cert-req.conf"
passwd=1234 # sets CA password
noCA=0
upattern="" # empty username pattern
machinen="" # machine name pattern
CAExp=730 # defines number of days CA certificate is valid
policyCaExp=730 # defines number of days policy CA certificate is valid
issuingCaExp=730 # defines number of days issuing CA certificate is valid
ServerExp=365 # defines number of days Server certificate is valid
userExp=60 # defines number of days user certificate is valid
FuserExp=0 # Number of certificates to be fast expired
crlExp=30 # defines number of days till crllist is expired
cfp="CAforACS" # default definition for CA name 
sdn="Server" # default definition for Server name 
chain=0 # do not create chain 
basic_constrains_path_length=-1
name_constrains="No"
key_size=1024 # default key size
hashtype=md5 # default hash type
cn_max_size=64 # default size on CN
em_max_size=64
rndSerial=100001
numofservercert=1 # number of server certificates to be 1 initially.
san_cplx=0 # specified type of SAN to use "0" is none

###################################

version # show version of the tool

if [ $# -eq 0 ]; then # if no agruments supplied then show help
 help
exit
fi

echo "+-General Info-----------------------------------------+"
echo "+--|| Using `openssl version` ||"
echo "Arguments used : " $*

while [ "$1" != "" ]; do
    case "$1" in
        -Cm|--CA_mode)        
           shift
                   case "$1" in
                   noCA) # only create users
                     
                     noCA=1 # No CA is in use
                     
                     if [ $# -lt 3 ]; then # exit if number of arguments is smaller than 5
			  echo " Error -> No enough arguments provided"
			  echo " Error -> Run application without arguments to see help"
		             exit
		      fi
                   ;;
                    CA)   # use CA to sign certificates 
			                 echo "All issuing certificates will be signed by CA"
			     CAcert="ca/cacert.cer"
			      p12CAcert="ca/cacert.cer"
			       CApvk="ca/cakey.pem"
                   ;;
                    
                    # use subCA to sign certificates
                    subCA) echo "All issuing certificates will be signed by subordinate 3rd CA in chain"
 				          CAcert="issuingCa/issuingCa.cer"
				          p12CAcert="issuingCa/issuingCa.cer"
				          CApvk="issuingCa/issuingCa.key"
			             ;;		     
                   *) echo " Error -> No enough arguments provided"
               echo " Error -> Run application without arguments to see help"
		     exit
                   ;; 
                   esac
                 ;;
   
  
        -Ct | --certificate_type ) shift  # what type of certificate to generate
                                   machineuser=$1
                         case "$1" in	
                           mc) echo "Machine Certificate[s] will be created" ;;
	                   uc) echo "User Certificate[s] will be created" ;;
                            *) echo " Error -> No enough arguments provided or worng type of client  certificate"
                                echo " Note -> Run application without arguments to see help"
			         exit ;;
			 esac   
                                ;;

        -Noc | --number_of_certificates) shift
                                         numofucert=$1 # sets number of users certificates to generate
                                         echo "Number of User Cerificates to be generated: " $numofucert
                                ;;
        -Norc | --number_of_revoked_certificates) shift
                                 numofrev=$1 # sets number of revoked certificates to create exclude server certificate
	                    echo "Number of User revoked cerificates to be generated: " $numofrev
                                ;;
        -Nosc | --number_of_server_certificates) shift
                                 numofservercert=$1 # sets number of revoked certificates to create exclude server certificate
	                    echo "Number of server cerificates to be generated: " $numofservercert
                                ;;                        
        -up | --username_pattern) shift
                                upattern=$1 # defines user pattern
                                echo "Subject Name (CN) - username pattern will be : " $upattern
                                ;;
        -mp | --machinename_pattern) shift
                                machinen=$1
                                echo "Subject Name (CN) - machinename pattern will be : " $machinen
                                ;;                        
        -dp | --domainname_pattern) shift
                                domainpatern=$1 # defines user pattern
                                echo "Subject Alternative Name (SAN) - pattern will be : " $domainpatern
                                ;;
        
        -bcpt | --basic_constrains_path_length ) shift
                               basic_constrains_path_length=$1 #define issuing CA path lengh
                               echo "Basic constrains path length for issuingCA will be : " $basic_constrains_path_length
                                ;;
        -ncnt | --name_constrains ) shift
                               name_constrains="yes" #define usage of name constrains
                               echo "Name constrains will be applied to CA and subCA"
                               ;;        
        
        -hash | --hash_type ) shift # defines type of hash to be used for sign certificates
                                 case "$1" in
                                   md2 | MD2) # defines $hashtype hash to be used for sign certificates
                                          hashtype=md2
                                          echo "Signature hash algoritm is : MD4"
                                          ;;                              
                                   md4 | MD4) # defines $hashtype hash to be used for sign certificates
                                          hashtype=md4
                                          echo "Signature hash algoritm is : MD4"
                                          ;;
                                   sha1 | SHA1) # defines $hashtype hash to be used for sign certificates
                                          hashtype=sha1
                                          echo "Signature hash algoritm is : SHA1"
                                          ;;
                                   sha256 | SHA256) # defines $hashtype hash to be used for sign certificates
                                           hashtype=sha256
                                          echo "Signature hash algoritm is : SHA256"
                                           ;;
                                   sha384 | SHA384) # defines $hashtype hash to be used for sign certificates
                                           hashtype=sha384
                                          echo "Signature hash algoritm is : SHA384"
                                           ;;
                                   sha512 | SHA512) # defines $hashtype hash to be used for sign certificates
                                           hashtype=sha512
                                          echo "Signature hash algoritm is : SHA512"
                                           ;;                
                                   *) hashtype=md5
                                          echo "Signature hash algoritm is : md5"
                                           ;;
                                esac
                                ;;
        -cn_max_size | --common_name_max_size) shift
                                         cn_max_size=$1 # sets number of users certificates to generate
                                         echo "Max length of Common Name  allowed: " $cn_max_size
                                ;;
        
        -em_max_size | --email_max_size) shift
                                         em_max_size=$1 # sets number of users certificates to generate
                                         echo "Max length of email address allowed: " $em_max_size
                                ;;

        -keysz | --key_size ) shift  # what size of public key to generate

	 case "$1" in	
		512)  echo "Key size will be : 512 bit" 
		      key_size=512 
		      ;; 
      1024) echo "Key size will be : 1024 bit" 
             key_size=$key_size
                      ;; 
      2048) echo "Key size will be : 2048 bit" 
             key_size=2048 
                  ;;      
	   4096) echo "Key size will be : 4096 bit" 
             key_size=4096 
                   ;;      
		8192)  echo "Key size will be : 8192 bit" 
		       key_size=8192 
					    ;;
		16384)  echo "Key size will be : 16384 bit" 
		        echo "Warning: Generation of certificate having such lalrge key size can take a lot of time !!!"
		        key_size=16384 
					    ;;     			          
         *) echo "Key size will be  : 512 bit" 
		 		 key_size=512
		 			    ;;
			 esac   
                   ;;
                                
        -CAexp | --CA_experation) shift # Root CA expiration time
                                CAExp=$1 
                                ;;                        
        -policyCaexp | --policyCa_experation) 
                                shift
                                policyCaExp=$1
                                ;;
        -issuingCaexp | --issuingCa_experation) 
                                shift
                                issuingCaExp=$1
                                ;;
        -SERexp | --Server_experation) 
                                shift
                                ServerExp=$1
                                ;;                        
        -CLTexp | --Client_experation) shift
                                userExp=$1
                                ;;          
        -CLTFexp | --Client_fast_experation) shift
                                FuserExp=$1
                                echo "Number of fast expired certificates will be : " $FuserExp
                                ;;          
                                                        
        -CLRexp | --CRL_experation) shift
                                crlExp=$1
                                ;;                                                            
        -CAname | --CA_name)   shift 
        	  	        cfp=$1       
                                ;;
        -SVname | --Server_name)   shift 
        	  	        sdn=$1       
                                ;;
        -san | --SAN_complexity)   shift 
        	  	        san_cplx=$1       
                                ;;
        -RndSn | --Random_Serial_Number)  
        			 let rndSerial=$RANDOM%9000+1000       
        			 ;;           
        										
        -h | --help )           help
                                exit
                                ;;

        * )                     echo "---+ ERROR +-----------------------------------------------------------------------" 
                                echo "Unable to parse all arguments successfully, probably incorrect argument : " $1 
                                echo "run \"" $PWD$0 "--help\" to get list of supported arguments"  
                                exit 1
                                ;;

    esac
    shift
done

# arguments verification points

if [ "$numofucert" -lt "$FuserExp" ]; then # if number of user certificate is lesser than number of fast expired certificates, exit
echo "Configuration problems :"
echo " ---> Number of certificates must be greater than number of fast expired certificates"
exit
fi

if [ "$numofucert" -lt "$numofrev" ]; then # if number of user certificate is lesser than number of fast expired certificates, exit
echo "Configuration problems :"
echo " ---> Number of certificates must be greater than number of revoked certificates"
exit
fi
 
echo "+-Expiration Info--------------------------------------+"

 
   echo "Number of days CA certificate is valid: " $CAExp
   echo "Number of days policyCa certificate is valid: " $policyCaExp
   echo "Number of days Server certificate is valid: " $ServerExp
   echo "Number of days User/Machine certificate is valid: " $userExp

read -p "Press any key to start certificate generation or Ctrl-C to abort..."

if [ -d sslcert ]; then # removing old directory if exists
echo "Warning : sslcert directory already exists..."
echo "Would you like to [r]emove directory [m]ove directory or [a]bort execution"

read choice
  
  if [ $choice = 'r' ] || [ $choice = 'R' ]; then 
     echo Removing old Directory...
     rm -rf sslcert
  fi
  
  if [ $choice = 'm' ] || [ $choice = 'M' ]; then 
     echo "Please provide an new name for old directory"     
     read dirname     
     mv -f sslcert $dirname
     echo "Name of old ssldir was changed to $dirname"
  fi
   
  if [ $choice != 'r' ] && [ $choice != 'R' ] && [ $choice != 'm' ] && [ $choice != 'M' ]; then # if incorrect input was entered 
     echo Stopping the execution...
     exit
  fi

fi

echo "-> Creating sslcert directory"
mkdir sslcert
cd sslcert

if [ $noCA -eq 1 ]; then # create only users directory
  echo "-> Creating private directory"
  mkdir acs 
  echo "OFFLINE:" > acs/CSDBUsers.txt
else

echo "-> Creating certs and private directory"
mkdir certs server clients crl ca acs policyCa issuingCa clients_der clients_p12

echo "-> Creating serial file with base serial to be : $rndSerial" 

echo $rndSerial > serial
chmod 777 serial
echo "-> Creating index file"
touch certindex.txt

###### Creating openssl configuration file for root CA

echo "-> Generating CA root configuration file for openssl"

cat > ca.config <<-EOF
#
# OpenSSL configuration file.
#
# Establish working directory.
[ req ]
#default_bits        = $key_size
default_bits        = 2048
default_keyfile     = ca/cakey.pem
default_md          = $hashtype
distinguished_name  = req_distinguished_name
x509_extensions     = rootca_cert
#string_mask         = utf8only
#utf8                = yes
prompt               = no
[ req_distinguished_name ]
countryName            = IL
stateOrProvinceName         = State Or Provice Name
localityName         = Natania
organizationName         = Cisco Systems.
organizationalUnitName         = ISE\, Identity Division
commonName         = $cfp
emailAddress     = $cfp@$domainpatern
[ rootca_cert ]
# Following section describes extensions which are being added to the Root CA
basicConstraints       = critical, CA:true
subjectKeyIdentifier   = hash
keyUsage               = critical, keyCertSign, cRLSign
authorityKeyIdentifier = keyid:always,issuer:always
nsCertType             = sslCA, emailCA, objCA
nsComment              = "Following certificate generated by OpenSSL"
EOF

if [ $name_constrains = "yes" ]; then # add name constrains if required
cat >> ca.config <<-EOF
nameConstraints=permitted;IP:192.168.0.0/255.255.0.0,permitted;DNS:www.example.co.il,permitted;URI:.example.uri.com,excluded;email:.cisco.com,excluded;email:.net,excluded;email:.,excluded;dirName:dir_sect
[dir_sect]
O=Cisco
0.OU=Managment
1.OU=Managment1
2.OU=Managment2
EOF
fi

echo "-> Done..."

### Generating root CA

echo "-> Generating Root CA"
echo "-> Private key password is : $passwd"
openssl req -new -x509  -passout pass:$passwd -keyout ca/cakey.pem -out ca/cacert.cer -days $CAExp  -passin pass:$passwd -config ./ca.config # 2>/dev/null # -subj /DC=org/DC=OpenSSL/DC=users/UID=123456+CN=CAforISE\ Test

cp ca/cacert.cer ca/cacert_dup.cer
openssl x509 -in ca/cacert_dup.cer -inform PEM -out ca/cacert.der -outform DER 2>/dev/null
rm ca/cacert_dup.cer
echo "-> Done..."


######### Configuration openssl configuration file for policyCa certificate request

echo "-> Generating openssl certificate request configuration file for policyCa certificate"

cat > policyCa-cert-req.config <<-EOF
#
# OpenSSL configuration file for policyCa certificate request.
# 
[ req ]
#default_bits         = $key_size
default_bits         = 2048
default_keyfile      = policyCa/policyCa.key
default_md           = $hashtype
distinguished_name   = req_distinguished_name
x509_extensions      = policyCa_req
string_mask          = nombstr
prompt               = no
[ req_distinguished_name ]
countryName         = IL
stateOrProvinceName         = State Or Province Name
localityName         = Natania
organizationName         = Cisco
organizationalUnitName         = ACS Devision
commonName         = policyCa_$cfp
emailAddress     = policyCa_$cfp@$domainpatern
[ policyCa_req ]
basicConstraints        = critical, CA:true
subjectKeyIdentifier    = hash
authorityKeyIdentifier  = keyid, issuer:always
keyUsage                = critical, keyCertSign, cRLSign
EOF

echo "-> Done..."

######### Configuration openssl file for policyCa certificate 

echo "-> Generating openssl certificate configuration file for policyCa certificate"

echo "#" > policyCa.config
echo "# OpenSSL configuration file for policyCa certificate request." >> policyCa.config
echo "#" >> policyCa.config
echo "" >> policyCa.config
echo "[ ca ]" >> policyCa.config
echo "default_ca = CA_default" >> policyCa.config
echo "[ CA_default ]">> policyCa.config
echo "dir            = \.       # Where everything is kept">> policyCa.config
echo "certs          = "\$"dir/certs           # Where the issued certs are kept">> policyCa.config
echo "crl_dir        = "\$"dir/crl             # Where the issued crl are kept">> policyCa.config
echo "database       = "\$"dir/certindex.txt   # database index file.">> policyCa.config
echo "new_certs_dir  = "\$"dir/certs        # default place for new certs.">> policyCa.config
echo "">> policyCa.config
echo "certificate    = "\$"dir/ca/cacert.cer          # The CA certificate">> policyCa.config
echo "serial         = "\$"dir/serial          # The current serial number">> policyCa.config
echo "crl            = "\$"dir/ca.crl          # The current CRL">> policyCa.config
echo "private_key    = "\$"dir/ca/cakey.pem  # The private key">> policyCa.config
echo "">> policyCa.config
echo "RANDFILE       = "\$"dir/private/.rand   # private random number file">> policyCa.config
echo "">> policyCa.config
echo "">> policyCa.config
echo "default_days      = 4383     # how long to certify for">> policyCa.config
echo "default_crl_days  = 30       # how long before next CRL">> policyCa.config
echo "default_md        = $hashtype      # which md to use.">> policyCa.config
echo "Preserve          = no       # keep passed DN ordering">> policyCa.config
echo "">> policyCa.config
echo "x509_extensions   = policyCa_cert">> policyCa.config
echo "copy_extensions   = none">> policyCa.config
echo "policy            = policy_match">> policyCa.config
echo "">> policyCa.config
echo "[ policyCa_cert ]">> policyCa.config
echo "basicConstraints        = critical, CA:true">> policyCa.config
if (( "$basic_constrains_path_length" >= "0" )); then
echo "basicConstraints        = critical, CA:true,pathlen:$basic_constrains_path_length">> policyCa.config
else
echo "basicConstraints        = critical, CA:true">> issuingCa.config
fi
echo "authorityKeyIdentifier  = keyid:always, issuer:always">> policyCa.config
echo "subjectKeyIdentifier    = hash">> policyCa.config
echo "keyUsage                = critical, keyCertSign, cRLSign">> policyCa.config
echo "nsComment               = "Generated using OpenSSL"">> policyCa.config
echo "nsCertType             = sslCA, emailCA, objCA">> policyCa.config
echo "">> policyCa.config
echo "[ policy_match ]">> policyCa.config
echo "countryName             = match">> policyCa.config
echo "stateOrProvinceName     = optional">> policyCa.config
echo "localityName            = optional">> policyCa.config
echo "organizationName        = supplied">> policyCa.config
echo "organizationalUnitName  = optional">> policyCa.config
echo "commonName              = supplied">> policyCa.config
echo "emailAddress            = optional">> policyCa.config
echo "-> Done..." 


### Generating policyCa certificate 
echo "-> Generating policyCa private key ,certificate request and certificate"
echo "Private key password is : $passwd"
openssl req -new -passout pass:$passwd -keyout policyCa/policyCa.key -out policyCa/policyCa.csr -config ./policyCa-cert-req.config 
cat policyCa/policyCa.csr policyCa/policyCa.key > policyCa/policyCa.pem
openssl ca -batch -notext -passin pass:$passwd -out policyCa/policyCa.cer -config ./policyCa.config -days $policyCaExp -infiles policyCa/policyCa.pem
cp policyCa/policyCa.cer policyCa/policyCa_dup.cer
openssl x509 -in policyCa/policyCa_dup.cer -inform PEM -out policyCa/policyCa.der -outform DER 
rm policyCa/policyCa.csr policyCa/policyCa.pem policyCa/policyCa_dup.cer


######### Configuration openssl configuration file for issuingCa certificate request

echo "-> Generating openssl certificate request configuration file for issuingCa certificate"

echo "#" > issuingCa-cert-req.config
echo "# OpenSSL configuration file for issuingCa certificate request." >> issuingCa-cert-req.config
echo "#" >> issuingCa-cert-req.config
echo "" >> issuingCa-cert-req.config
echo "" >> issuingCa-cert-req.config
echo "[ req ]" >> issuingCa-cert-req.config
#echo "default_bits         = $key_size" >> issuingCa-cert-req.config
echo "default_bits         = 2048" >> issuingCa-cert-req.config
echo "default_keyfile      = issuingCa/issuingCa.key" >> issuingCa-cert-req.config
echo "default_md           = $hashtype" >> issuingCa-cert-req.config
echo "distinguished_name   = req_distinguished_name" >> issuingCa-cert-req.config
echo "x509_extensions      = issuingCa_req" >> issuingCa-cert-req.config
echo "string_mask          = nombstr" >> issuingCa-cert-req.config
echo "prompt               = no" >> issuingCa-cert-req.config
echo "" >> issuingCa-cert-req.config
echo "[ req_distinguished_name ]" >> issuingCa-cert-req.config
echo "countryName         = IL" >> issuingCa-cert-req.config
echo "" >> issuingCa-cert-req.config
echo "stateOrProvinceName         = State Or Province Name" >> issuingCa-cert-req.config
echo "" >> issuingCa-cert-req.config
echo "localityName         = Natania" >> issuingCa-cert-req.config
echo "" >> issuingCa-cert-req.config
echo "organizationName         = Cisco" >> issuingCa-cert-req.config
echo "" >> issuingCa-cert-req.config
echo "organizationalUnitName         = ACS Devision" >> issuingCa-cert-req.config
echo "" >> issuingCa-cert-req.config
echo "commonName         = issuingCa_$cfp" >> issuingCa-cert-req.config
echo "" >> issuingCa-cert-req.config
echo "emailAddress     = issuingCa_$cfp@$domainpatern" >> issuingCa-cert-req.config
echo "" >> issuingCa-cert-req.config
echo "[ issuingCa_req ]" >> issuingCa-cert-req.config
echo "basicConstraints        = critical, CA:true" >> issuingCa-cert-req.config
echo "subjectKeyIdentifier    = hash" >> issuingCa-cert-req.config
echo "authorityKeyIdentifier  = keyid, issuer:always" >> issuingCa-cert-req.config
echo "keyUsage                = critical, keyCertSign, cRLSign" >> issuingCa-cert-req.config
echo "-> Done..."

######### Configuration openssl file for issuingCa certificate 

echo "-> Generating openssl certificate configuration file for issuingCa certificate"

echo "#" > issuingCa.config
echo "# OpenSSL configuration file for issuingCa certificate request." >> issuingCa.config
echo "#" >> issuingCa.config
echo "" >> issuingCa.config
echo "[ ca ]" >> issuingCa.config
echo "default_ca = CA_default" >> issuingCa.config
echo "[ CA_default ]">> issuingCa.config
echo "dir            = \.       # Where everything is kept">> issuingCa.config
echo "certs          = "\$"dir/certs           # Where the issued certs are kept">> issuingCa.config
echo "crl_dir        = "\$"dir/crl             # Where the issued crl are kept">> issuingCa.config
echo "database       = "\$"dir/certindex.txt   # database index file.">> issuingCa.config
echo "new_certs_dir  = "\$"dir/certs        # default place for new certs.">> issuingCa.config
echo "">> issuingCa.config
echo "certificate    = "\$"dir/policyCa/policyCa.cer          # The CA certificate">> issuingCa.config
echo "serial         = "\$"dir/serial          # The current serial number">> issuingCa.config
echo "crl            = "\$"dir/ca.crl          # The current CRL">> issuingCa.config
echo "private_key    = "\$"dir/policyCa/policyCa.key  # The private key">> issuingCa.config
echo "">> issuingCa.config
echo "RANDFILE       = "\$"dir/private/.rand   # private random number file">> issuingCa.config
echo "">> issuingCa.config
echo "">> issuingCa.config
echo "default_days      = 4383     # how long to certify for">> issuingCa.config
echo "default_crl_days  = 30       # how long before next CRL">> issuingCa.config
echo "default_md        = $hashtype      # which md to use.">> issuingCa.config
#echo "default_md        = sha1      # which md to use.">> issuingCa.config
echo "Preserve          = no       # keep passed DN ordering">> issuingCa.config
echo "">> issuingCa.config
echo "x509_extensions   = issuingCa_cert">> issuingCa.config
echo "copy_extensions   = none">> issuingCa.config
echo "policy            = policy_match">> issuingCa.config
echo "">> issuingCa.config
echo "[ issuingCa_cert ]">> issuingCa.config

if (( "$basic_constrains_path_length" >= "0" )); then
echo "basicConstraints        = critical, CA:true,pathlen:$basic_constrains_path_length">> issuingCa.config
else
echo "basicConstraints        = critical, CA:true">> issuingCa.config
fi

echo "authorityKeyIdentifier  = keyid:always, issuer:always">> issuingCa.config
echo "subjectKeyIdentifier    = hash">> issuingCa.config
echo "keyUsage                = critical, keyCertSign, cRLSign">> issuingCa.config
echo "nsComment               = "Generated using OpenSSL"">> issuingCa.config
echo "nsCertType             = sslCA, emailCA, objCA">> issuingCa.config
echo "">> issuingCa.config
echo "[ policy_match ]">> issuingCa.config
echo "countryName             = match">> issuingCa.config
echo "stateOrProvinceName     = optional">> issuingCa.config
echo "localityName            = optional">> issuingCa.config
echo "organizationName        = supplied">> issuingCa.config
echo "organizationalUnitName  = optional">> issuingCa.config
echo "commonName              = supplied">> issuingCa.config
echo "emailAddress            = optional">> issuingCa.config
echo "-> Done..." 


### Generating issuingCa certificate 
echo "-> Generating issuingCa private key ,certificate request and certificate"
echo "Private key password is : $passwd"
openssl req -new -passout pass:$passwd -keyout issuingCa/issuingCa.key -out issuingCa/issuingCa.csr -config ./issuingCa-cert-req.config 
cat issuingCa/issuingCa.csr issuingCa/issuingCa.key > issuingCa/issuingCa.pem

openssl ca -batch -notext -passin pass:$passwd -out issuingCa/issuingCa.cer -config ./issuingCa.config -days $issuingCaExp -infiles issuingCa/issuingCa.pem
cp issuingCa/issuingCa.cer issuingCa/issuingCa_dup.cer
openssl x509 -in issuingCa/issuingCa_dup.cer -inform PEM -out issuingCa/issuingCa.der -outform DER 
rm issuingCa/issuingCa.csr issuingCa/issuingCa.pem issuingCa/issuingCa_dup.cer


######### Configuration openssl configuration file for server certificate request

echo "-> Generating openssl certificate request configuration file for server certificate"

cat > server-req-cert.config <<-EOF
#
# OpenSSL configuration file for server certificate request.
#
[ req ]
default_bits        = $key_size
default_keyfile     = server/server.key
default_md          = $hashtype
distinguished_name  = req_distinguished_name
x509_extension      = server_req
prompt               = no
string_mask         = nombstr
[ req_distinguished_name ]
countryName         = IL
stateOrProvinceName = State Or Province Name
localityName        = Natania
organizationName    = Cisco
organizationalUnitName = PMBU
commonName     = $sdn
emailAddress   = $sdn@cisco.com
#serialNumber   = 5200012 8BNT
[ server_req ]
basicConstraints      = critical, CA:false
subjectKeyIdentifier  = hash
authorityKeyIdentifier=keyid:always,issuer:always
#echo "keyUsage              = digitalSignature, keyEncipherment
#echo "extendedKeyUsage      = serverAuth, clientAuth
#echo "nsCertType            = server
EOF

echo "-> Done..."

######### Configuration openssl configuration file for server certificate 

echo "-> Generating openssl configuration file for server certificate"
cat > server.config <<-EOF
#
# OpenSSL configuration file for server certificate request.
#
[ ca ]
default_ca     = CA_default           # The default ca section
[ CA_default ]
dir            = .       # Where everything is kept
certs          = \$dir/certs
crl_dir        = \$dir/crl
database       = \$dir/certindex.txt
new_certs_dir  = \$dir/certs
certificate    = \$dir/$CAcert
serial         = \$dir/serial
crl            = \$dir/ca.crl
private_key    = \$dir/$CApvk
RANDFILE       = \$dir/private/.rand
default_days     = 730
default_crl_days = 30
default_md       = $hashtype
Preserve         = no
x509_extensions  = server_cert
copy_extensions  = none
policy           = policy_anything
[ server_cert ]
basicConstraints        = critical, CA:false
authorityKeyIdentifier  = keyid:always
subjectKeyIdentifier    = hash
keyUsage                = digitalSignature, nonRepudiation, keyEncipherment
extendedKeyUsage        = serverAuth, clientAuth
#extendedKeyUsage        = serverAuth
nsCertType              = client, server, objsign
nsComment               = \"Server certificate generated using OpenSSL for testing PKI functionality in AAA server\"
nsCaRevocationUrl = http://www.domain.dom/ca-crl.pem
[ policy_anything ]
countryName              = supplied
stateOrProvinceName      = optional
localityName             = optional
organizationName         = supplied
organizationalUnitName   = optional
commonName               = supplied
emailAddress             = optional
#serialNumber            = optional
[ crl_ext ]
issuerAltName=issuer:copy
authorityKeyIdentifier=keyid:always,issuer:always
EOF

echo "-> Done..."


### Generating Server Certificate

echo "-> Generating Server private key ,certificate request and certificate"
echo "Private key password is : $passwd"

echo "-> Generating Server private key with RSA encryption"

openssl genrsa -des -passout pass:$passwd -out server/server.key $key_size 

echo "-> Generating Server private key in pkcs\#8 format using DES encryption"
openssl pkcs8 -in server/server.key -passin pass:$passwd -passout pass:$passwd -v2 des -topk8 -out server/server_pvk_des.p8c

echo "-> Generating Server private key in pkcs\#8 format using 3DES encryption"
openssl pkcs8 -in server/server.key -passin pass:$passwd -passout pass:$passwd -v2 des3 -topk8 -out server/server_pvk_des3.p8c

echo "-> Generating Server private key in pkcs\#8 format using AES encryption"
openssl pkcs8 -in server/server.key -passin pass:$passwd -passout pass:$passwd -v2 aes128 -topk8 -out server/server_pvk_aes128.p8c

openssl req -new -key server/server.key -passin pass:$passwd -out server/server.csr -config ./server-req-cert.config

cat server/server.csr server/server.key > server/server.pem
openssl ca -batch -notext -passin pass:$passwd -out server/server.cer -config ./server.config -days $ServerExp -infiles server/server.pem

######### Creating server certificate in DER format

openssl x509 -in server/server.cer -out server/server.der -outform DER

######### Creating server certificate PKCS#12 format ( Windows compatible )

openssl pkcs12 -export -passout pass:$passwd -in server/server.cer -inkey server/server.key -passin pass:$passwd -certfile $p12CAcert -name "ACSServer" -out server/server.p12

#rm -f server/server.pem
echo "-> Done..."


###### Creating openssl configuration file for user generation certificate request 

echo "-> Generating configuration file for user certificate request for openssl"

echo "#" > user-cert-req.conf
echo "# OpenSSL configuration file for user certificate request." >> user-cert-req.conf
echo "#" >> user-cert-req.conf
echo "" >> user-cert-req.conf
echo "oid_section         = new_oids" >> user-cert-req.conf
echo "[ new_oids ]" >> user-cert-req.conf
echo "uid=0.9.2342.19200300.100.1.1" >> user-cert-req.conf
echo "[ req ]" >> user-cert-req.conf
echo "default_bits        = $key_size" >> user-cert-req.conf
echo "default_keyfile     = user.key" >> user-cert-req.conf
echo "default_md          = $hashtype" >> user-cert-req.conf
echo "distinguished_name  = req_distinguished_name" >> user-cert-req.conf
echo "x509_extensions     = user_req" >> user-cert-req.conf
echo "string_mask        = nombstr" >> user-cert-req.conf
#echo "string_mask         = utf8only" >> user-cert-req.conf
#echo "utf8                = yes" >> user-cert-req.conf
echo "" >> user-cert-req.conf
echo "[ req_distinguished_name ]" >> user-cert-req.conf
echo "0.commonName              = Common Name" >> user-cert-req.conf
echo "0.commonName_max          = $cn_max_size" >> user-cert-req.conf
echo "1.commonName              = Common Name1" >> user-cert-req.conf
echo "2.commonName_max          = $cn_max_size" >> user-cert-req.conf
echo "0.emailAddress            = Email Address" >> user-cert-req.conf
echo "0.emailAddress_max        = $em_max_size" >> user-cert-req.conf
echo "1.emailAddress            = Email Address1" >> user-cert-req.conf
echo "1.emailAddress_max        = $em_max_size" >> user-cert-req.conf
echo "0.stateOrProvinceName     = IL" >> user-cert-req.conf
echo "1.stateOrProvinceName     = IL" >> user-cert-req.conf
echo "0.organizationalUnitName  = No" >> user-cert-req.conf
echo "1.organizationalUnitName  = No" >> user-cert-req.conf
echo "2.organizationalUnitName  = No" >> user-cert-req.conf
echo "0.organizationName        = No" >> user-cert-req.conf
echo "1.organizationName        = No" >> user-cert-req.conf
echo "0.serialNumber            = Serial Number" >> user-cert-req.conf
echo "1.serialNumber            = Serial Number" >> user-cert-req.conf
echo "0.street                  = Street" >> user-cert-req.conf
echo "1.street                  = Street" >> user-cert-req.conf
echo "0.uid                     = user id" >> user-cert-req.conf
echo "0.uid_max                 = 20" >> user-cert-req.conf
echo "1.uid                     = user id" >> user-cert-req.conf
echo "1.uid_max                 = 20" >> user-cert-req.conf
echo "surname                   = surname" >> user-cert-req.conf
echo "surname_max               = 20" >> user-cert-req.conf
echo "name                      = Name" >> user-cert-req.conf
echo "name_max                  = 20" >> user-cert-req.conf
echo "givenName                 = Given Name" >> user-cert-req.conf
echo "givenName_max             = 20" >> user-cert-req.conf
echo "initials                  = Mr." >> user-cert-req.conf
echo "initials_max              = 20" >> user-cert-req.conf
echo "generationQualifier       = IV" >> user-cert-req.conf
echo "generationQualifier_max   = 20" >> user-cert-req.conf
echo "title                     = Doctor" >> user-cert-req.conf
echo "title__max                = 20" >> user-cert-req.conf
echo "dnQualifier               = dnQualifier" >> user-cert-req.conf
echo "dnQualifier_max           = 20" >> user-cert-req.conf
echo "" >> user-cert-req.conf
echo "[ user_req ]" >> user-cert-req.conf
echo "basicConstraints         = critical, CA:false" >> user-cert-req.conf
echo "subjectKeyIdentifier     = hash" >> user-cert-req.conf
echo "keyUsage                 = digitalSignature, nonRepudiation, keyEncipherment" >> user-cert-req.conf
echo "extendedKeyUsage         = clientAuth, emailProtection" >> user-cert-req.conf
echo "nsCertType               = client, email" >> user-cert-req.conf
echo "# nsComment              = "Requete de signature de certificat"" >> user-cert-req.conf
echo "" >> user-cert-req.conf
echo "subjectAltName  = email:copy" >> user-cert-req.conf
echo "" >> user-cert-req.conf
echo "nsRevocationUrl = ldap://ldapip:9009/?certificateRevocationList?sub?(cn=CRL)" >> user-cert-req.conf


echo "-> Done..."




###### Creating openssl configuration file for machine CSR 

echo "-> Generating configuration file for machine certificate sign request for openssl"

cat > machine-cert-req.conf <<-EOF
[ req ]
default_bits        = $key_size
default_keyfile     = user.key
default_md          = $hashtype
distinguished_name  = req_distinguished_name
x509_extensions     = user_req
string_mask         = nombstr
[ req_distinguished_name ]
commonName              = Common Name
commonName_max          = $cn_max_size
[ user_req ]
basicConstraints         = critical, CA:false
subjectKeyIdentifier     = hash
keyUsage                 = digitalSignature, keyEncipherment
extendedKeyUsage         = clientAuth
nsCertType               = client
subjectAltName  = DNS:$machinen.$domainpatern
EOF

echo "-> Done..."

######### Configuration file for machine public key finnaly signed by CA

echo "-> Generating configuration file for machine certificate generation for openssl"

cat > machinecert.config <<-EOF
[ ca ] 
default_ca = default_CA 
[ default_CA ] 
dir = . 
certs = \$dir 
new_certs_dir = \$dir/certs 
database = \$dir/certindex.txt 
serial = \$dir/serial 
certificate = \$dir/$CAcert 
private_key = \$dir/$CApvk
default_days = 30 
default_crl_days = 30 
default_md = $hashtype 
preserve = yes 
x509_extensions = user_cert 
policy = policy_anything 
email_in_dn = no 
[ policy_anything ] 
commonName             = supplied
emailAddress           = optional
stateOrProvinceName    = optional
organizationName       = optional
organizationalUnitName = optional
organizationalUnitName = optional
organizationalUnitName = optional
serialNumber           = optional
street                 = optional 
[ user_cert ]
basicConstraints = critical,CA:false 
#....echo "authorityKeyIdentifier=keyid:always,issuer:always 
authorityKeyIdentifier=keyid:always
subjectKeyIdentifier = hash
keyUsage = digitalSignature,nonRepudiation,keyEncipherment
extendedKeyUsage = clientAuth, serverAuth
nsCertType = client, email,objsign
subjectAltName = DNS:$machinen.$domainpatern
nsComment = \"Machine certificare created by OpenSSL for ACS\"
crlDistributionPoints=URI:http://www.yourip.here/crllist.crl
#echo "#extendedKeyUsage = clientAuth,emailProtection
EOF

echo "-> Done..."


######### Configuration file for final user certificates generation

echo "-> Generating configuration file for user certificate generation for openssl"

cat > usercert.config <<-EOF
[ ca ] 
default_ca = default_CA
[ default_CA ]
dir = .
certs = \$dir
new_certs_dir = \$dir/certs
database = \$dir/certindex.txt
serial = \$dir/serial
certificate = \$dir/$CAcert
private_key = \$dir/$CApvk
default_days = 30
default_crl_days = 30
default_md = $hashtype
#default_md = md5
preserve = yes
x509_extensions = user_cert
policy = policy_anything
email_in_dn = yes
oid_section = new_oids
[ new_oids ]
uid=0.9.2342.19200300.100.1.1 # user ID
[ policy_anything ]
commonName             = supplied
commonName             = supplied
emailAddress           = supplied
emailAddress           = supplied
stateOrProvinceName    = optional
stateOrProvinceName    = optional
organizationalUnitName = supplied
organizationalUnitName = optional
organizationalUnitName = optional
organizationName       = supplied
organizationName       = supplied
serialNumber           = optional
serialNumber           = optional
street                 = optional
street                 = optional
userId                 = optional
userId                 = optional
surname                = optional
name                   = optional
givenName              = optional
initials               = optional
title                  = optional
generationQualifier    = optional
dnQualifier            = optional
[ user_cert ]
basicConstraints = critical,CA:false
authorityKeyIdentifier=keyid:always,issuer:always
subjectKeyIdentifier     = hash
keyUsage = digitalSignature,nonRepudiation,keyEncipherment
extendedKeyUsage = clientAuth, emailProtection
nsCertType = client, email
nsComment = \"User certificare created by OpenSSL for ACS\"
crlDistributionPoints=URI:http://www.yourip.here/crllist.crl
EOF

# setting up SAN name
if [ $san_cplx -gt 0 ]; then #check if SAN is needed

 case $san_cplx in	
      1)  
cat >> usercert.config <<-EOF
subjectAltName = email:copy
EOF
        ;;
      2) 
cat >> usercert.config <<-EOF
subjectAltName = email:САША Атлас
EOF
        ;;
      3) 
cat >> usercert.config <<-EOF
subjectAltName =email:copy,email:my@other.address,URI:http://my.url.here/,otherName:1.3.6.1.5.5.7.8.7;IA5STRING:_xmpp-client.im.example.com,IP:192.168.7.1,RID:1.2.3.4,dirName:dir_sect,ediPartyName:aaa;bbb
[dir_sect]
C=UK
O=My Organization
OU=My Unit
CN=My Name
EOF
        ;;
     esac 
fi
#subjectAltName = email:copy
#subjectAltName = email:САША Атлас
#subjectAltName=email:大戦士と平和のメーカー
#subjectAltName =email:copy,email:my@other.address,URI:http://my.url.here/,otherName:1.3.6.1.5.5.7.8.7;IA5STRING:_xmpp-client.im.example.com,IP:192.168.7.1,RID:1.2.3.4,dirName:dir_sect

echo "-> Done..."

#### Generating ACS user configuration file
echo "OFFLINE:" > acs/CSDBUsers.txt

fi # Create only user related data
echo "NUMOFUCERT " $numofucert 

machine_temp_pattern=$machinen # holds machine pattern
user_temp_pattern=$upattern # holds user pattern

while [ $i -lt $numofucert ]; do

if [ $noCA -ne 1 ]; then # create only users directory

if [ "$machinen" != "" ]; then # if request for machine certificate is received

if [ $numofucert -gt 1 ]; then # check if only single certificate is required
 machinen=$machine_temp_pattern$i
fi

echo "Generate private key for : $machinen.$domainpatern"
openssl genrsa -out clients/$machinen.pvk $key_size 

echo "-> Enveloping private key in PKCS#8 format using 3des encryption..."
openssl pkcs8 -in clients/$machinen.pvk -passin pass:$passwd -passout pass:$passwd -v2 des3 -topk8 -out clients/$machinen"_pvk_des3".p8c
echo "-> Enveloping private key in PKCS#8 format using aes128 encryption..."
openssl pkcs8 -in clients/$machinen.pvk -passin pass:$passwd -passout pass:$passwd -v2 aes128 -topk8 -out clients/$machinen"_pvk_aes128".p8c


echo "$machinen.$domainpatern" > enter_machine.txt
echo "$machinen.$domainpatern" >> enter_machine.txt


######### Creating certificate request for machine
  openssl req -new  -config $MACHINE_CSR_CONFIG -key clients/$machinen.pvk -out clients/$machinen.csr < enter_machine.txt # 2>/dev/null

if [ $i -lt "$FuserExp" ]; then # if still fast expired certificates are needed
  echo $i
  openssl ca -batch -notext -passin pass:$passwd -config machinecert.config -days 1 -out clients/$machinen.cer -infiles clients/$machinen.csr      
else
  openssl ca -batch -notext -passin pass:$passwd -config machinecert.config -days $userExp -out clients/$machinen.cer -infiles clients/$machinen.csr     
fi

openssl verify -verbose -purpose sslclient -CAfile "$PWD/"$CAcert clients/$machinen.cer >> certver.log

######### Creating machine certificate in DER format ( LDAP compatible )

openssl x509 -in clients/$machinen.cer -out clients_der/$machinen.der -outform DER

######### Creating machine certificate PKCS#12 format ( Windows compatible )

openssl pkcs12 -export -passout pass:$passwd -in clients/$machinen.cer -inkey clients/$machinen.pvk -certfile $p12CAcert -name "$machinen" -out clients_p12/$machinen.p12

fi

if [ "$upattern" != "" ]; then # if request for user certificate is recieved

if [ $numofucert -gt 1 ]; then # check if only single certificate is required
 upattern=$user_temp_pattern$i
fi

 

######### Creating private key for user

#echo -e "大戦士と平和のメーカー" > enter_user.txt
#echo -e "大戦士と平和のメーカー@$domainpatern" >> enter_user.txt

echo "$upattern" > enter_user.txt
echo "Users" >> enter_user.txt
echo "$upattern@$domainpatern" >> enter_user.txt
echo $upattern"1@$domainpatern" >> enter_user.txt
echo "IL" >> enter_user.txt
echo "CA" >> enter_user.txt
echo "Managment" >> enter_user.txt
echo "Managment1" >> enter_user.txt
echo "Managment2" >> enter_user.txt
echo "Cisco" >> enter_user.txt
echo "Systems" >> enter_user.txt
#echo "IL" >> enter_user.txt
echo "520001$i 8BNT" >> enter_user.txt
echo "520002$i 8BNT" >> enter_user.txt
echo "2nd. Hard Drive " >> enter_user.txt
echo "3nd. Soft Drive " >> enter_user.txt
echo "$upattern" >> enter_user.txt
echo "second_$upattern" >> enter_user.txt
echo "sur_$upattern" >> enter_user.txt
echo "name_$upattern" >> enter_user.txt
echo "given_$upattern" >> enter_user.txt
echo "Mr." >> enter_user.txt
echo "III" >> enter_user.txt
echo "Doctor" >> enter_user.txt
echo "DC=example,DC=com" >> enter_user.txt

echo "Generate private key for : $upattern"
openssl genrsa -out clients/$upattern.pvk $key_size 

echo "-> Enveloping private key in PKCS#8 format using 3des encryption..."
openssl pkcs8 -in clients/$upattern.pvk -passin pass:$passwd -passout pass:$passwd -v2 des3 -topk8 -out clients/$upattern"_pvk_des3".p8c
echo "-> Enveloping private key in PKCS#8 format using aes128 encryption..."
openssl pkcs8 -in clients/$upattern.pvk -passin pass:$passwd -passout pass:$passwd -v2 aes128 -topk8 -out clients/$upattern"_pvk_aes128".p8c

######### Creating certificate request for user
 openssl req -utf8 -new -config $USER_CSR_CONFIG -key clients/$upattern.pvk -out clients/$upattern.csr < enter_user.txt 2>/dev/null
 
 #openssl req -utf8 -new -config $USER_CSR_CONFIG -subj "/O=大戦士と平和のメーカー/OU=管理/emailAddress=aa@cisco.com/CN=Хаси" -key clients/$upattern.pvk -out clients/$upattern.csr < enter_user.txt

if [ $i -lt "$FuserExp" ]; then # if still fast expired certificates are needed
   openssl ca -utf8 -batch -notext -passin pass:$passwd -config usercert.config -days 1 -out clients/$upattern.cer -infiles clients/$upattern.csr     
   
else
   openssl ca -utf8 -batch -notext -passin pass:$passwd -config usercert.config -days $userExp -out clients/$upattern.cer -infiles clients/$upattern.csr     
fi

openssl verify -verbose -purpose sslclient -CAfile "$PWD/"$CAcert clients/$upattern.cer >> certver.log

######### Creating user certificate in DER format

openssl x509 -in clients/$upattern.cer -out clients_der/$upattern.der -outform DER

######### Creating user certificate PKCS#12 format

openssl pkcs12 -export -passout pass:$passwd -in clients/$upattern.cer -inkey clients/$upattern.pvk -certfile $p12CAcert -name "$upattern" -out clients_p12/$upattern.p12


fi

######## Creating CSDB configuration file for user insertion
echo "-> Creating CSDB configuration for user : $upattern"
echo "ADD:"$upattern":CSDB:"$upattern":PROFILE:0" >> acs/CSDBUsers.txt
echo "-> Creating Active Directory configuration for user : $upattern"
echo "net user $upattern $upattern /ADD /times:all  /expires:never /comment:\"Stress Employer User\"">> acs/ActDirUsr.bat

fi # end of only users if

let "i=$i + 1"
done

if [ $noCA -ne 1 ]; then # create only users directory
  
######### Creating CRL repository

ls certs/ > input.txt

i=0
let "numofrev=$numofrev + 1" # shifting certificate revokation to the first client cert
while read line; do
   if [ $i -gt 1 ] && [ $i -le $numofrev ]; then
     openssl ca -batch -passin pass:$passwd -config server.config -revoke certs/$line 
   fi
   ((i++))
  done < input.txt

echo "-> Publishing CRL repository"
openssl ca -gencrl -crldays $crlExp -batch -passin pass:$passwd -config server.config -crlexts crl_ext -out crl/crllist.crl
echo "-> Done..."
fi


echo "Removing temporary files..."
rm -f enter.txt
rm -f input.txt
rm -f *.old
rm -f clients/*.csr
rm -f policyCa/*.csr
rm -f policyCa/*.pem
rm -f server/*.csr

##### Creating gzip package
echo "-> Compressing bulk data in single certificates.tar.gz package"
cd ..
tar -czf certificates.tar.gz sslcert/ 
gzip certificates.tar.gz -t -v

echo "-> Done..."
