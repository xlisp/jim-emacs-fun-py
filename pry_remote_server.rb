require 'pry-remote'

class Foo
  def initialize(x, y)
    binding.remote_pry
  end
end

Foo.new 10, 20

# ruby pry_remote_test.rb 
# [pry-remote] Waiting for client on druby://127.0.0.1:9876
# => 接受到客户端连接的时候：[pry-remote] Client received, starting remote session

# ruby -v
# ruby 2.6.10p210 (2022-04-12 revision 67958) [universal.arm64e-darwin23]

