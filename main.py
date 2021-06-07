# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import vtk

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ColorBackground = [0.0, 0.0, 0.0]
    numberOfCuts = 6

    FirstObjPath = r"./MR-Model.obj"

    reader = vtk.vtkOBJReader()
    reader.SetFileName(FirstObjPath)
    reader.Update()

    colors = vtk.vtkNamedColors()

    bounds = reader.GetOutput().GetBounds()
    print('Bounds:', ', '.join(['{:.3f}'.format(f) for f in bounds]))

    # ---------- cutter 1

    plane1 = vtk.vtkPlane()
    plane1.SetOrigin(reader.GetOutput().GetCenter())
    plane1.SetNormal(1, 0, 0)
    cutter1 = vtk.vtkPlaneCutter()
    cutter1.SetInputConnection(reader.GetOutputPort())
    cutter1.SetPlane(plane1)

    # ---------- cutter 2

    plane2 = vtk.vtkPlane()
    plane2.SetOrigin(reader.GetOutput().GetCenter())
    plane2.SetNormal(0, 0, 1)
    cutter2 = vtk.vtkPlaneCutter()
    cutter2.SetInputConnection(reader.GetOutputPort())
    cutter2.SetPlane(plane2)

    p01 = (bounds[1] , bounds[0] , bounds[5])
    p02 = (bounds[2], bounds[3], bounds[5])
    _vtkAppendPolyData = vtk.vtkAppendPolyData()

    for ks in range(numberOfCuts):
        p0 = (0, p01[1] + (p02[1] - p01[1]) / float(numberOfCuts) * ks, 0)
        plane = vtk.vtkPlane()
        plane.SetNormal(0, 1, 0)
        plane.SetOrigin(p0)

        cut = vtk.vtkCutter()
        cut.SetInputConnection(reader.GetOutputPort())
        cut.SetCutFunction(plane)
        cut.Update()
        output = cut.GetOutput()
        _vtkAppendPolyData.AddInputData(output)

    horizontalCutterMapper = vtk.vtkPolyDataMapper()
    horizontalCutterMapper.SetInputConnection(_vtkAppendPolyData.GetOutputPort())
    horizontalCutterMapper.ScalarVisibilityOff()
    horizontalCutterActor = vtk.vtkActor()
    horizontalCutterActor.GetProperty().SetColor(colors.GetColor3d('Banana'))
    horizontalCutterActor.GetProperty().SetLineWidth(2)
    horizontalCutterActor.SetMapper(horizontalCutterMapper)


    ################# cutter 1
    # Create cutter actor
    cutter1Mapper = vtk.vtkCompositePolyDataMapper()
    cutter1Mapper.SetInputConnection(cutter1.GetOutputPort())
    cutter1Mapper.ScalarVisibilityOff()
    cutter1Actor = vtk.vtkActor()
    cutter1Actor.SetMapper(cutter1Mapper)
    cutter1Actor.GetProperty().SetColor(colors.GetColor3d('Banana'))

    ################# cutter 2
    # Create cutter actor
    cutter2Mapper = vtk.vtkCompositePolyDataMapper()
    cutter2Mapper.SetInputConnection(cutter2.GetOutputPort())
    cutter2Mapper.ScalarVisibilityOff()
    cutter2Actor = vtk.vtkActor()
    cutter2Actor.SetMapper(cutter2Mapper)
    cutter2Actor.GetProperty().SetColor(colors.GetColor3d('Banana'))

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
    renderer.AddActor(cutter1Actor)
    renderer.AddActor(cutter2Actor)
    renderer.AddActor(horizontalCutterActor)
    renderer.AddActor(modelActor)

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

    # planeCut.Update()
    #
    # #DataSet of your cut:
    # planeCutPolyData=planeCut.GetOutput()
    #
    # #Let write all the slice data:
    # w=vtk.vtkPolyDataWriter()
    # w.SetFileName('anyfilename.vtp')
    # w.SetInputConnection(placeCut.GetOutputPort())
    # w.Write()
