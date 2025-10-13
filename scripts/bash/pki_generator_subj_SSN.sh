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
	echo "   -Noc, --number_of_certificates [Options] allowerd values are [0-99999...]"
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
   echo "   -hash, --hash_type [Options] allowed values are [sha1, md5]"
   echo "   -keysz, --key_size [Options] allowed values are [512,1024,2048,4096,8192]"
   echo "   -cn_max_size , --common_name_max_size [Options] allowed values are [0-999]"
   echo "   -em_max_size , --email_max_size [Options] allowed values are [0-999]" 
   echo "   -RndSn, --Random_Serial_Number" 
	echo "-------------------------------------------"
	echo "Examples of configuration:"
	echo " $0 -Cm CA -Noc 1000 -Norc 5 -up user -mp machine -dp cisco.com  -CAexp 365 -policyCaexp 365 -issuingCaexp 365 -SERexp 365 -CLTexp 365 -hash md5 -keysz 1024 -RndSn"
	echo "   - will create :"
	echo "        * 1000 user[0-999] certificates where CN will have following format:"
	echo "        * cn=user0,cn=user1... and SAN user0@example.com,user1@example.com..."
	echo "        * 1000 machine[0-999] certificates where CN will have following format:"
	echo "        * cn=machine0.cisco.com,cn=machine1... and SAN DNS: user0.cisco.com..."
	echo "        * one server certificate+private key"
	echo "        * one CA certificate+private key"
	echo "        * 5 revoked certificate-Norc | --number_of_revoked_certificates) shift
                                 numofrev=$1 # sets number of revoked certificates to create exclude server certificate
	                    echo "Number of User revoked cerificates to be generated: " $numofrev
                                ;;s"
	echo "        * every certificate will be valid for 365 days"
   echo "        * signature algorithm to be used is MD5"
   echo "        * key size will be 1024 bit"
	echo " $0 -Cm noCA -Noc 100 user"
   echo "   - will create :"
	echo "        * scripts to insert users in CSDB and Active Directory only."
	echo "        * No certificates will be created"
	echo "Note: "
	echo "Default password used for all certificates is : 1234"
	echo "CA and policyCa certificate are being generated regardless of switch settings"
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
  	  echo "| PKI Generator ver 1.1.3  +-+"
	  echo "| by Atlas Alexander       | |"
	  echo "| for Cisco Systems        | |"
	  echo "+--------------------------+ |"
	  echo " +---------------------------+"
  }

# Initial difinition part


i=0
USER_CSR_CONFIG="user-cert-req.conf"
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
key_size=1024 # default key size
hashtype=md5 # default hash type
cn_max_size=64 # default size on CN
em_max_size=64
rndSerial=100001
numofservercert=1 # number of server certificates to be 1 initially.

###################################

version # show version of the tool

if [ $# -eq 0 ]; then # if no agruments supplied then show help
 help
exit
fi

echo "+-General Info-----------------------------------------+"
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
			     CAcert="/ca/cacert.cer"
			      p12CAcert="ca/cacert.cer"
			       CApvk="/ca/cakey.pem"
                   ;;
                    
                    # use subCA to sign certificates
                    subCA) echo "All issuing certificates will be signed by 3rd CA in chain"
 				          CAcert="/issuingCa/issuingCa.cer"
				          p12CAcert="issuingCa/issuingCa.cer"
				          CApvk="/issuingCa/issuingCa.pem"
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
        -hash | --hash_type ) shift # defines type of hash to be used for sign certificates
                                 case "$1" in
                                   sha1 | SHA1) # defines $hashtype hash to be used for sign certificates
                                          hashtype=sha1
                                          echo "Signature hash algoritm is : SHA1"
                                          ;;
                                 sha2 | SHA2) # defines $hashtype hash to be used for sign certificates
                                           hashtype=sha256
                                          echo "Signature hash algoritm is : SHA2"
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
                                
        -keysz | --key_size ) shift  # what type of certificate to generate

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
        -RndSn | --Random_Serial_Number) shift 
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

