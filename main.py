# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import vtk
import json
import os

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def writeToObjFile(data, fileName):
    writer = vtk.vtkOBJWriter()
    writer.SetFileName(os.path.join(os.getcwd(), "cutts", fileName))
    writer.SetInputData(data)
    writer.Update()

def writeAsXmlFile(data, fileName):
    vtkXMLPolyDataWriter = vtk.vtkXMLPolyDataWriter()
    vtkXMLPolyDataWriter.SetFileName(os.path.join(os.getcwd(), "cutts", fileName))
    vtkXMLPolyDataWriter.SetInputConnection(data)
    vtkXMLPolyDataWriter.Update()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ColorBackground = [0.0, 0.0, 0.0]

    # read protocol file
    with open('protocol.json', 'r') as myfile:
        data = myfile.read()

    # parse file
    protocol = json.loads(data)
    protocol = protocol['protocol']['data']
    # print("usd: " + str(len(protocol['right'])))

    numberOfCuts = len(protocol['right'])


    FirstObjPath = r"./MR-Model.obj"

    reader = vtk.vtkOBJReader()
    reader.SetFileName(FirstObjPath)
    reader.Update()

    colors = vtk.vtkNamedColors()

    bounds = reader.GetOutput().GetBounds()
    print('Bounds:', ', '.join(['{:.3f}'.format(f) for f in bounds]))

    # ---------- X plane
    plane1 = vtk.vtkPlane()
    plane1.SetOrigin(reader.GetOutput().GetCenter())
    plane1.SetNormal(1, 0, 0)
    # ---------- Z plane
    plane2 = vtk.vtkPlane()
    plane2.SetOrigin(reader.GetOutput().GetCenter())
    plane2.SetNormal(0, 0, 1)

    p01 = (bounds[1], bounds[0], bounds[5])
    p02 = (bounds[2], bounds[3], bounds[5])

    # collectData
    _vtkAppendPolyData = vtk.vtkAppendPolyData()

    for i in range(numberOfCuts):
        p0 = (0, p01[1] + (p02[1] - p01[1]) / float(numberOfCuts) * i, 0)
        plane = vtk.vtkPlane()
        plane.SetNormal(0, 1, 0)
        plane.SetOrigin(p0)

        cut = vtk.vtkCutter()
        cut.SetInputConnection(reader.GetOutputPort())
        cut.SetCutFunction(plane)
        cut.Update()

        # fill cutts
        FeatureEdges = vtk.vtkFeatureEdges()
        FeatureEdges.SetInputConnection(cut.GetOutputPort())
        FeatureEdges.BoundaryEdgesOn()
        FeatureEdges.FeatureEdgesOff()
        FeatureEdges.NonManifoldEdgesOff()
        FeatureEdges.ManifoldEdgesOff()
        FeatureEdges.Update()

        cutStrips = vtk.vtkStripper()  # Forms loops (closed polylines) from cutter
        cutStrips.SetInputConnection(cut.GetOutputPort())
        cutStrips.Update()
        cutPoly = vtk.vtkPolyData()  # This trick defines polygons as polyline loop
        cutPoly.SetPoints((cutStrips.GetOutput()).GetPoints())
        cutPoly.SetPolys((cutStrips.GetOutput()).GetLines())

        # need to be exported
        leftSide = vtk.vtkClipPolyData()
        leftSide.SetInputData(cutPoly)
        leftSide.SetClipFunction(plane1)
        leftSide.Update()
        # need to be exported
        rightSide = vtk.vtkClipPolyData()
        rightSide.SetInputData(cutPoly)
        rightSide.InsideOutOn()
        rightSide.SetClipFunction(plane1)
        rightSide.Update()

        if(len(protocol['right'][i]['cut']) == 1):
            writeToObjFile(rightSide.GetOutput(), protocol['right'][i]['cut'][0]['name'])
            writeToObjFile(leftSide.GetOutput(), protocol['left'][i]['cut'][0]['name'])
            _vtkAppendPolyData.AddInputData(rightSide.GetOutput())
            _vtkAppendPolyData.AddInputData(rightSide.GetOutput())

        if(len(protocol['right'][i]['cut']) > 1):

            leftSideDorsal = vtk.vtkClipPolyData()
            leftSideDorsal.SetInputData(leftSide.GetOutput())
            leftSideDorsal.SetClipFunction(plane2)
            leftSideDorsal.Update()

            leftSideVentral = vtk.vtkClipPolyData()
            leftSideVentral.SetInputData(leftSide.GetOutput())
            leftSideVentral.InsideOutOn()
            leftSideVentral.SetClipFunction(plane2)
            leftSideVentral.Update()

            rightSideDorsal = vtk.vtkClipPolyData()
            rightSideDorsal.SetInputData(rightSide.GetOutput())
            rightSideDorsal.SetClipFunction(plane2)
            rightSideDorsal.Update()

            rightSideVentral = vtk.vtkClipPolyData()
            rightSideVentral.SetInputData(rightSide.GetOutput())
            rightSideVentral.InsideOutOn()
            rightSideVentral.SetClipFunction(plane2)
            rightSideVentral.Update()

            writeToObjFile(rightSideVentral.GetOutput(), protocol['right'][i]['cut'][0]['name'])
            writeToObjFile(rightSideDorsal.GetOutput(), protocol['right'][i]['cut'][1]['name'])
            writeToObjFile(leftSideVentral.GetOutput(), protocol['left'][i]['cut'][0]['name'])
            writeToObjFile(leftSideDorsal.GetOutput(), protocol['left'][i]['cut'][1]['name'])

            _vtkAppendPolyData.AddInputData(rightSideVentral.GetOutput())
            _vtkAppendPolyData.AddInputData(rightSideDorsal.GetOutput())
            _vtkAppendPolyData.AddInputData(leftSideVentral.GetOutput())
            _vtkAppendPolyData.AddInputData(leftSideDorsal.GetOutput())
        else:
            _vtkAppendPolyData.AddInputData(cutPoly)

    writeAsXmlFile(_vtkAppendPolyData.GetOutputPort(), "cut")

    horizontalCutterMapper = vtk.vtkPolyDataMapper()
    horizontalCutterMapper.SetInputConnection(_vtkAppendPolyData.GetOutputPort())
    horizontalCutterMapper.ScalarVisibilityOff()
    horizontalCutterActor = vtk.vtkActor()
    horizontalCutterActor.GetProperty().SetColor(colors.GetColor3d('Banana'))
    horizontalCutterActor.GetProperty().SetLineWidth(2)
    horizontalCutterActor.SetMapper(horizontalCutterMapper)

    ################# model
    # Create model actor
    modelMapper = vtk.vtkPolyDataMapper()
    modelMapper.SetInputConnection(reader.GetOutputPort())
    modelMapper.ScalarVisibilityOff()
    modelActor = vtk.vtkActor()
    modelActor.GetProperty().SetColor(colors.GetColor3d('Flesh'))
    modelActor.SetMapper(modelMapper)

    # Create renderers and add actors of plane and model
    renderer = vtk.vtkRenderer()
    renderer.AddActor(horizontalCutterActor)
    # renderer.AddActor(modelActor)

    # Add renderer to renderwindow and render
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(600, 600)
    renderWindow.SetWindowName('CutWithCutFunction')

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    renderer.SetBackground(colors.GetColor3d('Burlywood'))
    renderer.GetActiveCamera().SetPosition(0, -1, 0)
    renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
    renderer.GetActiveCamera().SetViewUp(0, 0, 1)
    renderer.GetActiveCamera().Azimuth(30)
    renderer.GetActiveCamera().Elevation(30)

    renderer.ResetCamera()
    renderWindow.Render()

    interactor.Start()
