# SoupScript

Welcome to the worst programming language you have ever laid your eyes on.

I largely followed [this guide](https://austinhenley.com/blog/teenytinycompiler1.html) to make this monstrosity.

Obviously I won't be maintaining this project, unless I get bored. This was mostly for my own educational purposes rather than any sort of desire to popularise the language.

## How to compile SoupScript

Simply running `compile.bat` will make an `a.exe` file from the `source.soup` file by default. Running in command prompt lets you specify different files, like so: `compile.bat input_file.soup output_file.exe`. The compiler uses the python and clang commands, so if you don't have either of these, it won't work correctly. You can change the file to use another C compiler if you prefer. For me `python` is the command for python, but I have read that for others it may be `python3` so keep that in mind as well. If the compiler doesn't work for whatever reason, you can manually compile just by running compile.py, and then using clang or another C compiler to compile the out.c file it creates.

## Explanation of files

`a.exe` is the executable for Windows for my example program.

`compile.bat` is the full compiler, which will only run on Windows (unless there is another OS I'm not aware of that supports batch files).

`compile.py` is the SoupScript part of the compiler. It compiles SoupScript into C. This will run on any computer with python 3 installed I believe.

`lex.py` is the lexer. This basically looks for keywords in the SoupScript code

`parse.py` is the parser. This takes the keywords from the lexer and makes sure everything is in the right order and then converts it to C. Only supports integers.

`emit.py` is the emitter. All this does is put the C code in a file.

`parsefloat.py` is the same as `parse.py`, but while `parse.py` only supports integers, this only supports floats (although you can use them like normal integers where possible in C)

`source.c` is the output of the compiler when compiling `source.soup`. The compiler actually creates a file called `out.c` but since this is immediately deleted once it is done compiling, I have decided to include the output in another file.

`source.jar` and `source.java` I have decided to include to show how I have previously programmed this same program in Java some months ago. They are not necessary for the compiler.

`source.soup` is the code I have written to demonstrate SoupScript. It takes an integer and checks if it is a prime number or not.

`source-unformatted.soup` is the same as `source.soup` but with all formatting removed, to show the periods are unnecessary and everything can be written on a single line.

## Explanation of the language

```
|text| --> /* Comment */, there is no // equivalent.
. --> Used for formatting, just pretend these are tabs and spaces. Don't even think about replacing them with spaces or forgetting one. When at the end of a line, a linebreak can be used.
, --> Negates a prior keyword, used for b, p. Also used to mark the end of a variable.
+-/* --> Same as in other languages.
% --> Same as in other languages, doesn't work with floats/`parsefloat.py`.
%% --> Like scanf in C, but much more basic.
b --> =, because "b" makes way more sense than "=". Just a normal b when followed by a comma (the compiler accounts for this when compiling to C).
p --> print, does not automatically print newlines, but \n can be used. Just a normal p when followed by a comma.
> and < --> Same as in other languages.
? --> starts if statement.
& --> starts while statement.
; --> ends print, while, if (like '}' and ')').
!< and !> --> >= and <= respectively, because "not greater than" makes more sense than "less than or equal to".
!! --> starts print, while, if (like '{' and '(').
0 --> marks the start of a number. Double 0 to get a normal 0. There is no technical reason why numbers need to be like this, I just felt like doing it this way. Can add a '.' to make it a normal float (this probably breaks parse.py, haven't tested it). If a '.' is not immediately followed by a number it works like an integer.
letters, numbers, space, tab, newline --> marks the start of a variable (I am aware this is an awful idea, I haven't implemented any way to convert variables starting with unusual characters into C, so this will probably break.
«text» --> "String", because using «» is much cooler.
```

## SoupScript Syntax

obviously I can't write down every single possibility, but to demonstrate some syntax here are some examples.
SoupScript on the left, C in the middle, Python on the right.

if statement: `?b,ar,=010!!foo,bb,ar,;` or:
```
?b,ar,=010!!.         if (bar == 10) {          if bar == 10:
....foo,bb,ar,.           foo = bar;                foo = bar
;.                    }                     
```

while statement: `&b,ar,!<010!!foo,bfoo,+01;` or:
```
&b,ar,!<010!!.        while (bar >= 10) {       while bar >= 10:
....foo,bfoo,+01.           foo = foo + 1;            foo = foo + 1
;.                    }                     
```

hello world: `p!!«Hello world!»;` or:
```
p!!«Hello world!»;.   printf("Hello world!");   print("Hello world!")
```

get input: `%%number,` or:
```
%%number,.            scanf("%i", &number)      number = input()
```

I ran out of ideas of things to put here, so enjoy what you can.
