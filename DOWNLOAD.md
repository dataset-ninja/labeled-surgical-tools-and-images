Dataset **Labeled Surgical Tools and Images** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogInMzOi8vc3VwZXJ2aXNlbHktZGF0YXNldHMvMTkzNV9MYWJlbGVkIFN1cmdpY2FsIFRvb2xzIGFuZCBJbWFnZXMvbGFiZWxlZC1zdXJnaWNhbC10b29scy1hbmQtaW1hZ2VzLURhdGFzZXROaW5qYS50YXIiLCAic2lnIjogIlpMZTA1ZXYxQUhZblN5NS9QTXhlcmthMHhOTjZ5bzhFaTNjWDgreks2NFU9In0=?response-content-disposition=attachment%3B%20filename%3D%22labeled-surgical-tools-and-images-DatasetNinja.tar%22)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Labeled Surgical Tools and Images', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/dilavado/labeled-surgical-tools/download?datasetVersionNumber=1).