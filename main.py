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
    numberOfCuts = 8

    FirstObjPath = r"./MR-Model.obj"

    reader = vtk.vtkOBJReader()
    reader.SetFileName(FirstObjPath)
    reader.Update()

    colors = vtk.vtkNamedColors()

    bounds = reader.GetOutput().GetBounds()
    print(bounds)
    plane = vtk.vtkPlane()
    plane.SetOrigin((bounds[1] + bounds[0]) / 2.0,
                    (bounds[3] + bounds[2]) / 2.0,
                    (bounds[5] + bounds[4]) / 2.0)
    plane.SetNormal(0, 1, 0)

    # Create Scalars.
    scalars = vtk.vtkDoubleArray()
    numberOfPoints = reader.GetOutput().GetNumberOfPoints()
    scalars.SetNumberOfTuples(numberOfPoints)
    pts = reader.GetOutput().GetPoints()
    for i in range(0, numberOfPoints):
        point = pts.GetPoint(i)
        scalars.SetTuple1(i, plane.EvaluateFunction(point))
    reader.GetOutput().GetPointData().SetScalars(scalars)
    reader.GetOutput().GetPointData().GetScalars().GetRange()

    # Create the cutter.

    cutter = vtk.vtkContourFilter()
    cutter.SetInputConnection(reader.GetOutputPort())
    cutter.ComputeScalarsOff()
    cutter.ComputeNormalsOff()
    cutter.GenerateValues(
        numberOfCuts,
        0.99 * reader.GetOutput().GetPointData().GetScalars().GetRange()[0],
        0.99 * reader.GetOutput().GetPointData().GetScalars().GetRange()[1])


    cutterMapper = vtk.vtkPolyDataMapper()
    cutterMapper.SetInputConnection(cutter.GetOutputPort())
    cutterMapper.ScalarVisibilityOff()

    # Create the cut actor.
    cutterActor = vtk.vtkActor()
    cutterActor.GetProperty().SetColor(colors.GetColor3d('Banana'))
    cutterActor.GetProperty().SetLineWidth(2)
    cutterActor.SetMapper(cutterMapper)

    # Create the model actor
    modelMapper = vtk.vtkPolyDataMapper()
    modelMapper.SetInputConnection(reader.GetOutputPort())
    modelMapper.ScalarVisibilityOff()

    modelActor = vtk.vtkActor()
    modelActor.GetProperty().SetColor(colors.GetColor3d('Flesh'))
    modelActor.SetMapper(modelMapper)

    # Create renderers and add the plane and model actors.
    renderer = vtk.vtkRenderer()
    renderer.AddActor(cutterActor)
    renderer.AddActor(modelActor)

    # Add renderer to renderwindow and render
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(600, 600)
    renderWindow.SetWindowName('CutWithCutScalars')

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