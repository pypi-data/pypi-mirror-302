from zipfile import ZipFile 
import gdown
import os
import configparser
from pathlib import Path

        

class download:
    def __init__(self, data_name):
        self.dir_home = Path.home()
        self.get_data_dir()
        
        # Dictionary to hold filenmae-id-data_type information
        self.image_dict = {
            'WashingtonDC': ['WashingtonDC_Ref_156bands', '13NGtcTWsViteI1J46IDXldlMPPOnTNLz', 'image', 'WashingtonDC_Ref_156bands\WashingtonDC_Ref_156bands'],
            'MicroscenePolymers': ['Microscene_Polymers', '1SjIToGJwkkWyBZER5Wv-1v1-I22Y-EBI', 'image', 'Microscene_Polymers\reflectance_image_polymers'],
            'FabricVehicleDetecitonRIT': ['Detection_Test_Cooke_City_RIT', '1TxTiM98Fc-D5_ZBFlOlceR0lXdH5qqEo', 'image', 'Detection_Test_Cooke_City_RIT\self_test\self_test\HyMap\self_test_refl.img'],
            'VegBaccharisUPWINS': ['Vegetation_Baccharis_halmifolia_UPWINS', '1e5SloCAzXGIfDRlzhqYcmQ5JUMC8DweC', 'image', 'Vegetation_Baccharis_halmifolia_UPWINS\Morven_Baccharis_h_or_ref'],
            'PaintDetectionUPWINS': ['Morven_paint_samples_or_ref', '1WX_efoG5iIIYjg5Juh9tDz-Tk1BrElrk', 'image', 'Morven_paint_samples_or_ref/Morven_paint_samples_or_ref']
        }
        
        try:
            # determine the file information
            fname, fid, file_type, self.data_fname = self.image_dict[data_name]
            
            # Check if the spectral image or librRY directory exists, and create it if needed
            if file_type=='image':
                if not os.path.isdir('spectral_images'):
                    os.mkdir('spectral_images')  
            if file_type=='library':
                if not os.path.isdir('spectral_libraries'):
                    os.mkdir('spectral_libraries')  
            
            self.download_unzip(fname, fid);
            
        except:
            print('No data downloaded.  Available datasets are:')
            for key in self.image_dict.keys():
                print(key)
    
    def get_fname(self):
        return self.data_fname
        
    
    def get_data_dir(self):    
        # Create a ConfigParser object
        config = configparser.ConfigParser()
        # Read the configuration file
        if os.path.isfile(self.dir_home/'hsi_data_config.ini'):
            config.read(self.dir_home/'hsi_data_config.ini')
        else:
            self.set_data_dir('.')
            config.read(self.dir_home/'hsi_data_config.ini')
        # Access the data dir value from the configuration file
        self.data_dir = config.get('General', 'data_dir')
        
                                    
    def set_data_dir(self, data_dir):
        try:
            config = configparser.ConfigParser()
            # Add sections and key-value pairs
            config['General'] = {'data_dir': data_dir}
            # Write the configuration to a file
            with open(self.dir_home/'hsi_data_config.ini', 'w') as configfile:
                config.write(configfile)   
        except: 
            print('Directory value not valid.')        
            config = configparser.ConfigParser()
            # Add sections and key-value pairs
            config['General'] = {'data_dir': '.'}
            # Write the configuration to a file
            with open(self.dir_home/'hsi_data_config.ini', 'w') as configfile:
                config.write(configfile)   
            
            
    def download_unzip(self, fname, fid):
            
        if not os.path.isdir('spectral_images/'+fname):
            # Download the zip files of the image.
            fnameZip = self.data_dir+'/'+'spectral_images/'+fname+'.zip'
            if not os.path.isfile(fnameZip):
                gdown.download(id=fid, output=fnameZip)
            else:
                print(f'File {fnameZip} exists.')
            
            # Unzip the images
            with ZipFile(fnameZip, 'r') as zObject: 
                zipped_filenames = zObject.namelist()
                zObject.extractall( 
                    path=self.data_dir+'/'+'spectral_images/'+fname) 
            for zfname in zipped_filenames:
                print(f'File saved as: {self.data_dir}/spectral_images/{fname}/{zfname}')
            
            # Delete the zip file
            os.remove(fnameZip)
    
