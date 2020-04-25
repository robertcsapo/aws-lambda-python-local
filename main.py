from flask import Flask, request
from flask.json import jsonify
import os
import argparse
import json
import requests
from aws import context

'''     Unofficial AWS Lambda Python Local Service                  '''
'''     Flask as framework API Gateway                              '''
'''     Mockup AWS context                                          '''
'''     Your lambda_function importade in `lambda_function` file    '''

app = Flask(__name__)


''' AWS Lambda Function '''
@app.route("/", methods=["GET", "POST"])
def awsLambda():
    if request.method == "GET":
        result = {"success": "online"}
        return(jsonify(result))
    elif request.method == "POST":
        data = lambda_function.lambda_handler(
            json.loads(request.data), context
            )
        return(jsonify(data))
    else:
        result = {"error": "wrong method"}
        return(jsonify(result))


''' Information about the host '''
@app.route("/host", methods=["GET"])
def host():
    if request.method == "GET":
        result = {}

        ''' Local Server '''
        server = {}
        server["hostname"] = os.environ["HOSTNAME"]
        server["python_version"] = os.environ["PYTHON_VERSION"]
        server["path"] = os.environ["PATH"]
        server["pwd"] = os.getcwd()
        server["ipaddr"] = []
        ipaddrs = str(os.popen("ip addr | egrep inet | grep -v 'host lo' | awk '{print $2}'").read()).rstrip()
        for ipaddr in ipaddrs.splitlines():
            server["ipaddr"].append(ipaddr)
        server["flask_bind_host"] = args.host
        server["flask_bind_port"] = args.port
        server["flask_debug"] = app.config["DEBUG"]

        ''' User/Client '''
        client = {}
        try:
            client["content-type"] = request.headers["Content-Type"]
        except KeyError:
            pass
        client["user-agent"] = request.headers["User-Agent"]
        try:
            client["x-forwarded-for"] = request.headers["X-Forwarded-For"]
        except KeyError:
            pass

        client["host"] = request.remote_addr

        ''' AWS mockups '''
        aws = {}
        for value in context.__dict__:
            aws[value] = context.__dict__[value]

        result = {
            "server": server,
            "client": client,
            "aws": aws
            }

        return(jsonify(result))
    else:
        result = {"error": "wrong method"}
        return(jsonify(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Unofficial AWS Lambda Python Local Service",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    parser.add_argument("--function_name", default="mockup-function",
                        help="Lambda function name")
    parser.add_argument("--function_version", default="$LATEST",
                        help="Lambda function version")
    parser.add_argument("--host", default="0.0.0.0",
                        help="Bind on host address")
    parser.add_argument("--port", default="5000",
                        help="Bind on host port")
    parser.add_argument("--debug", action="store_true",
                        help="Debug Flask service")

    args = parser.parse_args()

    ''' If you mount lambda_function.py, but it's empty  '''
    ''' Pull the latest from repository '''
    try:
        from lambda_function import lambda_function
        restart = False
    except ImportError:
        print(" * Warning: lambda_function.py is missing, downloading sample from github")
        url = "https://raw.githubusercontent.com/robertcsapo/aws-lambda-python-local/master/lambda_function.py"
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        with open(os.getcwd()+"/lambda_function/lambda_function.py", "wb") as f:
            f.write(response.content)
        restart = True

    if os.stat(os.getcwd()+"/lambda_function/lambda_function.py").st_size <= 2:
        print(" * Warning: lambda_function.py is empty - downloading sample from github")
        url = "https://raw.githubusercontent.com/robertcsapo/aws-lambda-python-local/master/lambda_function.py"
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()
        with open(os.getcwd()+"/lambda_function/lambda_function.py", "wb") as f:
            f.write(response.content)
        restart = True

    if restart is True:
        print(" * Restarting with new lambda_function.py")
        os.system("python main.py")

    ''' Loads AWS mockup context to object '''
    context = context.Context(args.function_name, args.function_version)
    app.run(host=args.host, port=args.port, threaded=True, debug=args.debug)
