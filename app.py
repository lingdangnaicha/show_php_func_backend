from flask import Flask, request, Response
import sqlite3
import json

from flask_cors import cross_origin

app = Flask(__name__)
conn = sqlite3.connect("./php_func.db", check_same_thread=False)
cursor = conn.cursor()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/getData', methods=['GET'])
@cross_origin(origins='*', methods='GET', max_age=64000)
def get_data():
    try:
        where = get('where').upper()
        like = get('like')
        offset = int(get('offset'))
        if where not in ['FUNC_NAME', 'VER_INFO', 'FUNC_PURPOSE', 'HTML_LINK', 'FUNC_USAGE', 'FUNC_WARNING', 'FUNC_NOTE', 'FUNC_CHANGE_LOG']:
            return Response(_(403, f"where must be column name."), mimetype='application/json')
        if "\"" in like:
            return Response(_(403, f"like err."), mimetype='application/json')
        sql = f"select * from PHP where {where} like \"%{like}%\" limit {str(offset)}, 20"
        info = cursor.execute(sql)
        format_info = []
        headers = [comlun[0] for comlun in info.description]
        for line in info:
            format_info.append(dict(zip(headers, line)))
        return Response(_(200, format_info), mimetype='application/json')
    except Exception as e:
        return Response(_(500, f"Err: {e}"), mimetype='application/json')


def get(string, defalut_info=None):
    if defalut_info is None:
        defalut_info = {'where': 'FUNC_NAME', 'like': '', 'offset': 0}
    tmp = request.args.get(string)
    if tmp and isinstance(tmp, str):
        return tmp
    else:
        return defalut_info[string]


def _(status_code, info):
    return json.dumps({"code": status_code, "info": info})


if __name__ == '__main__':
    app.run()
