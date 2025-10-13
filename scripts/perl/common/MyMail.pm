package MyMail;

# Author, yosi.
# Desc. Mail sending functions. 

# To use by scripts put at @inc.
# see dir list of @inc by:
# perl -e 'print join("\n",@INC)."\n"'
# 
# On laptop its path is: /usr/lib/perl5/5.8/MyPkgs
 
# send mail function.
# parameters.
# subject
# message
# from
# to list

sub send_mail{
my $subj = shift;
my $msg =  shift;
my $from = shift;
my @to = @_;
#shift(@to);

print "subject, $subj\nmessage, $msg\nfrom, $from\nTo list, $to\n";
exit 0;

$subject = "subject: make_all_general_2.5 auto notification\n";
$data="$_[0]";

#create SMTP object
$smtp = Net::SMTP->new("il-tlv-smtpout.comverse.com") ;
print $smtp->domain,"\n";

#sender mail
$smtp->mail("Yosi.Izaq\@comverse.com") ;
print "sender Yosi.Izaq\@comverse.com\n";

#reciever mail
#$smtp->to("Yosi.Izaq\@comverse.com") ;
#$smtp->to($to) ;
$smtp->recipient(@to);
print "reciever: @to\n";

#start SMTP data connection
$smtp->data() ;
print "start SMTP connection\n";

#send data, can repeat as many times as needed
$smtp->datasend($subject) ;
$smtp->datasend($data) ;
print "send mail: $data\n";

#end SMTP data connection
$smtp->dataend() ;
print "end data connection\n";

#Close the connection to SMTP server.
$smtp->quit() ;
print "end server connection\n";


}


1;

