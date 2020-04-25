# aws-lambda-python-local  
Docker Hub (Cloud)  
![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/robertcsapo/aws-lambda-python-local)![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/robertcsapo/aws-lambda-python-local)![Docker Image Size (tag)](https://img.shields.io/docker/image-size/robertcsapo/aws-lambda-python-local/latest)  
Python versions  
![Docker Image Version (tag latest semver)](https://img.shields.io/docker/v/robertcsapo/aws-lambda-python-local/3.9)![Docker Image Version (tag latest semver)](https://img.shields.io/docker/v/robertcsapo/aws-lambda-python-local/3.8)![Docker Image Version (tag latest semver)](https://img.shields.io/docker/v/robertcsapo/aws-lambda-python-local/3.7)![Docker Image Version (tag latest semver)](https://img.shields.io/docker/v/robertcsapo/aws-lambda-python-local/3.6)  

Local development setup to mock an AWS Lambda Setup.  
Edit your ```lambda_function.py```, as you do in AWS.  

```
import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```
_(```lambda_function.py``` is either hosted mounted or downloaded automatically, when running as Docker image)_


Execute your AWS Lambda function through HTTP.  
```curl http://localhost:5000```

## Features
- [x] event
  - json
- [x] context (mockup)
  - function_name
  - function_version
  - invoked_function_arn
  - aws_request_id
  - log_group_name
  - log_stream_name
  - memory_limit_in_mb

## Usage

### Docker
```docker run -it --rm -p 5000:5000 -v $PWD:/aws-lambda-python-local/lambda_function/ robertcsapo/aws-lambda-python-local:latest```

If **lambda_function.py** is missing in **$PWD**
* It will download a sample from this github repo
```
 * lambda_function.py is missing, downloading sample from github
```
* Throw Error if issues with $PWD
```
FileNotFoundError: [Errno 2] No such file or directory: '/aws-lambda-python-local/lambda_function/lambda_function.py'
```

#### Settings
```docker run -it --rm -p 5000:5000 -v $PWD:/aws-lambda-python-local/lambda_function/ robertcsapo/aws-lambda-python-local:latest -h```

```
usage: main.py [-h] [--function_name FUNCTION_NAME] [--function_version FUNCTION_VERSION] [--host HOST] [--port PORT] [--debug]

Unofficial AWS Lambda Python Local Service

optional arguments:
  -h, --help            show this help message and exit
  --function_name FUNCTION_NAME
                        Lambda function name (default: mockup-function)
  --function_version FUNCTION_VERSION
                        Lambda function version (default: $LATEST)
  --host HOST           Bind on host address (default: 0.0.0.0)
  --port PORT           Bind on host port (default: 5000)
  --debug               Debug Flask service (default: False)
```

#### Docker Memory Limit (as in AWS Lambda)
```docker run --memory 512m -it --rm -p 5000:5000 -v $PWD:/aws-lambda-python-local/lambda_function/ robertcsapo/aws-lambda-python-local:latest```

### Change Python versions

#### Python 3.8
```docker run -it --rm -p 5000:5000 -v $PWD:/aws-lambda-python-local/lambda_function/ robertcsapo/aws-lambda-python-local:3.8```

#### Python 3.7
```docker run -it --rm -p 5000:5000 -v $PWD:/aws-lambda-python-local/lambda_function/ robertcsapo/aws-lambda-python-local:3.7```

#### Python 3.6
```docker run -it --rm -p 5000:5000 -v $PWD:/aws-lambda-python-local/lambda_function/ robertcsapo/aws-lambda-python-local:3.6```

#### Host environment
```curl http://localhost:5000/host```

```
{
  "aws": {
    "aws_request_id": "5964a9d6-7d76-11ea-8c74-0242ac110004",
    "function_name": "mockup-function",
    "function_version": "$LATEST",
    "invoked_function_arn": "arn:aws:lambda:eu-north-1:000000000000:function:mockup-function",
    "log_group_name": "/aws/lambda/mockup-function",
    "log_stream_name": "2020/04/13/[$LATEST]4459c970fa6d4c77aca62c95850fce54",
    "memory_limit_in_mb": "512.0M"
  },
  "client": {
    "content-type": "application/json",
    "host": "172.17.0.1",
    "user-agent": "PostmanRuntime/7.24.0"
  },
  "server": {
    "flask_bind_host": "0.0.0.0",
    "flask_bind_port": "5000",
    "flask_debug": true,
    "hostname": "ab60f3ae120b",
    "ipaddr": [
      "172.17.0.4/16"
    ],
    "path": "/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "pwd": "/data/export",
    "python_version": "3.8.0"
  }
}
```

### non-Docker

#### Build
```git clone https://github.com/robertcsapo/aws-lambda-python-local.git```

#### Run
```python main.py```

#### Settings
```python main.py -h ```

#### Limitations with non-Docker
- Can't limit memory (only on host)
- Manually installing python versions and virtualenv

## License
  
MIT License  
Copyright (c) 2020 robertcsapo
