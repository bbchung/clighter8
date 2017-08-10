#! /usr/bin/python2

import logging
import json
import SocketServer as socketserver
import threading
import sys
import os
from threading import Timer

# sys.path.append(
# os.path.dirname(
# os.path.realpath(__file__)) +
# "/../third_party")


class BufferData:

    def __init__(self):
        self.tu = None
        self.compile_args = None


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
            except Exception as e:
                logging.warn(str(e))
                break

            # print("received: {0}{1}".format(data, len(data)))
            if not data:
                break

            if remain:
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
        except Exception as e:
            logging.warn(str(e))

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
            except Exception as e:
                logging.warn(str(e))

            result = self.__init(
                cwd, global_compile_args, whitelist, blacklist)
            self.__safe_sendall(json.dumps([sn, result]))

        elif msg['cmd'] == 'parse':
            bufname = msg['params']['bufname']
            content = msg['params']['content']

            if not bufname:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            bufname = bufname.encode('utf-8')

            if content:
                self.__update_unsaved(bufname, content.encode('utf-8'))

            if not self.__parse(bufname):
                self.__safe_sendall(json.dumps([sn, None]))
                return

            includes = clighter8_helper.get_cwd_includes(
                self.buffer_data[bufname].tu, self.cwd)
            self.__update_inc_compile_args(
                includes, self.buffer_data[bufname].compile_args)

            self.__safe_sendall(json.dumps(
                [sn, {'bufname': bufname}]))

        elif msg['cmd'] == 'highlight':
            bufname = msg['params']['bufname']
            begin_line = msg['params']['begin_line']
            end_line = msg['params']['end_line']
            row = msg['params']['row']
            col = msg['params']['col']
            word = msg['params']['word']

            if not bufname:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            bufname = bufname.encode('utf-8')

            hlt = self.__highlight(
                bufname, begin_line, end_line, row, col, word)

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
            word = msg['params']['word']

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

            if not symbol or word != symbol.spelling:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            self.__safe_sendall(json.dumps(
                [sn, [symbol.spelling, symbol.get_usr()]]))


        elif msg['cmd'] == 'cursor_info':
            bufname = msg['params']['bufname']
            row = msg['params']['row']
            col = msg['params']['col']

            if not bufname:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            bufname = bufname.encode('utf-8')

            bufdata = self.buffer_data.get(bufname)
            if not bufdata:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            tu = bufdata.tu
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

            bufdata = self.buffer_data.get(bufname)
            if not bufdata:
                self.__safe_sendall(json.dumps([sn, None]))
                return

            result = bufdata.compile_args
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

            for cmd in cmds:
                result.add(os.path.join(cmd.directory, cmd.filename))

            self.__safe_sendall(json.dumps([sn, list(result)]))

    def __delete_buffer_data(self, bufname):
        if bufname in self.buffer_data:
            del self.buffer_data[bufname]

    def __init(self, cwd, global_compile_args, whitelist, blacklist):
        try:
            self.idx = cindex.Index.create()
        except Exception as e:
            logging.error(str(e))
            return False

        try:
            self.cdb = cindex.CompilationDatabase.fromDirectory(cwd)
        except cindex.CompilationDatabaseError:
            logging.info('compilation data is not found in ' + cwd)
        except Exception as e:
            logging.warn(str(e))

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
            self.buffer_data[bufname].compile_args = self.global_compile_args + \
                clighter8_helper.get_compile_args_from_cdb(self.cdb, bufname)

        try:
            if self.buffer_data[bufname].tu:
                self.buffer_data[bufname].tu.reparse(
                    self.unsaved,
                    0x01 | 0x04 | 0x100 | 0x200 | 0x2)
            else:
                self.buffer_data[bufname].tu = self.idx.parse(
                    bufname,
                    self.buffer_data[bufname].compile_args,
                    self.unsaved,
                    0x01 | 0x04 | 0x100 | 0x200 | 0x2)

            return True
        except Exception as e:
            del self.buffer_data[bufname]
            logging.warn(str(e))
            return False

    def __update_inc_compile_args(self, includes, args):
        for bufname in includes:
            if bufname not in self.buffer_data:
                self.buffer_data[bufname] = BufferData()

            self.buffer_data[bufname].compile_args = args

    def __highlight(self, bufname, begin_line, end_line, row, col, word):
        if bufname not in self.buffer_data:
            return {}

        tu = self.buffer_data[bufname].tu
        if not tu:
            return {}

        symbol = clighter8_helper.get_semantic_symbol_from_location(
            tu, bufname, row, col)

        if symbol and word != symbol.spelling:
            symbol = None

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

            # cursor = clighter8_helper.get_cursor(
                # tu, bufname, token.location.line, token.location.column)

            cursor = token.cursor
            cursor._tu = tu

            pos = [
                token.location.line, token.location.column, len(
                    token.spelling)]
            group = clighter8_helper.get_hlt_group(
                cursor.kind, self.whitelist, self.blacklist)

            if group:
                if group not in result:
                    result[group] = []

                result[group].append(pos)

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

    try:
        from clang import cindex
    except ImportError as e:
        logging.error(str(e))
        sys.exit(1)

    import clighter8_helper

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
