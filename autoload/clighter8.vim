let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\'   )
execute('source '. s:script_folder_path . '/../syntax/clighter8.vim')
execute('source '. s:script_folder_path . '/../third_party/gtags.vim')

fun! clighter8#start()
    if exists('s:channel')
        return
    endif

    let s:channel = ch_open('localhost:8787')
    if ch_status(s:channel) ==# 'fail'
        let l:cmd = 'python '. s:script_folder_path.'/../python/engine.py '. g:clighter8_logfile
        let s:job = job_start(l:cmd, {'stoponexit': '', 'in_io': 'null', 'out_io': 'null', 'err_io': 'null'})
        let s:channel = ch_open('localhost:8787', {'waittime': 500})
        if ch_status(s:channel) ==# 'fail'
            echohl ErrorMsg | echo '[clighter8] failed start engine' | echohl None
            return
        endif
    endif

    let l:succ = clighter8#engine#init(s:channel, g:clighter8_libclang_path, g:clighter8_global_compile_args, getcwd(), g:clighter8_highlight_whitelist, g:clighter8_highlight_blacklist)

    if l:succ == v:false
        echohl ErrorMsg | echo '[clighter8] failed to init client' | echohl None
        call ch_close(s:channel)
        unlet s:channel
        return
    endif

    call s:req_parsecpp(expand('%:p'))

    if g:clighter8_auto_gtags == 1
        call s:update_gtags()
    endif

    augroup Clighter8
        autocmd!

        if g:clighter8_syntax_highlight == 1
            au BufEnter,TextChanged,TextChangedI * call s:on_textchanged(expand('%:p'))
            au BufEnter * call s:clear_matches([g:clighter8_usage_priority, g:clighter8_syntax_priority])
            au BufLeave * call s:req_parsecpp(expand('%:p'))
            au CursorMoved,CursorMovedI * call s:req_get_hlt(expand('%:p'))
            au BufDelete * call clighter8#engine#delete_buffer(s:channel, expand('%:p'))
            au VimLeave * call clighter8#stop()
        endif

        if g:clighter8_auto_gtags == 1
            au BufWritePost,BufEnter * call s:update_gtags()
        endif

        if g:clighter8_format_on_save == 1
            au BufWritePre * call clighter8#format()
        endif
    augroup END
endf

fun! clighter8#stop()
    augroup Clighter8
        autocmd!
    augroup END

    if exists('s:channel') && ch_status(s:channel) ==# 'open'
        call ch_close(s:channel)
        unlet s:channel
    endif

    let a:wnr = winnr()
    windo call s:clear_matches([g:clighter8_usage_priority, g:clighter8_syntax_priority])
    exe a:wnr.'wincmd w'
endf

fun s:req_parsecpp(bufname)
    if !exists('s:channel')
        return
    endif

    if index(['c', 'cpp'], &filetype) == -1
        return
    endif

    call clighter8#engine#req_parse_async(s:channel, a:bufname, {channel, msg->s:on_req_parse(channel, msg)})
endf

fun! clighter8#load_cdb()
    let l:cdb_files = clighter8#engine#get_cdb_files(s:channel)

    if empty(l:cdb_files)
        echohl WarningMsg | echo '[clighter8] no files to open' | echohl None
        return
    endif

    let l:all = len(l:cdb_files)
    let l:chk = 10
    let l:count = 0

    let l:incs = []
    echohl MoreMsg
    for bufname in l:cdb_files
        execute('silent! e! '. bufname)

        if index(['c', 'cpp'], &filetype) == -1
            continue
        endif

        let l:result = clighter8#engine#parse(s:channel, bufname, join(getbufline(bufname, 1,'$'), "\n"))
        if empty(l:result)
            continue
        endif

        let l:incs += l:result['includes']

        let l:count += 1
        let l:percent = 100.0 * l:count / l:all

        if l:percent >= l:chk
            redraw | echo '[clighter8] loading compilation database...' . float2nr(l:percent) . '%'
            let l:chk = l:percent + 10
        endif
    endfor
    echohl None

    if !empty(l:incs)
        execute('n! ' . join(l:incs, ' '))
    endif
endf

