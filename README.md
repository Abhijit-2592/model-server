# Model-Server

A Pure `python-3` based flexible gRPC server for hosting Deep Learning, Machine Learning models trained on any framework! The documentation can be found here https://abhijit-2592.github.io/model-server/

## Installation

### Method 1:
Installing from [python pip](https://pypi.org/project/model-server)

`pip3 install model-server`

If you hit errors with gRPC in M2 Macbook uninstall and reinstall protobuf using conda

```bash
pip uninstall grpcio
conda install grpcio
```

If you hit the following error `google not found`. Install protobuf using conda (For somereason it doesn't work with pip on M2 macbooks)
`conda install protobuf`


### Method 2:
Creating wheel from github

1. clone the repository
2. Run `bash create_pip_wheel_and_upload.sh`. This will prompt for userid and password. You can `ctrl-c` this
3. Then install the created wheel

### Method 3:

No installation. Using the source code directly.

If this is the case, you need to compile the protobufs. Run `bash compile_protobufs.sh`. Then add the project root to your `$PYTHONPATH`.

### Note:
Method 2 and 3 requires `libprotoc>=3.6.0`


## Why Model-Server?

Taking deep learning models to production at scale is not a very straight forward process. If you are using Tensorflow then you have [Tensorflow Serving](https://www.tensorflow.org/tfx/guide/serving). But, if you are using other frameworks like [PyTorch](https://pytorch.org/), [MXNet](https://mxnet.apache.org/), [scikit-learn](https://scikit-learn.org/stable/) etc. Taking your model to production is not very straight forward (Flask, Django and other ReST frameworks). Ideally you should be able to extend Tensorflow Serving to support models from other frameworks also but, this is extremly cumbersome! Thus, to bridge this gap we have [Model-Server](https://abhijit-2592.github.io/model-server/): A high performance framework neutral serving solution! **The idea is:** if you are able to train your model in `python` you should be  able to deploy at scale using pure `python`

## Salient Features

 [Model-Server](https://abhijit-2592.github.io/model-server/) is heavily inspired from [Tensorflow Serving](https://www.tensorflow.org/tfx/guide/serving)

* **Out of box client side batching support**
* **Pure python implementation**: You don't need to fiddle around with C++ to have a scalable deployment solution
* **Framework neutral**:  Using [PyTorch](https://pytorch.org/), [MXNet](https://mxnet.apache.org/) etc? Don't worry! The solution is platform neutral. If you can use a framework to train in `python-3`, [Model-Server](https://abhijit-2592.github.io/model-server/) can deploy it at scale
* **Single server for multi-framework and multi-models**: You can host multiple models using the same framework or a mixture of multiple [PyTorch](https://pytorch.org/), [MXNet](https://mxnet.apache.org/), [scikit-learn](https://scikit-learn.org/stable/) [Tensorflow](https://www.tensorflow.org/) etc models!

## Getting started

The core of Model Server is a `Servable`. A servable is nothing but a `python class` containing your model's prediction definition which will be served by the `Model-Server`. All servables must inherit from `model_server.Servable` for the  `Model-Server` to serve it.

To deploy your model to production with `Model Server`, you just have to write a single `python-3` file containing a `class` which inherits from `model_server.Servable` and has the following two methods:

```python
predict(self, input_array_dict)
get_model_info(self, list_of_model_info_dict)
```

Now run the floowing to start the server in `5001` port
```bash
python -m model_server.runserver path_to_custom_servable_file.py
```

For more info on  command line arguments:
```bash
python -m model_server.runserver --help
```


### A simple example

create a file called `simple_servable.py` with the following contents:
```python

import numpy as np
from model_server import Servable


class my_custom_servable(Servable):
    def __init__(self, args):
        # args contains values from ArgumentParser
        # Thus you can pass any kwargs via command line and you get them here
        pass

    def predict(self, input_array_dict):
        """This method is responsible for the gRPC call GetPredictions().
        All custom servables must define this method.

        Arguments:
            input_array_dict (dict): The PredictionRequest proto decoded as a python dictionary.

        # example
        input_array_dict = {
                           "input_tensor_name1": numpy array,
                           "input_tensor_name2": numpy array
                            }

        Returns:
            A python dictionary with key (typically output name) and value as numpy array of predictions

        # example
        output = {
                   "output_tensor_name1": numpy array,
                   "output_tensor_name2": numpy array
                  }
        """
        print(input_array_dict)
        return ({"output_array1": np.array([100, 200]).astype(np.float32),
                 "output_array2": np.array(["foo".encode(),"bar".encode()]).astype(object),  # you can get and pass strings encoded as bytes also
                 })

    def get_model_info(self, list_of_model_info_dict):
        """This method which is responsible for the call GetModelInfo()

        Arguments:
            list_of_model_info_dict (list/tuple): A list containing model_info_dicts

        Note:
            model_info_dict contains the following keys:

            {
                "name": "model name as string"
                "version": "version as string"
                "status": "status string"
                "misc": "string with miscellaneous info"
            }

        Returns:
            list_of_model_info_dict (dict): containing the model and server info. This is similar to the function input
        """
        return [{"name": "first_model", "version": 1, "status": "up"},
                {"name": "second_model", "version": 2, "status": "up", "misc": "Other miscellaneous details"}]
```

Now run:

```bash
python -m model_server.runserver path/to/simple_servable.py
```
To start the gRPC server!

Now let's define the client!

```python
import grpc
import numpy as np

from model_server import server_pb2, server_pb2_grpc
from model_server.utils import create_tensor_proto
from model_server.utils import create_predict_request
from model_server.utils import create_array_from_proto
from model_server.utils import create_model_info_proto

channel = grpc.insecure_channel('localhost:5001')  # default port
# create a stub (client)
stub = server_pb2_grpc.ModelServerStub(channel)
input_array_dict = {"input1":create_tensor_proto(np.array([1,2]).astype(np.uint8)),
                    "input2":create_tensor_proto(np.array([[10.0,11.0], [12.0,13.0]]).astype(np.float32)),
                    "input3":create_tensor_proto(np.array(["Hi".encode(), "Hello".encode(), "test".encode()]).astype(object))
                   }
# create the prediction request
predict_request= create_predict_request(input_array_dict, name="simple_call")
# make the call
response = stub.GetPredictions(predict_request)

# decode the response
print(create_array_from_proto(response.outputs["output_array1"]))

# prints: array([100., 200.], dtype=float32)

# Getting the model status

model_info_proto = create_model_info_proto([])  # you can pass an empty list also
response = stub.GetModelInfo(model_info_proto)

```

Look at [examples](https://github.com/Abhijit-2592/model-server/tree/master/examples) folder for further examples


## Work in Progress

- Support server side batching and async calls.
- Provide a gRPC endpoint for [Active Learning](https://en.wikipedia.org/wiki/Active_learning_(machine_learning)) so that you can plug in `Model Server` with your labeling tool and train on fly!
- Provide a ReST wrapper

Feel free to file issues, provide suggestions and pull requests
