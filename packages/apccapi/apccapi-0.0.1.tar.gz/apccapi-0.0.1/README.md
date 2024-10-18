## Installation

Install via pip with:

```bash
$ pip install apccapi
```

## Configure (Linux)

Obtain your API key from the CLIK (Climate Information toolKit) at https://cliks.apcc21.org and enter it into the apccapi.properties file, formatting it as follows:

```
$ vi ~/.apccapi.properties

key={your API key}
request_url=https://request.apcc21.org/apccdata
status_url=https://request.apcc21.org/status
```

## Configure (Windows)

Obtain your API key from the CLIK (Climate Information toolKit) at https://cliks.apcc21.org, and create the apccapi.properties file in your Windows Home directory (typically C:\Users\YourUserName) with the following format:

```
key={your API key}
request_url=https://request.apcc21.org/apccdata
status_url=https://request.apcc21.org/status
```

## Test

Perform a small test retrieve of MME data:
```
$ python
>>> import apccapi
>>> c = apccapi.Client()
>>> c.retrieve(
	{
		'jobtype': 'MME',
		'dataset': 'MME_3MONTH',
		'type': 'FORECAST',
		'method': 'SCM',
		'variable': ['prec', 't2m'],
		'period': ['Monthly mean'],
		'yearmonth': ['201909']
	},
	'mme3.zip'
)
>>>

```

## License

MIT License

Copyright (c) 2019 - 2024, APEC Climate Center

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.