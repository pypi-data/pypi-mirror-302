from zipfile import ZipFile 
import gdown
import configparser
import os

image_dict = {
            'WashingtonDC': ['WashingtonDC_Ref_156bands', '13NGtcTWsViteI1J46IDXldlMPPOnTNLz', 'spectral_images', 'WashingtonDC_Ref_156bands/WashingtonDC_Ref_156bands'],
            'MicroscenePolymers': ['Microscene_Polymers', '1SjIToGJwkkWyBZER5Wv-1v1-I22Y-EBI', 'spectral_images', 'Microscene_Polymers/reflectance_image_polymers'],
            'FabricVehicleDetecitonRIT': ['Detection_Test_Cooke_City_RIT', '1TxTiM98Fc-D5_ZBFlOlceR0lXdH5qqEo', 'spectral_images', 'Detection_Test_Cooke_City_RIT/self_test/self_test/HyMap/self_test_refl.img'],
            'VegBaccharisUPWINS': ['Vegetation_Baccharis_halmifolia_UPWINS', '1e5SloCAzXGIfDRlzhqYcmQ5JUMC8DweC', 'spectral_images', 'Vegetation_Baccharis_halmifolia_UPWINS/Morven_Baccharis_h_or_ref'],
            'PaintDetectionUPWINS': ['Morven_paint_samples_or_ref', '1WX_efoG5iIIYjg5Juh9tDz-Tk1BrElrk', 'spectral_images', 'Morven_paint_samples_or_ref/Morven_paint_samples_or_ref'],
            'indian_pines': ['indian_pines', '1d_348BZxHhWWhwo3Rt7jIo-hemG-FuWB', 'spectral_images', 'indian_pines/indian_pines'],
            'pavia_centre': ['pavia_centre', '1x3RJ2J_FzX-1wkmtmga7BvAZEwYt0_EY', 'spectral_images', 'pavia_centre/pavia_centre'],
            'pavia_university': ['pavia_university', '1ohdtA-0XGKRVSb5L9HfNHonBlTal1dIG', 'spectral_images', 'pavia_university/pavia_university']
}

lib_dict = {
            'GHISACONUS_2008': ['GHISACONUS_2008_001_speclib', '1b6XvgY46n-Dm8Df2QRiC1vE9Z7PA0VIa', 'spectral_libraries', 'GHISACONUS_2008_001_speclib/GHISACONUS_2008_001_speclib_orig.csv'],
            'MicroscenePolymersLibrary': ['Microscene_Polymers_Library', '1WbG1xCgs4mhNth30-IRinrGIzT1W_Anh', 'spectral_libraries', 'Microscene_Polymers_Library/Polymers Full.sli'],
            'UPWINS_4_16_2024': ['UPWINS_4_16_2024', '11Zn-DxlVevtg-KAKnDRiPEVxnLYXDl5h', 'spectral_libraries', 'UPWINS_4_16_2024/UPWINS_4_16_2024.sli']
}

data_dict = {**image_dict, **lib_dict}

def available_datasets():
    print('Available Images:')
    for key in image_dict.keys():
        print('   '+key)
    print('Available Spectral Libraries:')
    for key in lib_dict.keys():
        print('   '+key)
        

def get_fname(data_name):
    # get the main directory for storing data
    data_dir = get_data_dir()
    # read the information for the requested image from the dict
    fname, fid, file_type, data_fname = data_dict[data_name]
    # get the full filename with path
    data_fname = os.path.join(data_dir,file_type, data_fname)    
    # print and return the full filename
    print('Primary Image Filename:')
    print(data_fname)
    return data_fname

   
def get_data_dir():    
    home_dir = os.environ.get('HOME')  # For Linux/macOS
    if home_dir is None:
        home_dir = os.environ.get('USERPROFILE')  # For Windows
    fname_config = home_dir+'/hsi_data_config.ini'
    
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    # Read the configuration file
    if os.path.isfile(fname_config):
        config.read(fname_config)
    else:
        set_data_dir('.')
        config.read(fname_config)
    # Access the data dir value from the configuration file
    data_dir = config.get('General', 'data_dir')
    #print(f'Directory for storing spectral image, libraries, and metadata: {data_dir}')
    return data_dir
    
                                
def set_data_dir(data_dir):
    home_dir = os.environ.get('HOME')  # For Linux/macOS
    if home_dir is None:
        home_dir = os.environ.get('USERPROFILE')  # For Windows
    fname_config = home_dir+'/hsi_data_config.ini'
    
    try:
        config = configparser.ConfigParser()
        # Add sections and key-value pairs
        config['General'] = {'data_dir': data_dir}
        # Write the configuration to a file
        with open(fname_config, 'w') as configfile:
            config.write(configfile)   
    except: 
        print('Directory value not valid.')        
        config = configparser.ConfigParser()
        # Add sections and key-value pairs
        config['General'] = {'data_dir': '.'}
        # Write the configuration to a file
        with open(fname_config, 'w') as configfile:
            config.write(configfile)      
            
class download:
    def __init__(self, data_name):
        self.data_dict = data_dict        
        self.data_dir = get_data_dir()
        
        try:
            # determine the file information
            fname, fid, file_type, self.data_fname = self.data_dict[data_name]   
            
            # create the subdirectory for the filetype if needed
            self.subdir_filetype = os.path.join(self.data_dir,file_type)
            if not os.path.isdir(self.subdir_filetype):
                os.mkdir(self.subdir_filetype) 
            
            # create the name of the directory where this data wil lbe stored
            self.subdir_data = os.path.join(self.subdir_filetype,fname)
            
            self.download_unzip(fname, fid);
            
        except:
            print('No data downloaded.  Available datasets are:')
            available_datasets()
            
            
    def download_unzip(self, fname, fid):
        
        # dorwnload and unzip the files if the directory for these files does not exist
        if not os.path.isdir(self.subdir_data):
            # Download the zip files of the image into the  subdirectory for the filetype
            fnameZip = os.path.join(self.subdir_filetype, fname+'.zip')
            if not os.path.isfile(fnameZip):
                gdown.download(id=fid, output=fnameZip)
            else:
                print(f'File {fnameZip} exists.')
            
            # Unzip the images into the directory for this data
            with ZipFile(fnameZip, 'r') as zObject: 
                zipped_filenames = zObject.namelist()
                zObject.extractall( 
                    path=os.path.join(self.subdir_data) ) 
            for zfname in zipped_filenames:
                print(f'File saved as: {os.path.join(self.subdir_data,zfname)}')
            
            # Delete the zip file
            os.remove(fnameZip)
            print(' ')
        
        print('Available Files:')
        for dirpath,_,filenames in os.walk(self.subdir_data):
            for f in filenames:
                print(os.path.abspath(os.path.join(dirpath, f)))
        
    
