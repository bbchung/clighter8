if exists('g:loaded_clighter8')
    finish
endif


let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\'   )

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
let g:clighter8_global_compile_args = get(g:, 'clighter8_global_compile_args', ['-x', 'c++', '-std=c++0x'])
let g:clighter8_logfile = get(g:, 'clighter8_logfile', '/tmp/clighter8.log')
let g:clighter8_syntax_highlight = get(g:, 'clighter8_syntax_highlight', 1)


if g:clighter8_autostart
    au Filetype c,cpp call clighter8#start()
endif

let g:loaded_clighter8=1