if [ "$numofucert" -le "$FuserExp" ]; then # if number of user certificate is lesser than number of fast expired certificates, exit
echo "Configuration problems :"
echo " ---> Number of certificates must be greater than number of fast expired certificates"
exit
fi

if [ "$numofucert" -le "$numofrev" ]; then # if number of user certificate is lesser than number of fast expired certificates, exit
echo "Configuration problems :"
echo " ---> Number of certificates must be greater than number of revoked certificates"
exit
fi
 


 echo "+-Experation Info--------------------------------------+"

 
   echo "Number of days CA certificate is valid: " $CAExp
   echo "Number of days policyCa certificate is valid: " $policyCaExp
   echo "Number of days Server certificate is valid: " $ServerExp
   echo "Number of days User/Machine certificate is valid: " $userExp


if [ -d sslcert ]; then # removing old directory if exists
echo "Warning : sslcert directory already exists..."
echo "Would you like to [r]emove directory or [a]bort execution"

read choice
  
  if [ $choice = 'r' ] || [ $choice = 'R' ]; then 
     echo Removing old Directory...
     rm -rf sslcert
  else
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

echo "#"> ca.config
echo "# OpenSSL configuration file.">> ca.config
echo "#">> ca.config
echo "">> ca.config
echo "# Establish working directory.">> ca.config
echo "">> ca.config
echo "[ req ]">> ca.config
echo "default_bits        = $key_size">> ca.config
echo "default_keyfile     = ca/cakey.pem">> ca.config
echo "default_md          = $hashtype">> ca.config
echo "distinguished_name  = req_distinguished_name">> ca.config
echo "x509_extensions     = rootca_cert">> ca.config
echo "prompt               = no" >> ca.config
echo "">> ca.config
echo "[ req_distinguished_name ]">> ca.config
echo "countryName            = IL">> ca.config
echo "stateOrProvinceName         = State Or Provice Name">> ca.config
echo "localityName         = Natania">> ca.config
echo "organizationName         = Cisco Systems.">> ca.config
echo "organizationalUnitName         = ISE\, Identity Division">> ca.config
echo "commonName         = $cfp">> ca.config
echo "emailAddress     = $cfp@$domainpatern">> ca.config
echo "">> ca.config
echo "[ rootca_cert ]">> ca.config
echo "# Following section describes extensions which are being added to the Root CA">> ca.config
echo "">> ca.config
echo "basicConstraints       = critical, CA:true">> ca.config
echo "subjectKeyIdentifier   = hash">> ca.config
echo "keyUsage               = critical, keyCertSign, cRLSign">> ca.config
echo "authorityKeyIdentifier = keyid:always,issuer:always">> ca.config
echo "nsCertType             = sslCA, emailCA, objCA">> ca.config
echo "nsComment              = "Following certificate generated by OpenSSL"">> ca.config
echo "">> ca.config

echo "-> Done..."


### Generating root CA

echo "-> Generating Root CA"

echo "Private key password is : $passwd"
openssl req -new -x509  -passout pass:$passwd -keyout ca/cakey.pem -out ca/cacert.cer -days $CAExp  -passin pass:$passwd -config ./ca.config -subj /DC=org/DC=OpenSSL/DC=users/UID=123456+CN=CAforISE\ Test
cp ca/cacert.cer ca/cacert_dup.cer
openssl x509 -in ca/cacert_dup.cer -inform PEM -out ca/cacert.der -outform DER
rm ca/cacert_dup.cer
echo "-> Done..."


######### Configuration openssl configuration file for policyCa certificate request

echo "-> Generating openssl certificate request configuration file for policyCa certificate"

