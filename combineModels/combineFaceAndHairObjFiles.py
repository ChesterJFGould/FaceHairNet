# site: https://inareous.github.io/posts/opening-obj-using-py

import argparse
import sys
import numpy as np

class CombineFaceAndHairMesh:
    
    def __init__(self, faceFile, hairFile, outFile):
        # vertices(list of vertex) of first file and and second file
        self.filesVertices = []
        # faces(list of face) of first file and and second file
        self.filesFaces = []
        self.faceFileIndex = 0
        self.hairFileIndex = 1
        self.x = 0
        self.y = 1
        self.z = 2
        self.r = 3
        self.b = 4
        self.g = 5
        self.vertex1 = 0
        self.vertex2 = 1
        self.vertex3 = 2
        self.hairR = 51
        self.hairB = 25
        self.hairG = 0
        self.hairMeshXLen = 0
        self.hairMeshYLen = 0
        self.faceMeshXLen = 0
        self.faceMeshYLen = 0

        try:
            f1 = open(faceFile)
            f2 = open(hairFile)
            files = [f1, f2]

            for i in range(len(files)):
                vertices = []
                faces = []
                for line in files[i]:
                    lineList = line.split()
                    if lineList[0] == "v":
                        vertex = any
                        # vertex is in a form of "v 0.123 0.234 0.345" or "v 347.529 14.994 182.927 0.2 0.098 0.050"
                        # When there is 6 floats, last three represent color
                        if (len(lineList) > 4): 
                            vertex = np.array([float(lineList[1]), float(lineList[2]), float(lineList[3]), float(lineList[4]), float(lineList[5]), float(lineList[6])])
                        else:
                            # file up rgb value for hair mesh
                            vertex = np.array([float(lineList[1]), float(lineList[2]), float(lineList[3]), float(self.hairR), float(self.hairB), float(self.hairG)])
                        vertices.append(vertex)

                    elif lineList[0] == "f":
                        face = ([int(lineList[1]), int(lineList[2]), int(lineList[3])])
                        faces.append(face)
                # change list to np array        
                vertices = np.array(vertices)
                faces = np.array(faces)
                self.filesVertices.append(vertices)
                self.filesFaces.append(faces)

            # change list to np array        
            self.filesVertices = np.array(self.filesVertices, dtype=object)
            self.filesFaces = np.array(self.filesFaces, dtype=object)

            f1.close()
            f2.close()

        except IOError:
            print(".obj file not found.")

        self.moveFaceMeshToOrigin()
        self.resizeFaceMeshThatIsInOrigin()

        file = open(outFile, 'w')
        for vertices in self.filesVertices:
            for vertex in vertices:
                file.write("v {0} {1} {2} {3} {4} {5}\n".format(vertex[self.x], vertex[self.y], vertex[self.z], vertex[self.r], vertex[self.b], vertex[self.g]))

        # update the second file faces value because second file vertices index are changed by appending them to first file vertices.
        numOfVerticesOnFirstFile = 0
        for faces in self.filesFaces:
            for face in faces:
                file.write("f {0} {1} {2}\n".format(face[self.vertex1] + numOfVerticesOnFirstFile, face[self.vertex2] + numOfVerticesOnFirstFile, face[self.vertex3] + numOfVerticesOnFirstFile))
            numOfVerticesOnFirstFile = len(self.filesVertices[0])
        
        file.close()
            
    def moveFaceMeshToOrigin(self):

        list = [self.x, self.y, self.z]

        for axis in list:
            minVal = np.min(self.filesVertices[self.faceFileIndex][:,axis])
            maxVal = np.max(self.filesVertices[self.faceFileIndex][:,axis])
            midPointVal = float((maxVal + minVal)/2)
            minPointIndex = (np.abs(self.filesVertices[self.faceFileIndex][:,axis] - midPointVal)).argmin()
            closestMidPointVal = self.filesVertices[self.faceFileIndex][:,axis][minPointIndex]
            self.filesVertices[self.faceFileIndex][:,axis] = self.filesVertices[self.faceFileIndex][:,axis] - closestMidPointVal
            if (axis == self.x):
                self.faceMeshXLen = float((maxVal - minVal))
            elif (axis == self.y):
                self.faceMeshYLen = float((maxVal - minVal))

        # rotate the face to align with hair
        self.filesVertices[self.faceFileIndex][:,[self.x, self.z]] = self.filesVertices[self.faceFileIndex][:,[self.z, self.x]]


    def resizeFaceMeshThatIsInOrigin(self):

        list = [self.x, self.y]

        # get the length on x and y axises of hair
        for axis in list:
            minVal = np.min(self.filesVertices[self.hairFileIndex][:,axis])
            maxVal = np.max(self.filesVertices[self.hairFileIndex][:,axis])
            if (axis == self.x):
                self.hairMeshXLen = float((maxVal - minVal))
            elif (axis == self.y):
                self.hairMeshYLen = float((maxVal - minVal))

        # calculate resize rate 
        resizeRateX = int(np.ceil(self.faceMeshXLen/self.hairMeshXLen))
        resizeRateY = int(np.ceil(self.faceMeshYLen/self.hairMeshYLen))
        resizeRate = max(resizeRateX, resizeRateY) + 100

        list = [self.x, self.y, self.z]

        for axis in list:
            self.filesVertices[self.faceFileIndex][:,axis] = self.filesVertices[self.faceFileIndex][:,axis] / resizeRate




if __name__ == "__main__":

    # how to run: python combineFaceAndHairObjFiles.py -facef faceFileLocation -hairf HairFileLocation
    model = CombineFaceAndHairMesh(sys.argv[1], sys.argv[2], sys.argv[3])
