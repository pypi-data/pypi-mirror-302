import struct
import matplotlib.pyplot as plt
import sys

def read_bin_spectra(file_name):
    histos = []
    delta_e = 0

    with open(file_name, 'rb') as fin:
        # Read the number of voxels in structures
        n_voxels_in_structures = struct.unpack('i', fin.read(4))[0]
        print(f'nVoxelsInStructures: {n_voxels_in_structures}')


        # Read deltaE
        delta_e = struct.unpack('f', fin.read(4))[0]
        print(f'deltaE: {delta_e}')
        # Read arrayStruct
        array_struct = struct.unpack(f'{n_voxels_in_structures}i', fin.read(n_voxels_in_structures * 4))
        # Read spectraPointers
        spectra_pointers = struct.unpack(f'{n_voxels_in_structures}i', fin.read(n_voxels_in_structures * 4))
        # Read histograms
        for i in range(n_voxels_in_structures):
            if spectra_pointers[i] > 0:
                fin.seek(spectra_pointers[i])
                n_bins = struct.unpack('i', fin.read(4))[0]
                if n_bins < 1:
                    continue
                entries = struct.unpack(f'{n_bins}i', fin.read(n_bins * 4))
                histos.append(entries)

    return histos, delta_e