echo "#" > policyCa-cert-req.config
echo "# OpenSSL configuration file for policyCa certificate request." >> policyCa-cert-req.config
echo "#" >> policyCa-cert-req.config
echo "" >> policyCa-cert-req.config
echo "" >> policyCa-cert-req.config
echo "[ req ]" >> policyCa-cert-req.config
echo "default_bits         = $key_size" >> policyCa-cert-req.config
echo "default_keyfile      = policyCa/policyCa.key" >> policyCa-cert-req.config
echo "default_md           = $hashtype" >> policyCa-cert-req.config
echo "distinguished_name   = req_distinguished_name" >> policyCa-cert-req.config
echo "x509_extensions      = policyCa_req" >> policyCa-cert-req.config
echo "string_mask          = nombstr" >> policyCa-cert-req.config
echo "prompt               = no" >> policyCa-cert-req.config
echo "" >> policyCa-cert-req.config
echo "[ req_distinguished_name ]" >> policyCa-cert-req.config
echo "countryName         = IL" >> policyCa-cert-req.config
echo "" >> policyCa-cert-req.config
echo "stateOrProvinceName         = State Or Province Name" >> policyCa-cert-req.config
echo "" >> policyCa-cert-req.config
echo "localityName         = Natania" >> policyCa-cert-req.config
echo "" >> policyCa-cert-req.config
echo "organizationName         = Cisco" >> policyCa-cert-req.config
echo "" >> policyCa-cert-req.config
echo "organizationalUnitName         = ACS Devision" >> policyCa-cert-req.config
echo "" >> policyCa-cert-req.config
echo "commonName         = policyCa_$cfp" >> policyCa-cert-req.config
echo "" >> policyCa-cert-req.config
echo "emailAddress     = policyCa_$cfp@$domainpatern" >> policyCa-cert-req.config
echo "" >> policyCa-cert-req.config
echo "[ policyCa_req ]" >> policyCa-cert-req.config
echo "basicConstraints        = critical, CA:true" >> policyCa-cert-req.config
echo "subjectKeyIdentifier    = hash" >> policyCa-cert-req.config
echo "authorityKeyIdentifier  = keyid, issuer:always" >> policyCa-cert-req.config
echo "keyUsage                = critical, keyCertSign, cRLSign" >> policyCa-cert-req.config
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
echo "default_bits         = $key_size" >> issuingCa-cert-req.config
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
echo "Preserve          = no       # keep passed DN ordering">> issuingCa.config
echo "">> issuingCa.config
echo "x509_extensions   = issuingCa_cert">> issuingCa.config
echo "copy_extensions   = none">> issuingCa.config
echo "policy            = policy_match">> issuingCa.config
echo "">> issuingCa.config
echo "[ issuingCa_cert ]">> issuingCa.config
echo "basicConstraints        = critical, CA:true">> issuingCa.config
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
echo $passwd
echo $issuingCaExp
openssl ca -batch -notext -passin pass:$passwd -out issuingCa/issuingCa.cer -config ./issuingCa.config -days $issuingCaExp -infiles issuingCa/issuingCa.pem
cp issuingCa/issuingCa.cer issuingCa/issuingCa_dup.cer
openssl x509 -in issuingCa/issuingCa_dup.cer -inform PEM -out issuingCa/issuingCa.der -outform DER 
rm issuingCa/issuingCa.csr issuingCa/policyCa.pem issuingCa/issuingCa_dup.cer


######### Configuration openssl configuration file for server certificate request

echo "-> Generating openssl certificate request configuration file for server certificate"

