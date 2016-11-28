import logging
import json
import SocketServer as socketserver
import threading
import sys
import os
from threading import Timer


from clang import cindex
import clighter8_helper


class BufferData:

    def __init__(self):
        self.tu = None
        self.compile_args = None
        self.parse_busy = False
        self.hlt_busy = False


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_addres, server):
        self.buffer_data = {}
        self.unsaved = []
        self.cdb = None
        self.idx = None
        self.global_compile_args = None
        self.whitelist = []
        self.blacklist = []
        self.cwd = None

        socketserver.BaseRequestHandler.__init__(
            self, request, client_addres, server)

    def handle(self):
        remain = ''
        server.add_client(self.request)
        logging.info('accept a vim client')
        while True:
            try:
                data = self.request.recv(8192)
            except:
                logging.warn('socket recv error')
                break

            # print("received: {0}{1}".format(data, len(data)))
            if data == '':
                break

            if remain != '':
                data = remain + data

            remain = clighter8_helper.parse_line_delimited(
                data, self.__handle_json)

        self.request.close()

        server.remove_client(self.request)

    def __handle_json(self, json_str):
        try:
            decoded = json.loads(json_str)
        except ValueError:
            logging.warn('json decoding failed')
            return

        if decoded[0] >= 0:
            self.__handle_msg(decoded[0], decoded[1])

    def __safe_sendall(self, msg):
        try:
            self.request.sendall(msg)
        except:
            logging.warn('socket send error')
            pass

    def __handle_msg(self, sn, msg):
        if msg['cmd'] == 'init':
            libclang = msg["params"]["libclang"]
            cwd = msg["params"]["cwd"]
            global_compile_args = msg["params"]["global_compile_args"]
            whitelist = msg["params"]["whitelist"]
            blacklist = msg["params"]["blacklist"]

            try:
                cindex.Config.set_library_file(libclang)
                logging.info('config libclang path')
            except:
                logging.warn('cannot config library path')

            result = self.__init(
                cwd, global_compile_args, whitelist, blacklist)
            self.__safe_sendall(json.dumps([sn, result]))

        elif msg['cmd'] == 'parse':
            bufname = msg['params']['bufname']
            content = msg['params']['content']

            if not bufname or not content:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            bufname = bufname.encode('utf-8')
            content = content.encode('utf-8')

            self.__update_unsaved(bufname, content)
            self.__parse(bufname)
            self.__update_inc_compile_args(bufname, None)

            self.__safe_sendall(json.dumps([sn, bufname]))

        elif msg['cmd'] == 'req_parse':
            bufname = msg['params']['bufname']

            if not bufname:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            bufname = bufname.encode('utf-8')

            if self.__is_parse_busy(bufname):
                self.__safe_sendall(json.dumps([sn, None]))
                return

            self.__set_parse_busy(bufname)
            self.__safe_sendall(json.dumps([sn, bufname]))

        elif msg['cmd'] == 'req_get_hlt':
            bufname = msg['params']['bufname']

            if not bufname:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            bufname = bufname.encode('utf-8')

            if self.__is_hlt_busy(bufname):
                self.__safe_sendall(json.dumps([sn, None]))
                return

            self.__set_hlt_busy(bufname)
            self.__safe_sendall(json.dumps([sn, bufname]))

        elif msg['cmd'] == 'get_hlt':
            bufname = msg['params']['bufname']
            begin_line = msg['params']['begin_line']
            end_line = msg['params']['end_line']
            row = msg['params']['row']
            col = msg['params']['col']

            if not bufname:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            bufname = bufname.encode('utf-8')

            self.__unset_hlt_busy(bufname)
            hlt = self.__get_hlt(
                bufname, begin_line, end_line, row, col)

            result = {'bufname': bufname, 'hlt': hlt}
            self.__safe_sendall(json.dumps(
                [sn, result]))

        elif msg['cmd'] == 'delete_buffer':
            bufname = msg['params']['bufname']

            if not bufname:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            bufname = bufname.encode('utf-8')
            self.__delete_buffer_data(bufname)

            self.__safe_sendall(json.dumps([sn, bufname]))

        elif msg['cmd'] == 'get_usr_info':
            bufname = msg['params']['bufname']
            row = msg['params']['row']
            col = msg['params']['col']

            if not bufname:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            bufname = bufname.encode('utf-8')

            bfdata = self.buffer_data.get(bufname)
            if not bfdata or not bfdata.tu:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            symbol = clighter8_helper.get_semantic_symbol_from_location(
                bfdata.tu, bufname, row, col)

            if not symbol:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            self.__safe_sendall(json.dumps(
                [sn, [symbol.spelling, symbol.get_usr()]]))

        elif msg['cmd'] == 'rename':
            bufname = msg['params']['bufname']
            usr = msg['params']['usr']

            if not bufname:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            bufname = bufname.encode('utf-8')

            buffer_data = self.buffer_data.get(bufname)
            if not buffer_data:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            usage = []
            clighter8_helper.search_by_usr(
                self.buffer_data.get(bufname).tu, usr, usage)

            self.__safe_sendall(json.dumps([sn, usage]))

        elif msg['cmd'] == 'cursor_info':
            bufname = msg['params']['bufname']
            row = msg['params']['row']
            col = msg['params']['col']

            if not bufname:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            bufname = bufname.encode('utf-8')

            tu = self.buffer_data.get(bufname).tu
            cursor = clighter8_helper.get_cursor(tu, bufname, row, col)

            if not cursor:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            result = {
                'cursor': str(cursor), 'cursor.kind': str(
                    cursor.kind), 'cursor.type.kind': str(
                    cursor.type.kind), 'cursor.spelling': cursor.spelling, 'location': [
                    cursor.location.line, cursor.location.column]}
            self.__safe_sendall(json.dumps([sn, result]))

        elif msg['cmd'] == 'compile_info':
            bufname = msg['params']['bufname']

            if not bufname:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            bufname = bufname.encode('utf-8')

            result = self.buffer_data.get(bufname).compile_args
            self.__safe_sendall(json.dumps([sn, result]))

        elif msg['cmd'] == 'enable_log':
            enable = msg['params']['enable']

            if enable:
                logging.disable(logging.NOTSET)
            else:
                logging.disable(logging.CRITICAL)

            self.__safe_sendall(json.dumps([sn, enable]))

        elif msg['cmd'] == 'get_cdb_files':
            if not self.cdb:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            cmds = self.cdb.getAllCompileCommands()

            result = set()
            cdb_files = set()

            for cmd in cmds:
                cdb_files.add(os.path.join(cmd.directory, cmd.filename))

            result = result.union(cdb_files)

            for bufname in cdb_files:
                self.__parse(bufname)
                self.__update_inc_compile_args(bufname, result.add)

            self.__safe_sendall(json.dumps([sn, list(result)]))

    def __delete_buffer_data(self, bufname):
        if bufname in self.buffer_data:
            del self.buffer_data[bufname]

    def __set_parse_busy(self, bufname):
        if bufname in self.buffer_data:
            self.buffer_data[bufname].parse_busy = True

    def __is_parse_busy(self, bufname):
        if bufname in self.buffer_data:
            return self.buffer_data[bufname].parse_busy

        return False

    def __set_hlt_busy(self, bufname):
        if bufname in self.buffer_data:
            self.buffer_data[bufname].hlt_busy = True

    def __unset_hlt_busy(self, bufname):
        if bufname in self.buffer_data:
            self.buffer_data[bufname].hlt_busy = False

    def __is_hlt_busy(self, bufname):
        if bufname in self.buffer_data:
            return self.buffer_data[bufname].hlt_busy

        return False

    def __init(self, cwd, global_compile_args, whitelist, blacklist):
        try:
            self.idx = cindex.Index.create()
            self.cdb = cindex.CompilationDatabase.fromDirectory(cwd)
        except cindex.CompilationDatabaseError:
            logging.info('compilation data is not found in ' + cwd)
        except:
            return False

        self.global_compile_args = global_compile_args
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.cwd = cwd

        return True

    def __update_unsaved(self, bufname, content):
        for item in self.unsaved:
            if item[0] == bufname:
                self.unsaved.remove(item)

        self.unsaved.append((bufname, content))

    def __parse(self, bufname):
        if bufname not in self.buffer_data:
            self.buffer_data[bufname] = BufferData()
            self.buffer_data[bufname].compile_args = clighter8_helper.get_compile_args_from_cdb(
                self.cdb, bufname) + self.global_compile_args

        self.buffer_data[bufname].parse_busy = False

        try:
            if self.buffer_data[bufname].tu:
                self.buffer_data[bufname].tu.reparse(
                    self.unsaved,
                    cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD | 0x100 | 0x200 | 0x4)
            else:
                self.buffer_data[bufname].tu = self.idx.parse(
                    bufname,
                    self.buffer_data[bufname].compile_args,
                    self.unsaved,
                    cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD | 0x100 | 0x200 | 0x4)
        except:
            del self.buffer_data[bufname]
            logging.warn('libclang failed to parse', bufname)
            return

    def __update_inc_compile_args(self, bufname, on_update):
        if bufname not in self.buffer_data:
            return

        if not self.buffer_data[bufname].tu:
            return

        for i in self.buffer_data[bufname].tu.get_includes():
            if i.is_input_file:
                continue

            if not i.include.name.startswith(self.cwd):
                continue

            if i.include.name not in self.buffer_data:
                self.buffer_data[
                    i.include.name] = BufferData()

            if on_update:
                on_update(i.include.name)

            self.buffer_data[i.include.name].compile_args = self.buffer_data[
                bufname].compile_args

    def __get_hlt(self, bufname, begin_line, end_line, row, col):
        if bufname not in self.buffer_data:
            return {}

        tu = self.buffer_data[bufname].tu
        if not tu:
            return {}

        symbol = clighter8_helper.get_semantic_symbol_from_location(
            tu, bufname, row, col)

        tu_file = tu.get_file(bufname)

        if not tu_file:
            return {}

        begin = cindex.SourceLocation.from_position(
            tu, tu_file, line=begin_line, column=1)
        end = cindex.SourceLocation.from_position(
            tu, tu_file, line=end_line + 1, column=1)
        tokens = tu.get_tokens(
            extent=cindex.SourceRange.from_locations(begin, end))

        result = {}

        if symbol:
            result['clighter8Usage'] = []

        for token in tokens:
            if token.kind.value != 2:  # no keyword, comment
                continue

            cursor = token.cursor
            cursor._tu = tu

            pos = [
                token.location.line, token.location.column, len(
                    token.spelling)]
            group = clighter8_helper.get_hlt_group(
                cursor, self.whitelist, self.blacklist)

            if group:
                if group not in result:
                    result[group] = []

                result[group].append(pos)

            t_symbol = None
            t_symbol = clighter8_helper.get_semantic_symbol(cursor)

            if symbol and t_symbol and symbol == t_symbol and t_symbol.spelling == token.spelling:
                result['clighter8Usage'].append(pos)

        return result


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

    def __init__(self, addr, handler):
        self.__clients = set()
        self.__lock = threading.Lock()
        self.__timer = None

        self.allow_reuse_address = True

        socketserver.TCPServer.__init__(self, addr, handler)

    def add_client(self, cli):
        if self.__timer and self.__timer.isAlive():
            self.__timer.cancel()

        with self.__lock:
            self.__clients.add(cli)

    def remove_client(self, cli):
        with self.__lock:
            self.__clients.remove(cli)
            num_client = len(self.__clients)
            logging.info("a client has left(%d clients remains)" % num_client)

            if num_client == 0:
                logging.info(
                    'going to exit if there is no new client comes in 10 seconds')
                self.__timer = Timer(10, self.__shutdown_if_nocli)
                self.__timer.start()

    def __shutdown_if_nocli(self):
        num_client = len(self.__clients)
        if num_client > 0:
            return

        logging.info('server shutdown')
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    logfile = '/tmp/clighter8.log'
    if len(sys.argv) > 1:
        logfile = sys.argv[1]

    logging.basicConfig(
        filename=logfile,
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s')

    socketserver.TCPServer.allow_reuse_address = True
    HOST, PORT = "localhost", 8787
    try:
        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    except:
        logging.error("failed to start clighter8 server")
        exit()

    ip, port = server.server_address
    logging.info("server start at %s:%d" % (ip, port))
    server.serve_forever()
