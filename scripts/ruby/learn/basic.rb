#!/usr/bin/ruby

def sayGoodnight(name)
  "Goodnight, #{name}"
end


# Time for bed...
puts sayGoodnight("John-Boy")
puts sayGoodnight("Mary-Ellen")

puts "length of: gin goint is: "
puts  "gin joint".length   

puts "index of c in Rick: "
puts "Rick".index("c")
puts  "absolute value of -1942: "
puts -1942.abs

#arrays
a = [ 1, 'cat', 3.14 ]   # array with three elements
# access the first element
a[0] 
# set the third element
a[2] = nil
# dump out the array
puts "array content: #{a} " 

#initialize array with words
a = %w{ ant bee cat dog elk }
puts "array of words is #{a}"
puts "first element #{a[0]}"

#hashes
instSection = {
  'cello'     => 'string',
  'clarinet'  => 'woodwind',
  'drum'      => 'percussion',
  'oboe'      => 'woodwind',
  'trumpet'   => 'brass',
  'violin'    => 'string'
}

puts "musical instruments hash: #{instSection}"
puts "the oboe is #{instSection['oboe']} and the guitar is #{instSection['guitar']} (empty)"

#keys that don't exist in the hash return null or false, following code demonstrate how this can be changed to return for example 0 (if one wants to counts the amount of keys)
histogram = Hash.new(0)
puts "key1 is contained #{histogram['key1']} times"
histogram['key1'] = histogram['key1'] + 1
puts "add 1 and now key1 is contained #{histogram['key1']} times"









