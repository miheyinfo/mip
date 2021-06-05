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

    # ----------

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

    # ----------

    plane = vtk.vtkPlane()
    plane.SetOrigin((bounds[1] + bounds[0]) / 2.0, (bounds[3] + bounds[2]) / 2.0, bounds[4])
    plane.SetNormal(1, 0, 0)

    # Create cutter
    high = plane.EvaluateFunction((bounds[1] + bounds[0]) / 2.0, (bounds[3] + bounds[2]) / 2.0, bounds[5])

    verticalCutter = vtk.vtkCutter()
    verticalCutter.SetInputConnection(reader.GetOutputPort())
    verticalCutter.SetCutFunction(plane)
    verticalCutter.GenerateValues(1, 0.99, 0.99 * high)



    plane2 = vtk.vtkPlane()
    plane2.SetOrigin( bounds[5], (bounds[1] + bounds[0]) / 2.0, 0)
    plane2.SetNormal(0, 0, -1)


    verticalCutter2 = vtk.vtkCutter()
    verticalCutter2.SetInputConnection(reader.GetOutputPort())
    verticalCutter2.SetCutFunction(plane2)
    verticalCutter2.GenerateValues(1, 0.99, 0.99 * high)


    horizontalCutterMapper = vtk.vtkPolyDataMapper()
    horizontalCutterMapper.SetInputConnection(_vtkAppendPolyData.GetOutputPort())
    horizontalCutterMapper.ScalarVisibilityOff()

    verticalCutterMapper = vtk.vtkPolyDataMapper()
    verticalCutterMapper.SetInputConnection(verticalCutter.GetOutputPort())
    verticalCutterMapper.ScalarVisibilityOff()

    verticalCutterMapper2 = vtk.vtkPolyDataMapper()
    verticalCutterMapper2.SetInputConnection(verticalCutter2.GetOutputPort())
    verticalCutterMapper2.ScalarVisibilityOff()



    # ----------

    # Create horizontal cut actor
    horizontalCutterActor = vtk.vtkActor()
    horizontalCutterActor.GetProperty().SetColor(colors.GetColor3d('Banana'))
    horizontalCutterActor.GetProperty().SetLineWidth(2)
    horizontalCutterActor.SetMapper(horizontalCutterMapper)

    # Create  cut actor
    verticalCutterActor = vtk.vtkActor()
    verticalCutterActor.GetProperty().SetColor(colors.GetColor3d('Banana'))
    verticalCutterActor.GetProperty().SetLineWidth(2)
    verticalCutterActor.SetMapper(verticalCutterMapper)

    verticalCutterActor2 = vtk.vtkActor()
    verticalCutterActor2.GetProperty().SetColor(colors.GetColor3d('Banana'))
    verticalCutterActor2.GetProperty().SetLineWidth(2)
    verticalCutterActor2.SetMapper(verticalCutterMapper2)



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
    renderer.AddActor(verticalCutterActor)
    renderer.AddActor(verticalCutterActor2)
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