echo "#" > server-req-cert.config
echo "# OpenSSL configuration file for server certificate request." >> server-req-cert.config
echo "#" >> server-req-cert.config
echo "" >> server-req-cert.config
echo "[ req ]" >> server-req-cert.config
echo "default_bits        = $key_size" >> server-req-cert.config
echo "default_keyfile     = server/server.key" >> server-req-cert.config
echo "default_md          = $hashtype" >> server-req-cert.config
echo "distinguished_name  = req_distinguished_name" >> server-req-cert.config
echo "x509_extension      = server_req" >> server-req-cert.config
echo "prompt               = no" >> server-req-cert.config
echo "string_mask         = nombstr" >> server-req-cert.config
echo "" >> server-req-cert.config
echo "[ req_distinguished_name ]" >> server-req-cert.config
echo "countryName         = IL" >> server-req-cert.config
echo "stateOrProvinceName = State Or Province Name" >> server-req-cert.config
echo "localityName        = Natania" >> server-req-cert.config
echo "organizationName    = Cisco" >> server-req-cert.config
echo "organizationalUnitName = PMBU" >> server-req-cert.config
echo "commonName     = $sdn" >> server-req-cert.config
echo "emailAddress   = $sdn@example.com" >> server-req-cert.config
echo "serialNumber   = 5200012 8BNT">> server-req-cert.config
echo "[ server_req ]" >> server-req-cert.config
echo "basicConstraints      = critical, CA:false" >> server-req-cert.config
echo "subjectKeyIdentifier  = hash" >> server-req-cert.config
echo "authorityKeyIdentifier=keyid:always,issuer:always" >> server-req-cert.config

#echo "keyUsage              = digitalSignature, keyEncipherment" >> server-req-cert.config
#echo "extendedKeyUsage      = serverAuth, clientAuth" >> server-req-cert.config
#echo "nsCertType            = server" >> server-req-cert.config
echo "-> Done..."

######### Configuration openssl configuration file for server certificate 

echo "-> Generating openssl configuration file for server certificate"
echo "#" > server.config
echo "# OpenSSL configuration file for server certificate request." >> server.config
echo "#" >> server.config
echo "[ ca ]" >> server.config
echo "default_ca     = CA_default           # The default ca section" >> server.config
echo "" >> server.config
echo "[ CA_default ]" >> server.config
echo "dir            = .       # Where everything is kept" >> server.config
echo "certs          = "\$"dir/certs           # Where the issued certs are kept" >> server.config
echo "crl_dir        = "\$"dir/crl             # Where the issued crl are kept" >> server.config
echo "database       = "\$"dir/certindex.txt       # database index file." >> server.config
echo "new_certs_dir  = "\$"dir/certs        # default place for new certs." >> server.config
echo "certificate    = "\$"dir$CAcert          # The CA certificate" >> server.config
echo "serial         = "\$"dir/serial          # The current serial number" >> server.config
echo "crl            = "\$"dir/ca.crl          # The current CRL" >> server.config
echo "private_key    = "\$"dir$CApvk  # The private key" >> server.config
echo "RANDFILE       = "\$"dir/private/.rand   # private random number file" >> server.config
echo "" >> server.config
echo "default_days     = 730     # how long to certify for" >> server.config
echo "default_crl_days = 30      # how long before next CRL" >> server.config
echo "default_md       = $hashtype     # which md to use." >> server.config
echo "Preserve         = no      # keep passed DN ordering" >> server.config
echo "" >> server.config
echo "x509_extensions  = server_cert" >> server.config
echo "copy_extensions  = none" >> server.config
echo "policy           = policy_anything" >> server.config
echo "" >> server.config
echo "[ server_cert ]" >> server.config
echo "basicConstraints        = critical, CA:false" >> server.config
echo "authorityKeyIdentifier  = keyid:always" >> server.config
echo "subjectKeyIdentifier    = hash" >> server.config
echo "keyUsage                = digitalSignature, nonRepudiation, keyEncipherment" >> server.config
#echo "extendedKeyUsage        = serverAuth, clientAuth" >> server.config
echo "extendedKeyUsage        = serverAuth" >> server.config
echo "nsCertType              = server, objsign" >> server.config
echo "nsComment               = \"Server certificate generated using OpenSSL for testing PKI functionality in AAA server\"" >> server.config
echo "nsCaRevocationUrl = http://www.domain.dom/ca-crl.pem" >> server.config
echo "">> server.config
echo "[ policy_anything ]">> server.config
echo "countryName              = supplied">> server.config
echo "stateOrProvinceName      = optional">> server.config
echo "localityName             = optional">> server.config
echo "organizationName         = supplied">> server.config
echo "organizationalUnitName   = optional">> server.config
echo "commonName               = supplied">> server.config
echo "emailAddress             = optional">> server.config
echo "serialNumber             = optional">> server.config

