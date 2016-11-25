import logging
import json
import SocketServer as socketserver
import threading
import sys
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
                data, self.handle_json)

        self.request.close()

        server.remove_client(self.request)

    def handle_json(self, json_str):
        try:
            decoded = json.loads(json_str)
        except ValueError:
            logging.warn('json decoding failed')
            return

        if decoded[0] >= 0:
            self.handle_msg(decoded[0], decoded[1])

    def safe_sendall(self, msg):
        try:
            self.request.sendall(msg)
        except:
            logging.warn('socket send error')
            pass

    def handle_msg(self, sn, msg):
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

            succ = self.init(cwd, global_compile_args, whitelist, blacklist)
            self.safe_sendall(json.dumps([sn, succ]))

        elif msg['cmd'] == 'parse':
            bufname = msg['params']['bufname'].encode("utf-8")
            content = msg['params']['content'].encode("utf-8")

            if not bufname:
                self.safe_sendall(json.dumps([sn, '']))
                return

            self.update_unsaved(bufname, content)
            self.parse(bufname)

            self.safe_sendall(json.dumps([sn, bufname]))

        elif msg['cmd'] == 'req_parse':
            bufname = msg['params']['bufname'].encode("utf-8")
            if self.is_parse_busy(bufname):
                self.safe_sendall(json.dumps([sn, ""]))
                return

            self.set_parse_busy(bufname)
            self.safe_sendall(json.dumps([sn, bufname]))

        elif msg['cmd'] == 'req_get_hlt':
            bufname = msg['params']['bufname'].encode("utf-8")

            if self.is_hlt_busy(bufname):
                self.safe_sendall(json.dumps([sn, ""]))
                return

            self.set_hlt_busy(bufname)
            self.safe_sendall(json.dumps([sn, bufname]))

        elif msg['cmd'] == 'get_hlt':
            bufname = msg['params']['bufname'].encode("utf-8")
            begin_line = msg['params']['begin_line']
            end_line = msg['params']['end_line']
            row = msg['params']['row']
            col = msg['params']['col']

            self.unset_hlt_busy(bufname)
            hlt = self.get_hlt(
                bufname, begin_line, end_line, row, col)

            result = {'bufname': bufname, 'hlt': hlt}
            self.safe_sendall(json.dumps(
                [sn, result]))

        elif msg['cmd'] == 'delete_buffer':
            bufname = msg['params']['bufname'].encode("utf-8")
            self.delete_buffer_data(bufname)

        elif msg['cmd'] == 'get_usr_info':
            bufname = msg['params']['bufname'].encode("utf-8")
            row = msg['params']['row']
            col = msg['params']['col']

            ctx = self.get_buffer_data(bufname)
            if not ctx or not ctx.tu:
                self.safe_sendall(json.dumps([sn, '']))
                return

            symbol = clighter8_helper.get_semantic_symbol_from_location(
                ctx.tu, bufname, row, col)

            if not symbol:
                self.safe_sendall(json.dumps([sn, '']))
                return

            self.safe_sendall(json.dumps(
                [sn, [symbol.spelling, symbol.get_usr()]]))

        elif msg['cmd'] == 'rename':
            bufname = msg['params']['bufname'].encode("utf-8")
            usr = msg['params']['usr']

            buffer_data = self.get_buffer_data(bufname)
            if not buffer_data:
                self.safe_sendall(json.dumps([sn, None]))
                return

            usage = []
            clighter8_helper.search_by_usr(self.get_buffer_data(
                bufname).tu, usr, usage)

            self.safe_sendall(json.dumps([sn, usage]))

        elif msg['cmd'] == 'cursor_info':
            bufname = msg['params']['bufname'].encode("utf-8")
            row = msg['params']['row']
            col = msg['params']['col']

            tu = self.get_buffer_data(bufname).tu
            cursor = clighter8_helper.get_cursor(tu, bufname, row, col)

            if not cursor:
                self.safe_sendall(json.dumps([sn, None]))
                return

            result = {
                'cursor': str(cursor), 'cursor.kind': str(
                    cursor.kind), 'cursor.type.kind': str(
                    cursor.type.kind), 'cursor.spelling': cursor.spelling, 'location': [
                    cursor.location.line, cursor.location.column]}
            self.safe_sendall(json.dumps([sn, result]))

        elif msg['cmd'] == 'compile_info':
            bufname = msg['params']['bufname'].encode("utf-8")

            result = self.get_buffer_data(
                bufname).compile_args + self.global_compile_args
            self.safe_sendall(json.dumps([sn, result]))

        elif msg['cmd'] == 'enable_log':
            enable = msg['params']['enable']
            if enable:
                logging.disable(logging.NOTSET)
            else:
                logging.disable(logging.CRITICAL)

            self.safe_sendall(json.dumps([sn, True]))

    def get_buffer_data(self, bufname):
        if bufname in self.buffer_data:
            return self.buffer_data[bufname]

        return None

    def delete_buffer_data(self, bufname):
        if bufname in self.buffer_data:
            del self.buffer_data[bufname]

    def set_parse_busy(self, bufname):
        if bufname in self.buffer_data:
            self.buffer_data[bufname].parse_busy = True

    def is_parse_busy(self, bufname):
        if bufname in self.buffer_data:
            return self.buffer_data[bufname].parse_busy

        return False

    def set_hlt_busy(self, bufname):
        if bufname in self.buffer_data:
            self.buffer_data[bufname].hlt_busy = True

    def unset_hlt_busy(self, bufname):
        if bufname in self.buffer_data:
            self.buffer_data[bufname].hlt_busy = False

    def is_hlt_busy(self, bufname):
        if bufname in self.buffer_data:
            return self.buffer_data[bufname].hlt_busy

        return False

    def init(self, cwd, global_compile_args, whitelist, blacklist):
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

        return True

    def update_unsaved(self, bufname, content):
        for item in self.unsaved:
            if item[0] == bufname:
                self.unsaved.remove(item)

        self.unsaved.append((bufname, content))

    def parse(self, bufname):
        if bufname not in self.buffer_data:
            self.buffer_data[bufname] = BufferData()
            self.buffer_data[bufname].compile_args = clighter8_helper.get_compile_args_from_cdb(
                self.cdb, bufname)

        compile_args = self.buffer_data[
            bufname].compile_args + self.global_compile_args

        self.buffer_data[bufname].parse_busy = False

        try:
            if self.buffer_data[bufname].tu:
                self.buffer_data[bufname].tu.reparse(
                    self.unsaved,
                    cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
            else:
                self.buffer_data[bufname].tu = self.idx.parse(
                    bufname,
                    compile_args,
                    self.unsaved,
                    options=cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
        except:
            del self.buffer_data[bufname]
            logging.warn('libclang failed to parse', bufname)
            return

        for i in self.buffer_data[bufname].tu.get_includes():
            if i.is_input_file:
                continue

            if i.include not in self.buffer_data:
                self.buffer_data[
                    i.include.name] = BufferData()

            self.buffer_data[i.include.name].compile_args = self.buffer_data[
                bufname].compile_args

    def get_hlt(self, bufname, begin_line, end_line, row, col):
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
                self.__timer = Timer(10, self.shutdown_if_need)
                self.__timer.start()

    def shutdown_if_need(self):
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
