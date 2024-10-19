import requests
from projectkiwi3.models import Project, Annotation, Label, LabelingQueue, LabelingTask, Imagery
import numpy as np
from typing import List, Dict
from PIL import Image
import io
import base64
import shapely

class Client():
    imageryUrls: Dict[int, str] = {}

    def __init__(self, key: str, url:str ="https://projectkiwi.io"):
        """constructor

        Args:
            key (str): API key.
            url (str, optional): url for api, mostly used for development. Defaults to "https://projectkiwi.io".
        """

        self.key = key

        # trim trailing slash
        if url[-1] == "/":
            url = url[:-2]
        self.url = url

        if "localhost" in self.url:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    
    def get(self, url: str) -> any:
        """requests.get wrapper that adds api key

        Args:
            url (str): Full url to be passed to requests.get

        Returns:
            any: resp.json() from response
        """
        if "localhost" in self.url:
            resp = requests.get(url, verify=False, headers={'x-api-key': self.key})
        else:
            resp = requests.get(url, headers={'x-api-key': self.key})
        resp.raise_for_status()
        return resp.json()
    

    def post(self, url: str, json: dict) -> any:
        """requests.post wrapper that adds api key.

        Args:
            url (str): Full url to be passed to requests.post
            json (dict): request body in dict form

        Returns:
            any: resp.json() from response
        """        
        if "localhost" in self.url:
            resp = requests.post(url, json=json, verify=False, headers={'x-api-key': self.key})
        else:
            resp = requests.post(url, json=json, headers={'x-api-key': self.key})
        resp.raise_for_status()
        return resp.json()
    
    def getProject(self, projectId: int) -> List[Project]:
        """Get project details.

        Returns:
            Project: Project details
        """
        json = self.get(f"{self.url}/api/project/{projectId}")
        project: Project = Project.from_dict(json)
        return project

    def getProjects(self) -> List[Project]:
        """Get a list of projects for the user.

        Returns:
            List[Project]: Projects
        """
        json = self.get(f"{self.url}/api/project")
        projects: List[Project] = [Project.from_dict(projectDict) for projectDict in json]
        return projects
    


    def getLabels(self, projectId: int) -> List[Label]:
        """Get all labels for a given project.

        Args:
            projectId (int): The ID of the project e.g. 869

        Returns:
            List[Label]: All labels in the project(active and inactive)
        """        
        json = self.get(f"{self.url}/api/project/{projectId}/labels")
        labels: List[Label] = [Label.from_dict(labelDict) for labelDict in json]
        return labels

    
    def getAnnotations(self, projectId: int) -> List[Annotation]:
        """Get all annotations in the project.

        Args:
            projectId (int): The ID of the project e.g. 869

        Returns:
            List[Annotation]: All annotations in the project.
        """
        json = self.get(f"{self.url}/api/project/{projectId}/annotations")
        annotations: List[Annotation] = [Annotation.from_dict(dict) for dict in json]
        return annotations



    def getLabelingQueues(self, projectId: int) -> List[LabelingQueue]:
        """ Get all labeling queues for the project (sometimes called labeling workflows)

        Args:
            projectId (int): The ID of the project e.g. 869

        Returns:
            List[LabelingQueue]: All labeling queues
        """
        json = self.get(f"{self.url}/api/project/{projectId}/labelingQueue")
        queues: List[LabelingQueue] = [LabelingQueue.from_dict(dict) for dict in json]
        return queues
    
    def getLabelingQueue(self, id: int) -> LabelingQueue:
        """ Get labeling queue for a given id

        Args:
            id (int): The ID of the labeling queue, sometimes called 'labeling workflow' e.g. 421

        Returns:
            LabelingQueue: The labelingQueue
        """
        json = self.get(f"{self.url}/api/labelingQueue/{id}")
        queue: LabelingQueue = LabelingQueue.from_dict(json)
        return queue
    
    
    def getAllImagery(self, projectId: int) -> List[Imagery]:
        """ Get all imagery layers (geotiffs) for the project

        Args:
            projectId (int): The ID of the project e.g. 869

        Returns:
            List[Imagery]: All imagery layers
        """        
        json = self.get(f"{self.url}/api/project/{projectId}/imagery")
        imagery: List[Imagery] = [Imagery.from_dict(dict) for dict in json]
        return imagery
    
    def getImagery(self, imageryId: int) -> Imagery:
        """ Get a single imagery layer

        Args:
            imageryId (int): The ID of the imagery layer e.g. 869

        Returns:
            Imagery: The imagery layers
        """        
        json = self.get(f"{self.url}/api/imagery/{imageryId}")
        imagery: Imagery = Imagery.from_dict(json) 
        return imagery

    
    def getImageForTask(self, imageryId: int, coordinates: List[List[float]], max_size: int = 1024, padding_factor: float = None) -> np.array:
        """Get a numpy array for a given imagery layer within a set of coordinates.

        Args:
            imageryId (int): Id of Imagery layer to extract image from
            coordinates (List[List[float]]): coordinates in [[lng,lat], [lng,lat]] format
            max_size (int, optional): maximum width for the image. Defaults to 1024.
            padding_factor(float, optional): How much space to pad on each size. e.g. 0.2 will add 20% to each side

        Returns:
            np.array: image, which may include black borders for irregular shapes or at edges of layer.
        """       


        if padding_factor:
            polygon = shapely.Polygon(coordinates)
            scaled_polygon = shapely.affinity.scale(polygon, xfact=1+(2*padding_factor), yfact=1+(2*padding_factor))
            coordinates = list(scaled_polygon.exterior.coords)


        if not imageryId in self.imageryUrls:
            self.imageryUrls[imageryId] = self.get(f"{self.url}/api/imagery/{imageryId}/download_url")
        
        
        featureDict = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "coordinates": [coordinates],
                "type": "Polygon"
            }
        }
        r = requests.post("https://api.projectkiwi.io/v3/get_part", 
                            json={'polygon': featureDict,
                            'cog_url': self.imageryUrls[imageryId],
                            'max_size': max_size,
                            'base64': False
        })
        r.raise_for_status()
        image = Image.open(io.BytesIO(base64.decodebytes(bytes(r.text, "utf-8"))))
        return np.asarray(image)
    
    def addLabel(self, projectId: int, name: str, color: str = "rgb(255, 0, 0)") -> Label:
        """ Add a label to a project, sometimes called an annotation layer.

        Args:
            projectId (int): Project to add the label to e.g. 178
            name (str): Label name
            color (str, optional): label color in rgb(x, x, x) format. Defaults to "rgb(255, 0, 0)".

        Returns:
            Label: The created label
        """        
        json = self.post(f"{self.url}/api/project/{projectId}/labels", json={
            "name": name,
            "color": color,
            "active": True,
        })
        newLabel: Label = Label.from_dict(json)
        return newLabel

    def addAnnotation(self, projectId: int, coordinates: List[List[float]], shape: str, labelId: int, confidence: float = 1.0) -> Annotation:
        """Add an annotation to the project

        Args:
            projectId (int): ID of the project
            coordinates (List[List[float]]): coordinates in [[lng,lat], [lng,lat]] format. For Polygons, first and last coordinate should match.
            shape (str): Shape of the annotation, must be one of: Point, Polygon, Linestring
            labelId (int): Id of the label to assign to the annotation
            confidence (float): Confidence in the annotation e.g. 0.6. Defaults to 1.0.

        Returns:
            Annotation: The resulting created annotation.
        """
        VALID_SHAPES = ["Point", "Polygon", "Linestring"]
        assert shape in VALID_SHAPES, f"Shape must be one of: {VALID_SHAPES}"

        json = self.post(f"{self.url}/api/project/{projectId}/annotations", json={
            "coordinates": coordinates,
            "shape": shape,
            "labelId": labelId,
            "confidence": confidence
        })
        newAnnotation: Annotation = Annotation.from_dict(json)
        return newAnnotation