fun clighter8#rename(row, col)
    if index(['c', 'cpp'], &filetype) == -1
        return
    endif

    let l:bufname = expand('%:p')
    if empty(clighter8#engine#parse(s:channel, l:bufname, join(getbufline(l:bufname, 1,'$'), "\n")))
        echohl WarningMsg | echo '[clighter8] unable to rename' | echohl None
        return
    endif

    let l:usr_info = clighter8#engine#get_usr_info(s:channel, l:bufname, a:row, a:col, s:get_word())

    if empty(l:usr_info)
        echohl WarningMsg | echo '[clighter8] unable to rename' | echohl None
        return
    endif

    let [l:old, l:usr] = l:usr_info
    echohl Question | let l:new = input('Rename ' . l:old . ' to : ', l:old) | echohl None
    if (empty(l:new) || l:old ==# l:new)
        return
    endif

    let l:qflist = []
    let l:wnr = winnr()
    let l:bufnr = bufnr('%')
    let l:pos = getpos('.')

    let l:title = '[clighter8] rename "' . l:old . '" to "' . l:new. '"'
    let l:prompt = confirm(l:title . '?', "&Yes\n&All\n&No", 1)
    if (l:prompt == 3 || l:prompt == 0)
        return
    endif

    let l:start = reltime()

    let l:buffers = getbufinfo()
    let l:all = len(l:buffers)

    let l:count = 0
    let l:chk = 10
    echohl MoreMsg
    echo l:title. '... 0%'

    " to sort the buffers
    let l:sources = []
    let l:headers = []

    for info in l:buffers
        if s:is_header(info.name) == 1
            call add(l:headers, info)
        else
            call add(l:sources, info)
        endif
    endfor

    for info in l:sources + l:headers
        execute('silent! buffer! '. info.bufnr)

        if index(['c', 'cpp'], &filetype) == -1
            continue
        endif

        if empty(clighter8#engine#parse(s:channel, info.name, join(getbufline(info.name, 1,'$'), "\n")))
            continue
        endif

        let l:usage = clighter8#engine#rename(s:channel, info.name, l:usr)

        if empty(l:usage) 
            continue
        endif

        if (l:prompt == 1)
            let l:yn = confirm("rename '". l:old ."' to '" .l:new. "' in " .info.name. '?', "&Yes\n&No", 1)
            if (l:yn == 2 || l:yn == 0)
                continue
            endif
        endif

        silent! call s:replace(l:usage, l:old, l:new, l:qflist)

        call clighter8#engine#parse(s:channel, info.name, join(getbufline(info.name, 1,'$'), "\n"))

        let l:count += 1
        let l:percent = 100.0 * l:count / l:all

        if l:percent >= l:chk
            redraw | echo l:title. ' ...' . float2nr(l:percent) . '%'
            let l:chk = l:percent + 10
        endif
    endfor

    call setqflist(l:qflist)
    exe 'buffer! '.l:bufnr
    call setpos('.', l:pos)
    copen
    exe l:wnr.'wincmd w'

    if l:prompt == 2
        let l:seconds = reltimefloat(reltime(l:start))
        echo printf('[clighter8] time usage: %f seconds', l:seconds)
    endif

    echohl None
endf


func s:highlight(matches)
    for [group, all_pos] in items(a:matches)
        let l:count = 0
        let l:match8 = []
        let l:priority = (group ==# 'clighter8Usage') ? g:clighter8_usage_priority : g:clighter8_syntax_priority 

        for pos in all_pos
            call add(l:match8, pos)
            let l:count += 1
            if l:count == 8
                call matchaddpos(group, l:match8, l:priority)

                let l:count = 0
                let l:match8 = []
            endif
        endfor

        call matchaddpos(group, l:match8, l:priority)
    endfor
endf

fun! s:get_word()
    if match(getline('.')[col('.')-1] , '\w') == 0
        return expand("<cword>")
    else
        return ''
    endif
endf

fun! s:on_gtags_finish()
    if exists('s:gtags_need_update') && s:gtags_need_update == 1
        call s:update_gtags()
    endif
endf

fun! s:update_gtags()
    if &diff
        return
    endif

    if exists('s:gtags_job') && job_status(s:gtags_job) ==# 'run'
        let s:gtags_need_update = 1
    else
        let s:gtags_need_update = 0

        if filereadable('GPATH') && filereadable('GRTAGS') && filereadable('GTAGS')
            if executable('global')
                let s:gtags_need_update = 0
                let l:cmd = 'global -u --single-update="' . expand('%') . '"'
                let s:gtags_job = job_start(l:cmd, {'stoponexit': '', 'in_io': 'null', 'out_io': 'null', 'err_io': 'null', 'exit_cb' : {->s:on_gtags_finish()}})
            endif
        else
            if executable('gtags')
                let s:gtags_job = job_start('gtags', {'stoponexit': '', 'in_io': 'null', 'out_io': 'null', 'err_io': 'null', 'exit_cb' : {->s:on_gtags_finish()}})
            endif
        endif
    endif
endf

func s:on_parse(channel, msg)
    if empty(a:msg)
        return
    endif

    call s:clear_matches([g:clighter8_usage_priority])
    call clighter8#engine#req_get_hlt_async(a:channel, a:msg['bufname'], {channel, msg->s:on_req_get_hlt(channel, msg)})
endfunc

func s:on_req_parse(channel, msg)
    if empty(a:msg)
        return
    endif

    let l:content = v:null
    if bufloaded(a:msg)
        let l:content = join(getbufline(a:msg, 1,'$'), "\n")
    endif

    call clighter8#engine#parse_async(a:channel, a:msg, l:content, {channel, msg->s:on_parse(channel, msg)})
endfunc

func s:on_req_get_hlt(channel, msg)
    if empty(a:msg)
        return
    endif

    call clighter8#engine#get_hlt_async(a:channel, a:msg, line('w0'), line('w$'), line('.'), col('.'), s:get_word(), {channel, msg->s:on_get_hlt(channel, msg)})
endfunc

func s:on_get_hlt(channel, msg)
    if empty(a:msg)
        return
    endif

    if a:msg['bufname'] != expand('%:p')
        return
    endif

    call s:clear_matches([g:clighter8_syntax_priority, g:clighter8_usage_priority])
    call s:highlight(a:msg['hlt'])
endfunc


fun! s:replace(usage, old, new, qflist)
    let l:pattern = ''
    for [row, column] in a:usage
        if (!empty(l:pattern))
            let l:pattern = l:pattern . '\|'
        endif

        let l:pattern = l:pattern . '\%' . row . 'l' . '\%>' . (column - 1) . 'c\%<' . (column + strlen(a:old)) . 'c' . a:old
        call add(a:qflist, {'filename':bufname(''), 'bufnr':bufnr(''), 'lnum':row, 'col':column, 'type' : 'I', 'text':"'".a:old."' was renamed to '".a:new."'"})
    endfor

    let l:cmd = '%s/' . l:pattern . '/' . a:new . '/gI'

    execute(l:cmd)
endf

fun! s:clear_matches(priorities)
    for m in getmatches()
        if index(a:priorities, m['priority']) >= 0
            call matchdelete(m['id'])
        endif
    endfor
endf

fun! s:is_header(bufname)
    if empty(a:bufname)
        return ''
    endif

    let l:dot = -1
    let l:offset = 0
    let len = len(a:bufname)

    while l:offset < len
        if a:bufname[l:offset] ==# '.'
            let l:dot = l:offset
        endif

        let l:offset += 1
    endwhile

    if l:dot == -1 || l:dot == len(a:bufname) - 1
        return 0
    endif

    return a:bufname[l:dot + 1] ==? 'h'
endf

fun! s:on_timer(bufname)
    call s:req_parsecpp(a:bufname)
endf

func! s:on_textchanged(bufname)
    if index(['c', 'cpp'], &filetype) == -1
        return
    endif

    if exists('s:timer')
        call timer_stop(s:timer)
    endif

    let s:timer = timer_start(800, {timer->s:on_timer(a:bufname)})
endf

fun s:req_get_hlt(bufname)
    if !exists('s:channel')
        return
    endif

    if index(['c', 'cpp'], &filetype) == -1
        return
    endif

    call s:clear_matches([g:clighter8_usage_priority])
    call clighter8#engine#req_get_hlt_async(s:channel, a:bufname, {channel, msg->s:on_req_get_hlt(channel, msg)})
endf

fun! clighter8#format()
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


command! ClShowCursorInfo if exists ('s:channel') | echo clighter8#engine#cursor_info(s:channel, expand('%:p'), getpos('.')[1], getpos('.')[2]) | endif
command! ClShowCompileInfo if exists ('s:channel') | echo clighter8#engine#compile_info(s:channel, expand('%:p')) | endif
command! ClEnableLog if exists ('s:channel') | call clighter8#engine#enable_log(s:channel, v:true) | endif
command! ClDisableLog if exists ('s:channel') | call clighter8#engine#enable_log(s:channel, v:false) | endif
command! ClRenameCursor if exists ('s:channel') | call clighter8#rename(line('.'), col('.')) | endif

