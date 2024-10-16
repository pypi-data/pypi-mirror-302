from zipfile import ZipFile 
import gdown
import os
import configparser




        

class download:
    def __init__(self, data_name):
        self.create_config(self)
        self.read_settings(self)
        
        # Dictionary to hold filenmae-id-data_type information
        self.image_dict = {
            'WashingtonDC': ['WashingtonDC_Ref_156bands', '13NGtcTWsViteI1J46IDXldlMPPOnTNLz', 'image'],
            'MicroscenePolymers': ['Microscene_Polymers', '1SjIToGJwkkWyBZER5Wv-1v1-I22Y-EBI', 'image'],
            'FabricVehicleDetecitonRIT': ['Detection_Test_Cooke_City_RIT', '1TxTiM98Fc-D5_ZBFlOlceR0lXdH5qqEo', 'image'],
            'VegBaccharisUPWINS': ['Vegetation_Baccharis_halmifolia_UPWINS', '1e5SloCAzXGIfDRlzhqYcmQ5JUMC8DweC', 'image'],
            'PaintDetectionUPWINS': ['Vegetation_Baccharis_halmifolia_UPWINS', '1WX_efoG5iIIYjg5Juh9tDz-Tk1BrElrk', 'image']
        }
        
        https://drive.google.com/file/d//view?usp=drive_link
        https://drive.google.com/file/d//view?usp=drive_link
        # determine the file information
        fname, fid, file_type = self.image_dict[data_name]
        
        # Check if the spectral image or librRY directory exists, and create it if needed
        if file_type=='image':
            if not os.path.isdir('spectral_images'):
                os.mkdir('spectral_images')  
        if file_type=='library':
            if not os.path.isdir('spectral_libraries'):
                os.mkdir('spectral_libraries')  
        
        self.download_unzip(fname, fid);
        
    
    def read_settings(self):
        # Create a ConfigParser object
        config = configparser.ConfigParser()

        # Read the configuration file
        config.read('config.ini')

        # Access values from the configuration file
        debug_mode = config.getboolean('General', 'debug')
        log_level = config.get('General', 'log_level')
        db_name = config.get('Database', 'db_name')
        db_host = config.get('Database', 'db_host')
        db_port = config.get('Database', 'db_port')

        # Return a dictionary with the retrieved values
        config_values = {
            'debug_mode': debug_mode,
            'log_level': log_level,
            'db_name': db_name,
            'db_host': db_host,
            'db_port': db_port
        }
            
        # Print the retrieved values
        print(config_values['debug_mode'])
        print(sonfig_values['log_level'])
        print(config_values['db_name'])
        print(config_values['db_host'])
        print(config_values['db_port'])
        
                                    
    def create_config(self):
        config = configparser.ConfigParser()
        # Add sections and key-value pairs
        config['General'] = {'debug': True, 'log_level': 'info'}
        config['Database'] = {'db_name': 'example_db',
                            'db_host': 'localhost', 'db_port': '5432'}
        # Write the configuration to a file
        with open('config.ini', 'w') as configfile:
            config.write(configfile)           
            
            
    def download_unzip(self, fname, fid):
            
        if not os.path.isdir('spectral_images/'+fname):
            # Download the zip files of the image.
            fnameZip = 'spectral_images/'+fname+'.zip'
            if not os.path.isfile(fnameZip):
                gdown.download(id=fid, output=fnameZip)
            else:
                print(f'File {fnameZip} exists.')
            
            # Unzip the images
            with ZipFile(fnameZip, 'r') as zObject: 
                zipped_filenames = zObject.namelist()
                zObject.extractall( 
                    path='spectral_images/'+fname) 
            for zfname in zipped_filenames:
                print(f'File saved as: spectral_images/{fname}/{zfname}')
            
            # Delete the zip file
            os.remove(fnameZip)
    
    
    
    