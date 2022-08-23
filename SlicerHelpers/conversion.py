def convert_ras_to_ijk(main_volume_label: str='cts', landmarks_list_label: str = "landmarks"):
    import numpy as np
    volume_node = getNode(main_volume_label)
    landmarks_nodes = getNode(landmarks_list_label)
    landmarks_amount = landmarks_nodes.GetNumberOfMarkups() 
    point_Ras = [0, 0, 0, 1]
    for landmark_index in range(landmarks_amount):
        landmarks_nodes.GetNthFiducialWorldCoordinates(landmark_index, point_Ras)
        transformRasToVolumeRas = vtk.vtkGeneralTransform()
        slicer.vtkMRMLTransformNode.GetTransformBetweenNodes(None, volume_node.GetParentTransformNode(), transformRasToVolumeRas)
        point_VolumeRas = transformRasToVolumeRas.TransformPoint(point_Ras[0:3])
        volume_RasToIjk = vtk.vtkMatrix4x4()
        volume_node.GetRASToIJKMatrix(volume_RasToIjk)
        point_Ijk = [0, 0, 0, 1]
        volume_RasToIjk.MultiplyPoint(np.append(point_VolumeRas, 1.0), point_Ijk)
        point_Ijk = [round(c) for c in point_Ijk[0:3]]
        landmarks_nodes.SetNthControlPointDescription(landmark_index, ','.join(str(e) for e in point_Ijk))
        landmark_label = landmarks_nodes.GetNthMarkupLabel(landmark_index)
        print(f"{landmark_label}: {point_Ijk}")

def convert_ijk_to_ras(landmark_in_ijk: tuple, main_volume_label: str='cts'):
    import numpy as np
    volumeNode = getNode(main_volume_label)
    # Get physical coordinates from voxel coordinates
    volume_ijk_to_ras = vtk.vtkMatrix4x4()
    volumeNode.GetIJKToRASMatrix(volume_ijk_to_ras)
    point_VolumeRas = [0, 0, 0, 1]
    volume_ijk_to_ras.MultiplyPoint(np.append(landmark_in_ijk, 1.0), point_VolumeRas)
    # If volume node is transformed, apply that transform to get volume's RAS coordinates
    transformVolumeRasToRas = vtk.vtkGeneralTransform()
    slicer.vtkMRMLTransformNode.GetTransformBetweenNodes(volumeNode.GetParentTransformNode(), None, transformVolumeRasToRas)
    point_Ras = transformVolumeRasToRas.TransformPoint(point_VolumeRas[0:3])
    # print landmark in ras coordinates
    print(point_Ras)
