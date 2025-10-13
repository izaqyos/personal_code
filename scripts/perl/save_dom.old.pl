#!/usr/bin/perl
# Author Yosi Izaq
# Description. save dom2 games

use File::Copy;

@params = ();
@params = @ARGV;
$dom_path = "/cygdrive/d/temp/dom/";
$save_path = "/cygdrive/d/temp/temp/";

#print "there are " . @params . " parameters\n";
if (@params != 2){
  @params = get_params();
}

#  print "param @params\n";
  main();

sub main{
  my  $game = $params[0];
  my  $turn = $params[1];

  my  $game_path = $dom_path.$game ;
  my  $save_game_path = $save_path.$game."/".$turn;
  print "game path $game_path.\nsave game path $save_game_path\n";
  	
  if (! -e $save_game_path){
    print" creating save game directory for turn $turn.\n";
    if ( ! -e $save_path.$game){
          mkdir ($save_path.$game) || die "can't create dir $save_path.$game $!";
    }
    mkdir ($save_game_path) || die "can't create dir $save_game_path $!";
  }

  opendir(DIR, $game_path);
  @files = readdir(DIR);

  for (@files){
 
#   print "file $_\n";
#    if ($_ =~ /^\.\.*/ ){
#      print "match $& \n";
#    }

#don't want to copy . and .. ;)
    if (! /^\.\.*/){
      print "copying file $game_path/$_ to $save_game_path\n";
      copy($game_path."/".$_, $save_game_path) || die "failed copying file $game_path/$_ . $!";
  }
  }

      }

sub get_params{
  my @params = ();
  print "please enter game name\n";
  my $game = <STDIN>;
  chomp $game;

  print "please enter turn number\n";
  my $turn = <STDIN>;
  chomp $turn;
  
  push (@params, $game);
  push (@params, $turn);

#  print "params @params";

  return @params;
}
