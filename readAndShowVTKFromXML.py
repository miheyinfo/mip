import vtk
import os

if __name__ == '__main__':

    colors = vtk.vtkNamedColors()

    vtkXMLPolyDataReader = vtk.vtkXMLPolyDataReader()
    vtkXMLPolyDataReader.SetFileName(os.path.join(os.getcwd(), "cut"))
    vtkXMLPolyDataReader.Update()

    # Create model actor
    modelMapper = vtk.vtkPolyDataMapper()
    modelMapper.SetInputConnection(vtkXMLPolyDataReader.GetOutputPort())
    modelMapper.ScalarVisibilityOff()
    modelActor = vtk.vtkActor()
    modelActor.GetProperty().SetColor(colors.GetColor3d('Flesh'))
    modelActor.SetMapper(modelMapper)

    # Create renderers and add actors of plane and model
    renderer = vtk.vtkRenderer()
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