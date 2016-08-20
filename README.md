# Clighter8: Vim8 plugin to highlight C-family code

## Intro

Clighter8 is a vim plugin to support C-family code powered by libclang.
Currently it can highlight and rename-refactor code semantically. Clighter8's
engine takes the advantage of vim8's new async architecture, and it is highly
optimized, so it runs very fast, user will not feel any laggy.

## Requirements

clighter8 requires the following:

* Vim8
* libclang, http://llvm.org/apt/

## Installation

use vim plugin manager, for example

* Vundle Install:
```vim
Bundle 'bbchung/clighter8'
```

## Options

### g:clighter8_autostart

Start Clighter8 automatically.

Default: `1`
```vim
let g:clighter8_autostart = 0
```

### g:clighter8_libclang_path

Config the libclang path if libclang is not in default path or Clighter8 can't
find it.

Default: `''`
```vim
let g:clighter8_libclang_file = '/usr/lib/libclang.so'
```

### g:clighter8_highlight_blacklist

Define the group of syntax NOT to be highlighted.

Default: `['clighter8InclusionDirective']`

The recommend setting to not be dazzled:
```vim
let g:clighter8_highlight_blacklist = ['clighter8NamespaceRef', 'clighter8FunctionDecl', 'clighter8FieldDecl', 'clighter8DeclRefExprCall', 'clighter8MemberRefExprCall', 'clighter8MemberRefExprVar', 'clighter8Namespace', 'clighter8NamespaceRef', 'cligherInclusionDirective', 'clighter8VarDecl']
```

### g:clighter8_heuristic_compile_args

Clighter8 search the compilation database to compile, but the compilation
database the CMake generated doesn't include the header files. Clighter8 can
heuristic search the compilation database to guess the most possible compile
args if set this option.

Default: `1`
```vim
let g:clighter8_heuristic_compile_args = 1
```

### g:clighter8_compile_args

The global compile args of Clighter8.

Default: `[]`
```vim
let g:clighter8_compile_args = []
```

## Commands and Functions

Clighter8 provides these commands and functions.

### StartClighter8

### StopClighter8

### Rename()

* An experimental function to do rename-refactor.
* The scope is opened vim buffers.
* There is no one-step undo/redo method.
* Strongly recommend that backing up all files before calling this function.
* For convenience, you can add key mapping in your vimrc:
```vim
nmap <silent> <Leader>r :call Rename()<CR>
```

## Compilation Database

Clighter8 automatically load and parse the compilation database
"compile_commands.json" if it exists in current working directory, then the
compile options will be passed to libclang. For more information about
compilation database, please reference [Compilation Database][cdb].

## Highlight Group

Clighter8 defines these highlight groups corresponded to libclang.

```vim
hi default link clighter8Prepro PreProc
hi default link clighter8Decl Identifier
hi default link clighter8Ref Type
hi default link clighter8InclusionDirective cIncluded
hi default link clighter8MacroInstantiation Constant
hi default link clighter8VarDecl Identifier
hi default link clighter8StructDecl Identifier
hi default link clighter8UnionDecl Identifier
hi default link clighter8ClassDecl Identifier
hi default link clighter8EnumDecl Identifier
hi default link clighter8ParmDecl Identifier
hi default link clighter8FunctionDecl Identifier
hi default link clighter8FieldDecl Identifier
hi default link clighter8EnumConstantDecl Constant
hi default link clighter8DeclRefExprEnum Constant
hi default link clighter8DeclRefExprCall Type
hi default link clighter8MemberRefExprCall Type
hi default link clighter8MemberRefExprVar Type
hi default link clighter8TypeRef Type
hi default link clighter8Namespace Identifier
hi default link clighter8NamespaceRef Type
hi default link clighter8TemplateTypeParameter Identifier
hi default link clighter8TemplateNoneTypeParameter Identifier
hi default link clighter8TemplateRef Type
hi default link clighter8Occurrences IncSearch
```

You can customize these colors in your colorscheme, for example:
```vim
hi clighter8TypeRef term=NONE cterm=NONE ctermbg=232 ctermfg=255 gui=NONE
```
## FAQ

### Clighter8 doesn't work?
Check the Requirements and Installation.

### Why rename-refactor function is an experimental function?
Due to the character of c-family language, it's hard to do rename-refactor.
Clighter8 only search the current opened buffer to do rename-refactor and it
can't guarantee the correctness.

### How to set compile args?
Clighter8 set the compile args for each file with (g:clighter8_compile_args +
"compilation database"). Compile args will affect the correctness of highlight
and rename-refactor.

## LICENSE

This software is licensed under the [GPL v3 license][gpl].

Note: This license does not cover the files that come from the LLVM project.


[gpl]: http://www.gnu.org/copyleft/gpl.html
[ycm]: https://github.com/Valloric/YouCompleteMe
[cdb]: http://clang.llvm.org/docs/JSONCompilationDatabase.html
