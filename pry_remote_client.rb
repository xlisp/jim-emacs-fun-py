# 自动会连打开的druby://127.0.0.1:9876 repl 服务

坚持去λ化(中-易) jim-emacs-fun-py  master @ pry-remote

From: /Users/emacspy/EmacsPyPro/jim-emacs-fun-py/pry_remote_test.rb:5 Foo#initialize:

    4: def initialize(x, y)
 => 5:   binding.remote_pry
    6: end

[1] pry(#<Foo>)> x
=> 10
[2] pry(#<Foo>)> y
=> 20
[3] pry(#<Foo>)>

