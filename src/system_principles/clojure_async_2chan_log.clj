(ns system-principles.clojure-async-2chan-log
  (:require [clojure.core.async :refer [go chan <! >! sub pub close! >!!]]))

;; GPT: Clojure async write two chanel , a chanel record log message, b chanel  subscribe the a chanel and to print the log message.

;; Run: clj -X  system-principles.clojure-async-2chan-log/main
;; M-x cider-jack-in-clj => C-c C-k main file

(defn log-scribe []
  (let [a (chan)                 ; Our channel A, the log's main door,
        p (pub a identity)       ; A publisher to manage more,
        _ (go (loop []           ; Our logging loop, in async trance,
                (when-let [msg (<! a)] ; Waits for messages to chance.
                  (println "Logging:" msg) ; Logs the message, clear and bright,
                  (recur))))] ; Repeats this pattern through the night.
    a))

(defn log-listener [a]
  (let [b (chan)]                               ; Channel B, to hear and see,
    (sub (pub a identity) :log b)               ; Subscribes to A, in quiet glee.
    (go (loop []                                ; Looping through the async stream,
           (when-let [msg (<! b)]               ; Grabs the logs like in a dream.
             (println "Listener:" msg)          ; Prints each log with careful prose,
             (recur))))                         ; And back again, in endless rows.
    b))

(defn main []
  (let [a (log-scribe)                          ; Call the scribe to start the play,
        b (log-listener a)]                     ; Listener joins without delay.
    (>!! a "First log message")                 ; Write some logs to channel A,
    (>!! a "Second log message")                ; See them printed, clear as day.
    (Thread/sleep 1000)                         ; A short pause to let them show,
    (close! a)                                  ; Then close A, and end the flow.
    (close! b)))                                ; And B as well, for the curtain call.


(comment

  (def a (log-scribe))
  (def b (log-listener a))

  (>!! a "First log message") ;; => "Logging: First log message"

  (>!! a "Second log message")          ;;=> Logging: Second log message

  )