echo "[ crl_ext ]" >> server.config
echo "issuerAltName=issuer:copy" >> server.config
echo "authorityKeyIdentifier=keyid:always,issuer:always" >> server.config

echo "-> Done..."


### Generating Server Certificate
echo "-> Generating Server private key ,certificate request and certificate"
echo "Private key password is : $passwd"

#openssl genrsa -out server/$sdn.pvk $key_size 
#openssl req  -new -passout pass:$passwd -keyout server/server.key -out server/server.csr -config ./server-req-cert.config -subj /DC=org/DC=OpenSSL/DC=users/CN=server123

openssl req  -new -passout pass:$passwd -keyout server/server.key -out server/server.csr -config ./server-req-cert.config

cat server/server.csr server/server.key > server/server.pem
openssl ca -batch -notext -passin pass:$passwd -out server/server.cer -config ./server.config -days $ServerExp -infiles server/server.pem

######### Creating server certificate in DER format

openssl x509 -in server/server.cer -out server/server.der -outform DER

######### Creating server certificate PKCS#12 format ( Windows compatible )

openssl pkcs12 -export -passout pass:$passwd -in server/server.cer -inkey server/server.key -passin pass:$passwd -certfile $p12CAcert -name "ACSServer" -out server/server.p12


rm -f server/server.pem
echo "-> Done..."


###### Creating openssl configuration file for user generation certificate request 

echo "-> Generating certificate request configuration file for openssl"

echo "#" > user-cert-req.conf
echo "# OpenSSL configuration file for user certificate request." >> user-cert-req.conf
echo "#" >> user-cert-req.conf
echo "" >> user-cert-req.conf
echo "[ req ]" >> user-cert-req.conf
echo "default_bits        = $key_size" >> user-cert-req.conf
echo "default_keyfile     = user.key" >> user-cert-req.conf
echo "default_md          = sha1" >> user-cert-req.conf
echo "distinguished_name  = req_distinguished_name" >> user-cert-req.conf
echo "x509_extensions     = user_req" >> user-cert-req.conf
echo "string_mask         = nombstr" >> user-cert-req.conf
echo "" >> user-cert-req.conf
echo "[ req_distinguished_name ]" >> user-cert-req.conf
echo "commonName              = Common Name" >> user-cert-req.conf
echo "commonName_max          = $cn_max_size" >> user-cert-req.conf
echo "emailAddress            = Email Address" >> user-cert-req.conf
echo "emailAddress_max        = $em_max_size" >> user-cert-req.conf
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



#### Generating ACS user configuration file
echo "OFFLINE:" > acs/CSDBUsers.txt

fi # Create only user related data
echo "NUMOFUCERT " $numofucert 
while [ $i -lt $numofucert ]; do

if [ $noCA -ne 1 ]; then # create only users directory

if [ "$machinen" != "" ]; then # if request for machine certificate is recieved

######### Configuration file for final machine  certificates generation

echo "-> Generating configuration file for machine certificate generation for openssl"

