# frozen_string_literal: true

# This file is meant to contain handy Ruby extentions.
# It can be replaced in the future by gems such as activesupport (https://github.com/rails/rails/tree/master/activesupport).
# Currently activesupport gem is not present in Docker image in order to save time when building it
# since there is no significant benefits from installing ~1,6 MB to use only a few simple methods.

class String
  # Returns the string, removing all whitespace on both ends of the string
  # and changing whitespace groups into one space each.
  #
  # %{ foo
  #    bar }.squish                      # => "foo bar"
  # " foo   bar    \n   \t   boo".squish # => "foo bar boo"
  def squish
    self.split(' ').join(' ')
  end
end
