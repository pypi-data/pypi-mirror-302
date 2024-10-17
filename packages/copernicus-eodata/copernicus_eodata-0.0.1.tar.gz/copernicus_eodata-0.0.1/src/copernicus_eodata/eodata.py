import requests
from threading import Thread
import subprocess
import os
import time

class ODataAPI:
    def __init__(self, username: str, password: str):
        """
        Initialize a SentinelAPI object.

        Parameters
        ----------
        username : str
            Your username for the Copernicus Ecosystem.
        password : str
            Your password for the Copernicus Ecosystem.
        """
        
        self.username=username
        self.password=password
        
        self.s=requests.Session()
        
        self._get_access_token()
        
        self.downloader1=Thread(target=self._download_method, args=("",""))
        self.downloader2=Thread(target=self._download_method, args=("",""))
        self.downloader3=Thread(target=self._download_method, args=("",""))
        self.downloader4=Thread(target=self._download_method, args=("",""))

        self.s3Downloader1=S3Download()
        self.s3Downloader2=S3Download()
        self.s3Downloader3=S3Download()
        self.s3Downloader4=S3Download()
        
    def _get_access_token(self):
        """
        Get a new access token.

        This method posts a request to the Copernicus Authentication Service to
        obtain a new access token. The access token is then stored in the
        `accessToken` attribute of the SentinelAPI object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the request to the Authentication Service fails.
        """
        data = {
            "client_id": "cdse-public",
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
            }
        try:
            r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            data=data,
            )
            r.raise_for_status()
        except Exception as e:
            raise Exception(
                f"Access token creation failed. Reponse from the server was: {r.json()}"
                )
        self.accessToken = r.json()["access_token"]
        self.refreshToken = r.json()["refresh_token"]
        return
    
    def _refresh_token(self):
        """
        Refresh an existing access token.

        This method posts a request to the Copernicus Authentication Service to
        obtain a new access token based on the existing refresh token. The new
        access token is then stored in the `accessToken` attribute of the
        SentinelAPI object.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the request to the Authentication Service fails.
        """
        data = {
            "client_id": "cdse-public",
            "grant_type": "refresh_token",
            "refresh_token": self.refreshToken
        }
        try:
            r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=data,
            )
            if r.status_code==401 or r.status_code==400 :
                self._get_access_token()
                return
            r.raise_for_status()
        except Exception as e:
            raise Exception(
                f"Refreshing access token creation failed. Reponse from the server was: {r.json()}"
                )
        self.accessToken = r.json()["access_token"]
        self.refreshToken = r.json()["refresh_token"]
        return
    
    
    def search(self,product_type:str =None, area=None, start=None, end=None, expand=False, top=1000):
        
        """
        Search the Copernicus Ecosystem for products.

        Parameters
        ----------
        producttype : str, optional
            The type of product to search for. The default is None.
        area : str, optional
            The area to search in. The default is None.
        start : str, optional
            The start date of the time range to search for in the format 'YYYY-MM-DD'. The default is None.
        end : str, optional
            The end date of the time range to search for in the format 'YYYY-MM-DD'. The default is None.
        expand : bool, optional
            Whether to expand the attributes in the search result. The default is False.
        top : int, optional
            The maximum number of results to return. The default is 1000.

        Returns
        -------
        list
            A list of results matching the search query. 

        Raises
        ------
        Exception
            If the request to the Copernicus Ecosystem fails.
        """
        
        url="https://catalogue.dataspace.copernicus.eu/odata/v1/Products?"
        params=[]
            
        if product_type:
            params.append(f"contains(Name,'{product_type}')")
        if area:
            params.append(f"OData.CSC.Intersects(area=geography'SRID=4326;{area}')")
        if start:
            params.append(f"ContentDate/Start gt {start}")
        if end:
            params.append(f"ContentDate/Start lt {end}")
        
        if len(params)>0:
            url=f"{url}$filter="
            
        params=' and '.join(params)
        url=f"{url}{params}"
        
        if expand=='Attributes':
            url=f"{url}&$expand={expand}"
        url=f"{url}&$top={top}"
        result=[]
        result=self._get_query(url,result)
        return result
    
    def _get_query(self, url:str, result=[]):
        """
        Recursive function to get results from the Copernicus Ecosystem.

        Parameters
        ----------
        url : str
            The url to query.
        result : list, optional
            The list of results to extend. The default is an empty list.

        Returns
        -------
        list
            The list of results matching the search query.

        Raises
        ------
        Exception
            If the request to the Copernicus Ecosystem fails.
        """
        try:
            response = self.s.get(url).json()
        except Exception as e:
            print(e)
            return []
        if response:
            result.extend(self._get_result(response))
        if '@odata.nextLink' in response.keys():
            result = self._get_query(response['@odata.nextLink'],result)
        return result
            
    def _get_result(self, response:dict):
        """
        Process the result of a query to the Copernicus Ecosystem.

        Parameters
        ----------
        response : dict
            The response from the query.

        Returns
        -------
        list
            A list of results matching the search query.
        """
        if 'value' not in response.keys():
            return []
        result=response['value']
        for value in result:
            if 'Attributes' in value.keys():
                for attribute in value['Attributes']:
                    value[attribute['Name']]=attribute['Value']
                del value['Attributes']
        return result
        
    def get_active_downloads(self):
        """
        Check if any of the download threads are active.

        Returns
        -------
        tuple
            A tuple of 4 boolean values indicating if each of the download
            threads is active.
        """
        return (self.downloader1.is_alive(), self.downloader2.is_alive(),self.downloader3.is_alive(), self.downloader4.is_alive())
    
    def ready_to_download(self):
        """
        Check if the download threads are ready to start a new download.

        This method checks if all four of the download threads are not alive.
        If they are not alive, a new download can be started.

        Returns
        -------
        bool
            A boolean value indicating if the download threads are ready.
        """
        if self.downloader1.is_alive() and self.downloader2.is_alive() and self.downloader3.is_alive() and self.downloader4.is_alive():
            return False
        else:
            return True
    
    def download(self,uuid, product, rezip=False):
        """
        Download a product from the Copernicus Ecosystem.

        This method starts a new thread to download a product from the
        Copernicus Ecosystem. The download is done by calling the
        `_download_method` method.

        Parameters
        ----------
        uuid : str
            The uuid of the product to download.
        product : str
            The name of the product to download.
        rezip : bool, optional
            Whether to rezip the downloaded product. It will unzip and zip
            the product in a separate thread after the download which takes time but safes space.
            The default is False.

        Returns
        -------
        bool
            A boolean value indicating if the download was started
            successfully. If the download was started successfully, the
            method returns True. If the download was not started, the method
            returns False.
        """
        if not self.downloader1.is_alive():
            self.downloader1=Thread(target=self._download_method, args=(uuid,product,rezip))
            self.downloader1.start()
            return True
        elif not self.downloader2.is_alive():
            self.downloader2=Thread(target=self._download_method, args=(uuid,product,rezip))
            self.downloader2.start()
            return True
        elif not self.downloader3.is_alive():
            self.downloader3=Thread(target=self._download_method, args=(uuid,product,rezip))
            self.downloader3.start()
            return True
        elif not self.downloader4.is_alive():
            self.downloader4=Thread(target=self._download_method, args=(uuid,product,rezip))
            self.downloader4.start()
            return True
        else:
            return False
        
    def _download_method(self, uuid:str, file_name:str, rezip=True):
        
        """
        Download a product from the Copernicus Ecosystem.
        
        This method is an internal method of the SentinelAPI class. It
        downloads a product from the Copernicus Ecosystem and saves it to
        disk. The method does not return anything, but it starts a new
        thread to rezip the downloaded file if the rezip parameter is set
        to True.
        
        Parameters
        ----------
        uuid : str
            The uuid of the product to download.
        file_name : str
            The name of the product to download without the file extension.
        rezip : bool, optional
            Whether to rezip the downloaded product. It will unzip and zip
            the product in a separate thread after the download which takes
            time but safes space. The default is True.
        
        Returns
        -------
        bool
            A boolean value indicating if the download was started
            successfully. If the download was started successfully, the
            method returns True. If the download was not started, the method
            returns False.
        """
        s = requests.Session()
        headers = {"Authorization": f"Bearer {self.accessToken}"}
        s.headers.update(headers)
        
        try:
            url=f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({uuid})/$value"

            response = s.get(url, stream=True)
            
            if response.status_code==401:
                self._refresh_token()
                headers = {"Authorization": f"Bearer {self.accessToken}"}
                s.headers.update(headers)
                response = s.get(url, stream=True)

            with open(f"{file_name}{'_PART'}.zip", "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            os.rename(f"{file_name}{'_PART'}.zip",f"{file_name}.zip")
            if rezip:
                t=Thread(target=self._rezip, args=[file_name])
                t.start()
            return True
        
        except Exception as e:
            self._refresh_token()
            print(e)
            return False
        
    def _rezip(self,fileName):
        
        """
        Rezip a downloaded file
        
        Unzip the downloaded file, delete the zip file and rezip the unzipped folder.
        
        Parameters
        ----------
        fileName : str
            The name of the file to rezip.
        """
        subprocess.run(['unzip','-q',f'{fileName}.zip'])
        subprocess.run(['rm','-r', f'{fileName}.zip'])
        subprocess.run(['zip','-r','-q','-m',f'{fileName}.zip',f'{fileName}'])
    
    def s3_available(self):
        """
        Check if any of the S3 download threads are available.

        Returns
        -------
        bool
            A boolean value indicating if any of the S3 download threads are available.
        """
        if self.s3Downloader1.available():
            return True
        elif self.s3Downloader2.available():
            return True
        elif self.s3Downloader3.available():
            return True
        elif self.s3Downloader4.available():
            return True
        else:
            return False
        
    def s3_download(self,fileName,path:str,s3Path:str,s3cfg,zipping=True,progress=False):
        
        """
        Download a file from eodata s3 bucket using s3cmd and subprocees.Popen.
        s3cmd needs to be installed on the system and a cfg file 
        according to https://documentation.dataspace.copernicus.eu/APIs/S3.html needs to be provided. 
        Four parrallel downloads are supported by calling this function multiple times.
        
        Parameters
        ----------
        fileName : str
            The name of the file to download.
        s3Path : str
            The path to the file on the s3 bucket.
        path : str
            The path to download the file to.
        s3cfg : str
            The path to the s3cmd configuration file.
        zipping : bool, optional
            Whether to zip the downloaded file. The default is True.
        progress : bool, optional
            Whether to show the progress of the download. The default is False.
        
        Returns
        -------
        bool
            A boolean value indicating if the download was started successfully.
        """
        if self.s3Downloader1.available():
            self.s3Downloader1.start_download(fileName,s3Path,path,s3cfg,zipping,progress)
            return True
        elif self.s3Downloader2.available():
            self.s3Downloader2.start_download(fileName,s3Path,path,s3cfg,zipping,progress)
            return True
        elif self.s3Downloader3.available():
            self.s3Downloader3.start_download(fileName,s3Path,path,s3cfg,zipping,progress)
            return True
        elif self.s3Downloader4.available():
            self.s3Downloader4.start_download(fileName,s3Path,path,s3cfg,zipping,progress)
            return True
        else:
            return False
    


class S3Download:
    def __init__(self):
        self.fileName=None
        self.path=None
        self.s3Path=None
        self.s3cfg=None
        self.zip=None
        self.progress=None
        self.running=False

    def available(self):
        if self.running:
            return False
        else:
            return True

    def start_download(self,fileName,s3Path,path,s3cfg,zipping=True,progress=False):

        self.fileName=fileName
        self.path=path
        self.s3Path=s3Path
        self.s3cfg=s3cfg
        self.zip=zipping
        self.progress=progress
        self.running=True

        self.p=self._download_s3()
        self.monitor=Thread(target=self._monitor)
        self.monitor.start()
            
    def _monitor(self):
        run=True
        while run:
            if self.p.poll()!=None:
                run=False
                if self.zip:
                    subprocess.Popen(['zip', '-r','-m','-q',f'{self.path}/{self.fileName}.zip',f'{self.path}/{self.fileName}'])
            else:
                time.sleep(10)
        self.running=False
        return True
    
    
    def _download_s3(self):
        """
        Download a file from eodata s3 bucket using s3cmd and subprocees.Popen.
        s3cmd needs to be installed on the system and a cfg file 
        according to https://documentation.dataspace.copernicus.eu/APIs/S3.html needs to be provided. 
        Parrallel downloads are supported by calling this function multiple times.

        Returns
        -------
        Popen Object
            Popen object to monitor the download and create callbacks
        """

        if self.progress:
            progress='--progress'
        else:
            progress='--no-progress'

        if self.path:
            wd=os.getcwd()
            os.chdir(self.path)
        p=subprocess.Popen(['s3cmd', '-c', self.s3cfg,'-r',progress,'get',f's3:/{self.s3Path}'])
        if self.path:
            os.chdir(wd)
        return p
