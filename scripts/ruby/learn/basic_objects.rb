#!/usr/bin/ruby

class Song 
  def initialize (name, artist, duration)
    @name = name
    @aritst = artist
    @duration = duration
    end
end

mySong = Song.new("chacito", "leon gieco", 317)
puts " my song: #{mySong.inspect} "
