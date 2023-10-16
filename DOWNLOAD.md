Dataset **Labeled Surgical Tools and Images** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/P/n/Ap/p3y3UUJc22o4oOsqcYv1Zw1TA3aDd1MoQPjkwQ8tprbYdfb1UzHtvkLPRzO0m7ddca2XjPWZcdxehrwm3MwsRt97KdnB567u10vq4XiJbHaGcgCC6IaXuzRtaLYs.tar)

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