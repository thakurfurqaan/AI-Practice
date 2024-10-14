Run the following:

## MAC OS
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt -t ./package`
- `cp lambda_function.py package/`
- `cd package`
- `python -m zipfile -c ../deployment_package.zip .`


## Windows
- `python -m venv venv`
- `.\venv\Scripts\activate`
- `pip install -r requirements.txt -t ./package ; cp lambda_function.py package/ ; cd package ; python -m zipfile -c ../deployment_package.zip . ; cd ..`


- Then upload the zip file to AWS Lambda.

- Link it to an API Gateway endpoint.
- Pass the params in URL string or in the body of the request.
- Then call the API Gateway endpoint from a browser or any HTTP client.
