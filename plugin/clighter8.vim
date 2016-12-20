if exists('g:loaded_clighter8')
    finish
endif

let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\'   )

fun! ClFormat()
    if !executable(g:clang_format_path)
        return
    endif

    if v:count == 0
        let l:lines='all'
    else
        let l:lines=printf('%s:%s', v:lnum, v:lnum+v:count-1)
    endif

    execute('pyf '.s:script_folder_path.'/../third_party/clang-format.py')
endf

command! ClStart call clighter8#start()
command! ClStop call clighter8#stop()
command! ClRestart call clighter8#stop() | call clighter8#start()
command! ClLoadCdb call clighter8#start() | call clighter8#load_cdb()

let g:clighter8_autostart = get(g:, 'clighter8_autostart', 1)
let g:clighter8_libclang_path = get(g:, 'clighter8_libclang_path', '')
let g:clighter8_usage_priority = get(g:, 'clighter8_usage_priority', -1)
let g:clighter8_syntax_priority = get(g:, 'clighter8_syntax_priority', -2)
let g:clighter8_highlight_blacklist = get(g:, 'clighter8_highlight_blacklist', [])
let g:clighter8_highlight_whitelist = get(g:, 'clighter8_highlight_whitelist', [])
let g:clighter8_global_compile_args = get(g:, 'clighter8_global_compile_args', ['-x', 'c++', '-resource-dir=/usr/lib/llvm-3.9/lib/clang/3.9.0/'])
let g:clighter8_logfile = get(g:, 'clighter8_logfile', '/tmp/clighter8.log')
let g:clighter8_auto_gtags = get(g:, 'clighter8_auto_gtags', 1)
let g:clighter8_syntax_highlight = get(g:, 'clighter8_syntax_highlight', 1)
let g:clighter8_format_on_save = get(g:, 'clighter8_format_on_save', 0)
let g:clang_format_path = get(g:, 'clang_format_path', 'clang-format-3.9')


if g:clighter8_autostart
    au Filetype c,cpp call clighter8#start()
endif

let g:loaded_clighter8=1