echo "[ ca ]"> usercert.config 
echo "default_ca = default_CA">> usercert.config 
echo "">> usercert.config 
echo "[ default_CA ]">> usercert.config 
echo "dir = \.">> usercert.config 
echo "certs = "\$"dir">> usercert.config 
echo "new_certs_dir = "\$"dir/certs">> usercert.config 
echo "database = "\$"dir/certindex.txt">> usercert.config 
echo "serial = "\$"dir/serial">> usercert.config 
echo "certificate = "\$"dir$CAcert">> usercert.config 
echo "private_key = "\$"dir$CApvk">> usercert.config  #private key
echo "default_days = 30">> usercert.config 
echo "default_crl_days = 30">> usercert.config 
echo "default_md = sha1">> usercert.config 
echo "preserve = yes">> usercert.config 
echo "x509_extensions = user_cert">> usercert.config 
echo "policy = policy_anything">> usercert.config 
echo "email_in_dn = no ">> usercert.config 
echo "">> usercert.config 
echo "[ policy_anything ]">> usercert.config 
echo "commonName = supplied">> usercert.config 
echo "emailAddress = optional">> usercert.config 
echo "">> usercert.config 
echo "[ user_cert ]">> usercert.config 
echo "basicConstraints = critical,CA:false">> usercert.config 
#....echo "authorityKeyIdentifier=keyid:always,issuer:always">> usercert.config 
echo "authorityKeyIdentifier=keyid:always">> usercert.config 
echo "subjectKeyIdentifier     = hash" >> usercert.config 
echo "keyUsage = digitalSignature,nonRepudiation,keyEncipherment" >> usercert.config
echo "extendedKeyUsage = clientAuth, serverAuth">> usercert.config 
echo "nsCertType = client, email,objsign">> usercert.config 
echo "subjectAltName = DNS:$machinen$i.$domainpatern">> usercert.config
echo "nsComment = \"Machine certificare created by OpenSSL for ACS\"">> usercert.config
echo "crlDistributionPoints=URI:http://www.yourip.here/crllist.crl" >> usercert.config

#echo "#extendedKeyUsage = clientAuth,emailProtection">> usercert.config 

echo "-> Done..."

 openssl genrsa -out clients/$machinen$i.pvk $key_size 
 
 echo "machine is : " $machinen
 echo "$machinen$i.$domainpatern" > enter_machine.txt
 echo "$machinen$i.$domainpatern" >> enter_machine.txt
 
######### Creating certificate request for machine
  openssl req -new  -config $USER_CSR_CONFIG -key clients/$machinen$i.pvk -out clients/$machinen$i.csr < enter_machine.txt 

echo $userExp

if [ $i -lt "$FuserExp" ]; then # if still fast expired certificates are needed
  echo $i
  openssl ca -batch -notext -passin pass:$passwd -config usercert.config -days 1 -out clients/$machinen$i.cer -infiles clients/$machinen$i.csr      
else
  openssl ca -batch -notext -passin pass:$passwd -config usercert.config -days $userExp -out clients/$machinen$i.cer -infiles clients/$machinen$i.csr     
fi

openssl verify -verbose -purpose sslclient -CAfile "$PWD"$CAcert clients/$machinen$i.cer >> certver.log

######### Creating machine certificate in DER format ( LDAP compatible )

openssl x509 -in clients/$machinen$i.cer -out clients_der/$machinen$i.der -outform DER

######### Creating machine certificate PKCS#12 format ( Windows compatible )

openssl pkcs12 -export -passout pass:$passwd -in clients/$machinen$i.cer -inkey clients/$machinen$i.pvk -certfile $p12CAcert -name "$machinen$i" -out clients_p12/$machinen$i.p12


fi

echo "Pattern" $upattern
if [ "$upattern" != "" ]; then # if request for user certificate is recieved
 
######### Configuration file for final user certificates generation

echo "-> Generating configuration file for user certificate generation for openssl"

