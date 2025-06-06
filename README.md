# QuantEcon WASM project

This repository contains a subset of the [lecture-python-intro](https://intro.quantecon.org/intro.html).

This project is powered by Pyodide kernel which allows us to run the lectures in the browser without
any installation.

## Development

The script `update_lectures.py` is used to fetch the latest version of lectures from the
[wasm branch of lecture-python-intro series](https://github.com/QuantEcon/lecture-python-intro/tree/wasm).

In order to build and test the project locally, please install the required libraries using
```
pip install -r requirements.txt
```

The first step is to build the lecture series. To do so, use the following:
```
teachbooks build book
```

And run a local server using
```
teachbooks serve
```

To stop the server use:
```
teachbooks serve stop
```

### Update a lecture?

In order to update any lecture, it's recommended to update the same lecture in the
[wasm branch of lecture-python-intro series](https://github.com/QuantEcon/lecture-python-intro/tree/wasm) and 
run the script
```
python update_lectures.py
```

This allows us the keep all the lectures up-to-date in a single place and keep this repository a mirror of the 
main repository.
