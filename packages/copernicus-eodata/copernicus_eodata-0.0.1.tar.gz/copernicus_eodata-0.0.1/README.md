# Copernicus Ecosystem OData API
This is a simple package based on the tutorials from https://documentation.dataspace.copernicus.eu/APIs/OData.html. It does not support full functionality for searching but only product type, start and end sensing date, geographic criterior as intersection and expand attributes. There is a lot of room for improvement. Contribution is very welcome.

All other attributes by collection are not yet supported in the search query.

## Overview
Up to four parallel Downloads are supported, the maximum from OData. It uses the requests library to make API calls and the threading library to handle concurrent downloads.

## Installation
To install the library, use pip:

```bash
pip install copernicus-ecosystem
```
## Usage
To search and download images from OData
```python
from copernicus-ecosystem import ODataAPI

api=ODataAPI(username, password)
search_result(product_type='IW_SLC',start='2021-05-20T00:00:00', end='2021-05-21T00:00:00',expand="Attributes")
api.download(id, filename)
```
more information on available querys can be found here: https://documentation.dataspace.copernicus.eu/APIs/OData.html#list-of-odata-query-attributes-by-collection
### Multiple Downloads
If you want to download multiple files you could mange that in your own loop like that:
```python
from copernicus-ecosystem import ODataAPI

api=ODataAPI(username, password)
ids=[id1,id2,id3] #list of image ids
run=True
while run:
    remove=[]
    for image_id in ids:
        if api.ready_to_download(): # check if api is ready or all 4 downloads are still busy
            api.download(uuid,i) #start download thread
            remove.append(i) #remember to remov ethe image id from the list
    for i in remove:
        images.remove(i) #remove the image ids that are being downloaded
    time.sleep(10) #wait for 10 seconds before you check for one of four available download slots
    if len(images)==0:
        run=False # stop the loop when the list is empty. The threads will continue to download
```

### S3 Bucket download
It is also possible to download the data using the S3 bucket. You will need s3cmd and a s3cfg file according to this tutorial: https://documentation.dataspace.copernicus.eu/APIs/S3.html

```python
from copernicus-eodata import ODataAPI

api=ODataAPI(username, password)
api.s3_download(fileName,path,s3Path,s3cfg,zipping=True,progress=False)
```
The filename and the path to where the product should be downloaded needs to be passed seperatly. By default the downloaded product will be zipped after the download which takes addtional time.
## Contributing
Contributions are welcome! Please submit a pull request with your changes.

## License
This library is licensed under the MIT License. See LICENSE for details.