import os
import traceback
from datetime import datetime

import dtlpy as dl


class DataloopAI:
    def __init__(self):
        dl.login()
        self.project = ""
        self.dataset = ""

    def info(self):
        """
        Todo: add different important info.
        :return:
        """

        pass

    def __str__(self):
        """
        ToDo: Add format string.
        """
        return f""

    def project_getOrCreate(self, project_name: str):
        """
        This function returns the created or existing project.

        :param project_name: str: name of the project
        :return: project object
        """
        project_list = dl.projects.list()
        for project in project_list:
            if project.name == project_name:
                print("Found project with existing name.")
                self.project = project
                return self.project
        else:
            print("Created new project as no existing found")
            self.project = dl.projects.create(project_name=project_name)
            return self.project

    def dataset_getOrCreate(self, dataset_name: str):
        """
        This function returns the created or existing dataset.
        :param dataset: str: Name of the dataset
        :return: dataset object
        """
        dataset_list = self.project.datasets.list()
        for dataset in dataset_list:
            if dataset.name == dataset_name:
                print("Found project with existing name.")
                self.dataset = dataset
                return self.dataset
        else:
            print("Created new project as no existing found")
            self.dataset = self.project.datasets.create(dataset_name=dataset_name)
            return self.dataset

    def list_dataset(self, project):
        """
        This function returns existing dataset.
        :param project: str: Project name
        :return: str : list of the project
        """
        return ", ".join([d.name for d in project.datasets.list()])

    def list_project(self):
        """
        This function returns existing project.
        :return: str: list of existing project.
        """
        return ", ".join([p.name for p in dl.projects.list()])

    def add_label(self, label_name: str, attributes: list, color=(34, 6, 231)):
        """
        This function helps add the label to the dataset.

        :param label_name: str: Name of the label
        :param attributes: list: attributes
        :param color: label color
        :return: bool: it adds the label successfully.
        """
        self.dataset.add_label(label_name=label_name, color=color, attributes=attributes)
        return True

    @staticmethod
    def uploadImages(dataset, local_path):
        """
        Uploads individual file to the dataset.

        :param dataset: dataset object
        :param local_path: str: path to the file
        :return: bool: True if file uploads else False
        """
        dataset.items.upload(local_path=local_path)
        return True

    def uploadFolder(self, folder_path, maxcount=5):
        """
        Uploads the files inside the directory.

        :param folder_path: path of the folder with images
        :param maxcount: count of thr images need to be uploaded.
                            Eg. 5 (int): 5 images will be uploaded
                                all (str): all images will be uploaded.
        """
        files = os.listdir(folder_path)
        count = len(files) if maxcount == "all" else maxcount
        for i in range(count):
            self.uploadImages(self.dataset, os.path.join(folder_path, files[i]))
            print(f"{files[i]} uploaded successfully.")

    def add_metadata(self, metadata: dict):
        self.dataset.items.metadata['user'] = dict()
        for k, v in metadata:
            self.dataset.metadata['user'][k] = v
            self.dataset.update()
            print(f"{k} = {v} Metadata added. ")


if __name__ == "__main__":
    files_dir = "flower"
    try:
        dlp = DataloopAI()
        existing_projects = dlp.list_project()
        print(f"Existing projects: ")
        print(existing_projects)
        project = dlp.project_getOrCreate('myflower')
        existing_datasets = dlp.list_dataset(project=project)
        print(f"Existing datasets: ")
        print(existing_datasets)
        dataset = dlp.dataset_getOrCreate('flower')

        dlp.add_label(label_name="flower", attributes=['rose'], color=(34, 6, 231))
        dlp.add_label(label_name="color", attributes=['red'], color=(34, 7, 231))
        dlp.add_label(label_name="count", attributes=['single', 'many'], color=(34, 8, 231))

        dlp.uploadFolder(files_dir)
        # dlp.add_metadata({"collected": datetime.now()})
    except Exception as e:
        traceback.print_exc()


