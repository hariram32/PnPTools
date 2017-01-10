#!/usr/bin/env python

from login import login
from apic_config import DIR
import os

#DIR="../pnp_files"
class File(object):
    def __init__(self, apic, name,namespace, path):
        self.apic = apic
        self.name = name
        self.namespace = namespace
        self.path = path + "/" + name
        self.fileid = None

    def update(self):
        file_result = self.apic.file.updateFile(nameSpace=self.namespace, fileUpload=self.path, fileId=self.fileid)
        return file_result

    def upload(self):
        file_result = self.apic.file.uploadFile(nameSpace=self.namespace, fileUpload=self.path)
        return(file_result)

    def delete(self):
        file_result = self.apic.deleteFile(fileId=self.fileid)
        return file_result

    def present(self):
        files = self.apic.file.getFilesByNamespace(nameSpace=self.namespace)
        fileid_list = [file.id for file in files.response if file.name == self.name]
        self.fileid =  None if fileid_list == [] else fileid_list[0]
        return self.fileid


def check_namespace(apic, namespace):
    names = apic.file.getNameSpaceList()
    if names is not None:
        return namespace in names.response
    else:
        return False

def process_namespace(apic, namespace):
    if check_namespace(apic, namespace):
        print("NameSpace:{namespace}:valid".format(namespace=namespace))
    else:
        raise ValueError

    rootDir = DIR + "/" + namespace + "s"

    if not os.path.isdir(rootDir):
        print("No directory for {rootDir}, skipping".format(rootDir=rootDir))
        return

    for filename in os.listdir(rootDir):
        f = File(apic, filename, namespace, rootDir)

        if f.present() is None:
            result = f.upload()
            print("Uploaded File:{file} ({id})".format(file=result.response.name,id=result.response.id))
        else:
            result = f.update()
            print("Updated File:{file} ({id})".format(file=result.response.name, id=result.response.id))

def main():
    apic = login()
    for namespace in ["config", "template", "image"]:
        process_namespace(apic, namespace)

if __name__ == "__main__":
    main()