echo "[ ca ]"> usercert.config 
echo "default_ca = default_CA">> usercert.config 
echo "">> usercert.config 
echo "[ default_CA ]">> usercert.config 
echo "dir = \.">> usercert.config 
echo "certs = "\$"dir">> usercert.config 
echo "new_certs_dir = "\$"dir/certs">> usercert.config 
echo "database = "\$"dir/certindex.txt">> usercert.config 
echo "serial = "\$"dir/serial">> usercert.config 
echo "certificate = "\$"dir$CAcert">> usercert.config 
echo "private_key = "\$"dir$CApvk">> usercert.config  #private key
echo "default_days = 30">> usercert.config 
echo "default_crl_days = 30">> usercert.config 
echo "default_md = $hashtype">> usercert.config 
echo "preserve = yes">> usercert.config 
echo "x509_extensions = user_cert">> usercert.config 
echo "policy = policy_anything">> usercert.config 
echo "email_in_dn = no ">> usercert.config 
echo "">> usercert.config 
echo "[ policy_anything ]">> usercert.config 
echo "commonName = supplied">> usercert.config 
echo "emailAddress = optional">> usercert.config 
echo "">> usercert.config 
echo "[ user_cert ]">> usercert.config 
echo "basicConstraints = critical,CA:false">> usercert.config 
echo "authorityKeyIdentifier=keyid:always,issuer:always">> usercert.config 
echo "subjectKeyIdentifier     = hash" >> usercert.config 
echo "keyUsage = digitalSignature,nonRepudiation,keyEncipherment" >> usercert.config
echo "extendedKeyUsage = clientAuth, emailProtection">> usercert.config 
echo "nsCertType = client, email,objsign">> usercert.config 
echo "subjectAltName = email:copy">> usercert.config
#echo "subjectAltName = otherName:1.3.6.1.5.5.7.8.7;IA5STRING:_xmpp-client.im.example.com">> usercert.config
echo "nsComment = \"User certificare created by OpenSSL for ACS\"">> usercert.config
echo "crlDistributionPoints=URI:http://www.yourip.here/crllist.crl" >> usercert.config

#echo "#extendedKeyUsage = clientAuth,emailProtection">> usercert.config 

echo "-> Done..."
 
 
 
######### Creating private key for user

 openssl genrsa -out clients/$upattern$i.pvk $key_size 

 echo "user is : " $upattern
 echo "$upattern$i" > enter_user.txt
 echo "$upattern$i@$domainpatern" >> enter_user.txt
 
######### Creating certificate request for user
  openssl req -new  -config $USER_CSR_CONFIG -key clients/$upattern$i.pvk -out clients/$upattern$i.csr < enter_user.txt 

echo $userExp

if [ $i -lt "$FuserExp" ]; then # if still fast expired certificates are needed
   openssl ca -batch -notext -passin pass:$passwd -config usercert.config -days 1 -out clients/$upattern$i.cer -infiles clients/$upattern$i.csr     
   
else
   openssl ca -batch -notext -passin pass:$passwd -config usercert.config -days $userExp -out clients/$upattern$i.cer -infiles clients/$upattern$i.csr     
fi

openssl verify -verbose -purpose sslclient -CAfile "$PWD"$CAcert clients/$upattern$i.cer >> certver.log

######### Creating user certificate in DER format

openssl x509 -in clients/$upattern$i.cer -out clients_der/$upattern$i.der -outform DER

######### Creating user certificate PKCS#12 format

openssl pkcs12 -export -passout pass:$passwd -in clients/$upattern$i.cer -inkey clients/$upattern$i.pvk -certfile $p12CAcert -name "$upattern$i" -out clients_p12/$upattern$i.p12


fi





######### Creating user certificate

fi # end of only users if


######## Creating CSDB configuration file for user insertion
echo "-> Creating CSDB configuration for user : $upattern$i"
echo "ADD:"$upattern$i":CSDB:"$upattern$i":PROFILE:0" >> acs/CSDBUsers.txt
echo "-> Creating Active Directory configuration for user : $upattern$i"
echo "net user $upattern$i $upattern$i /ADD /times:all  /expires:never /comment:\"Stress Employer User\"">> acs/ActDirUsr.bat

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
