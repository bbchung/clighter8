fun! clighter8#engine#init(channel, libclang_path, compile_args, cwd, hlt_whitelist, hlt_blacklist)
    let l:expr = {'cmd' : 'init', 'params' : {'libclang' : a:libclang_path, 'cwd' : a:cwd, 'global_compile_args' : a:compile_args, 'whitelist' : a:hlt_whitelist, 'blacklist' : a:hlt_blacklist}}
    return ch_evalexpr(a:channel, l:expr)
endf

fun! clighter8#engine#get_hlt_async(channel, bufname, begin, end, row, col, word, callback)
    let l:expr = {'cmd' : 'get_hlt', 'params' : {'bufname' : a:bufname, 'begin_line' : a:begin, 'end_line' : a:end, 'row' : a:row, 'col': a:col, 'word' : a:word}}
    call ch_sendexpr(a:channel, l:expr, {'callback': a:callback})
endf

func clighter8#engine#cursor_info(channel, bufname, row, col)
    let l:expr = {'cmd' : 'cursor_info', 'params' : {'bufname' : a:bufname, 'row' : a:row, 'col': a:col}}
    return ch_evalexpr(a:channel, l:expr)
endf

func clighter8#engine#compile_info(channel, bufname)
    let l:expr = {'cmd' : 'compile_info', 'params' : {'bufname' : a:bufname}}
    return ch_evalexpr(a:channel, l:expr)
endf

func clighter8#engine#req_parse_async(channel, bufname, callback)
    let l:expr = {'cmd' : 'req_parse', 'params' : {'bufname' : a:bufname}}
    call ch_sendexpr(a:channel, l:expr, {'callback': a:callback})
endf

func clighter8#engine#req_get_hlt_async(channel, bufname, callback)
    let l:expr = {'cmd' : 'req_get_hlt', 'params' : {'bufname' : a:bufname}}
    call ch_sendexpr(a:channel, l:expr, {'callback': a:callback})
endf

func clighter8#engine#parse_async(channel, bufname, content, callback)
    let l:expr = {'cmd' : 'parse', 'params' : {'bufname' : a:bufname, 'content' : a:content}}
    call ch_sendexpr(a:channel, l:expr, {'callback': a:callback})
endf

func clighter8#engine#parse(channel, bufname, content)
    let l:expr = {'cmd' : 'parse', 'params' : {'bufname' : a:bufname, 'content' : a:content}}
    return ch_evalexpr(a:channel, l:expr, {'timeout' : 10000})
endf

fun! clighter8#engine#delete_buffer(channel, bufname)
    let l:expr = {'cmd' : 'delete_buffer', 'params' : {'bufname' : a:bufname}}
    call ch_sendexpr(a:channel, l:expr)
endf

fun! clighter8#engine#enable_log(channel, en)
    let l:expr = {'cmd' : 'enable_log', 'params' : {'enable' : a:en}}
    call ch_sendexpr(a:channel, l:expr)
endf

fun! clighter8#engine#get_usr_info(channel, bufname, row, col, word)
    let l:expr = {'cmd' : 'get_usr_info', 'params' : {'bufname' : a:bufname, 'row' : a:row, 'col': a:col, 'word' : a:word}}
    return ch_evalexpr(a:channel, l:expr)
endf

fun! clighter8#engine#get_cdb_files(channel)
    let l:expr = {'cmd' : 'get_cdb_files', 'params' : {}}
    return ch_evalexpr(a:channel, l:expr, {'timeout' : 10000})
endf
