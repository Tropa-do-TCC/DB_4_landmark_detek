def convert_ras_to_ijk(main_volume_label: str, landmarks_list_label: str = "landmarks"):
    volumeNode = getNode(main_volume_label)  # main volume label
    landmarksNodes = getNode(landmarks_list_label)  # landmarks list label
    point_Ras = [0, 0, 0, 1]
    for landmarkIndex, landmark in enumerate(landmarksNodes):
        landmarksNodes.GetNthFiducialWorldCoordinates(landmarkIndex, point_Ras)
        # If volume node is transformed, apply that transform to get volume's RAS coordinates
        transformRasToVolumeRas = vtk.vtkGeneralTransform()
        slicer.vtkMRMLTransformNode.GetTransformBetweenNodes(None, volumeNode.GetParentTransformNode(), transformRasToVolumeRas)
        point_VolumeRas = transformRasToVolumeRas.TransformPoint(point_Ras[0:3])
        # Get voxel coordinates from physical coordinates
        volumeRasToIjk = vtk.vtkMatrix4x4()
        volumeNode.GetRASToIJKMatrix(volumeRasToIjk)
        point_Ijk = [0, 0, 0, 1]
        volumeRasToIjk.MultiplyPoint(np.append(point_VolumeRas, 1.0), point_Ijk)
        point_Ijk = [int(round(c)) for c in point_Ijk[0:3]]
        # Print output
        print(f"{landmark.Label}: point_Ijk")

def convert_ijk_to_ras(main_volume_label: str, landmark_in_ijk: tuple):
    volumeNode = getNode(main_volume_label)
    # Get physical coordinates from voxel coordinates
    volumeIjkToRas = vtk.vtkMatrix4x4()
    volumeNode.GetIJKToRASMatrix(volumeIjkToRas)
    point_VolumeRas = [0, 0, 0, 1]
    volumeIjkToRas.MultiplyPoint(np.append(landmark_in_ijk, 1.0), point_VolumeRas)
    # If volume node is transformed, apply that transform to get volume's RAS coordinates
    transformVolumeRasToRas = vtk.vtkGeneralTransform()
    slicer.vtkMRMLTransformNode.GetTransformBetweenNodes(volumeNode.GetParentTransformNode(), None, transformVolumeRasToRas)
    point_Ras = transformVolumeRasToRas.TransformPoint(point_VolumeRas[0:3])
    # print landmark in ras coordinates
    print(point_Ras)
