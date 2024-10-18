# You name it

This is SHA-256 hash value of a phrase `"you name it"`, typed in hex characters set:
> 2b0aeafda2a056cd4d48628c1cb5405897698c1ca924a04e57d8ab0948a8b4a3

Imagine, could you ever say?

> Yes, I've seen this hash before.

Probably not. Hashes for human brains are extremely hard to memorize.


But `you name it` is a python package that translates data into a pseudo-random word. 
Those are readable and memorable words that mean rather nothing.

Our brains are much better in remembering words, even the
weirdest ones. When run multiple times with the same data, it will return the same name each time,
on each python interpreter, on different machines. You can expect strict reproduction of the
translation results.

This package converts the object you provide into bytes, then feeds `sha` algorithm with it. The input data can be anything complex that can be converted to `bytes` object.


