let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\'   )
execute('source '. s:script_folder_path . '/../syntax/clighter8.vim')

let s:parse_busy=0
let s:need_parse=0
let s:hlt_busy=0
let s:need_hlt=0
let s:enable=0
let s:hlt_timer=0
let s:parse_timer=0

fun! clighter8#start()
    if exists('s:channel')
        return
    endif

    let s:channel = ch_open('localhost:8787')
    if ch_status(s:channel) ==# 'fail'
        let l:cmd = 'python2 '. s:script_folder_path.'/../python/engine.py '. g:clighter8_logfile
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

    call s:toggle_highlight()
    call s:sched_parse()

    command! ClShowCursorInfo if exists ('s:channel') | echo clighter8#engine#cursor_info(s:channel, expand('%:p'), getpos('.')[1], getpos('.')[2]) | endif
    command! ClShowCompileInfo if exists ('s:channel') | echo clighter8#engine#compile_info(s:channel, expand('%:p')) | endif
    command! ClEnableLog if exists ('s:channel') | call clighter8#engine#enable_log(s:channel, v:true) | endif
    command! ClDisableLog if exists ('s:channel') | call clighter8#engine#enable_log(s:channel, v:false) | endif
    command! ClToggleHighlight if exists ('s:channel') | call s:toggle_highlight() | endif
endf

fun! clighter8#stop()
    augroup Clighter8
        autocmd!
    augroup END

    call timer_stop(s:parse_timer)
    call timer_stop(s:hlt_timer)

    if exists('s:channel') && ch_status(s:channel) ==# 'open'
        call ch_close(s:channel)
        unlet s:channel
    endif

    let l:wnr = winnr()
    windo call s:clear_matches([g:clighter8_usage_priority, g:clighter8_syntax_priority])
    exe l:wnr.'wincmd w'

    silent! delc ClShowCursorInfo
    silent! delc ClShowCompileInfo
    silent! delc ClEnableLog
    silent! delc ClDisableLog
    silent! delc ClRenameCursor
    silent! delc ClToggleHighlight
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

    let l:extra_inc = []
    echohl MoreMsg
    for bufname in l:cdb_files
        execute('silent! e! '. bufname)

        if index(['c', 'cpp'], &filetype) == -1
            continue
        endif

        let l:count += 1
        let l:percent = 100.0 * l:count / l:all

        if l:percent >= l:chk
            redraw | echo '[clighter8] loading compilation database...' . float2nr(l:percent) . '%'
            let l:chk = l:percent + 10
        endif
    endfor
    echohl None

    if !empty(l:extra_inc)
        execute('n! ' . join(l:extra_inc, ' '))
    endif
endf

fun! s:toggle_highlight()
    augroup Clighter8Highlight
        autocmd!
        let s:enable = !s:enable
        if s:enable == 1
            call s:sched_parse()

            au BufEnter,TextChanged,TextChangedI * call s:timer_parse()
            au BufEnter * call s:clear_matches([g:clighter8_usage_priority, g:clighter8_syntax_priority])
            "au BufDelete * call clighter8#engine#delete_buffer(s:channel, expand('%:p'))
            au VimLeave * call clighter8#stop()
            au CursorHold,CursorHoldI * call s:sched_highlight()
        else
            let l:wnr = winnr()
            windo call s:clear_matches([g:clighter8_usage_priority, g:clighter8_syntax_priority])
            exe l:wnr.'wincmd w'
        endif
    augroup END
endf

func s:render(matches)
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

fun! s:clear_matches(priorities)
    for m in getmatches()
        if index(a:priorities, m['priority']) >= 0
            call matchdelete(m['id'])
        endif
    endfor
endf

func! s:timer_parse()
    if index(['c', 'cpp'], &filetype) == -1
        return
    endif

    call timer_stop(s:parse_timer)

    if !exists('s:channel')
        return
    endif

    let s:parse_timer = timer_start(500, {->s:sched_parse()})
endf

fun! s:sched_parse()
    if index(['c', 'cpp'], &filetype) == -1
        return
    endif

    if s:parse_busy == 0
        let s:parse_busy=1
        call clighter8#engine#parse_async(s:channel, expand('%:p'), join(getbufline(expand('%:p'), 1,'$'), "\n"), {channel, msg->s:on_parse(channel, msg)})
    else
        let s:need_parse=1
    endif
endf

func s:on_parse(channel, msg)
    let s:parse_busy=0
    if !empty(a:msg)
        if a:msg['bufname'] == expand('%:p')
            call s:sched_highlight()
        endif
    endif

    if s:need_parse == 1
        let s:need_parse=0
        call s:sched_parse()
    endif
endfunc

fun s:timer_highlight(bufname)
    if index(['c', 'cpp'], &filetype) == -1
        return
    endif

    call timer_stop(s:hlt_timer)

    if !exists('s:channel')
        return
    endif

    let s:hlt_timer = timer_start(500, {->s:sched_highlight()})
endf

fun! s:sched_highlight()
    if index(['c', 'cpp'], &filetype) == -1
        return
    endif

    if s:hlt_busy == 0
        let s:hlt_busy=1
        call clighter8#engine#highlight_async(s:channel, expand('%:p'), line('w0'), line('w$'), line('.'), col('.'), s:get_word(), {channel, msg->s:on_highlight(channel, msg)})
    else
        let s:need_hlt=1
    endif
endf

func s:on_highlight(channel, msg)
    let s:hlt_busy=0

    if a:msg['bufname'] != expand('%:p')
        return
    endif

    if empty(a:msg)
        return
    endif
    
    call s:clear_matches([g:clighter8_syntax_priority, g:clighter8_usage_priority])
    call s:render(a:msg['hlt'])

    if s:need_hlt == 1 
        let s:need_hlt=0
        call s:sched_highlight()
    endif
endfunc
