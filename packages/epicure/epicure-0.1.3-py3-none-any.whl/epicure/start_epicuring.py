from napari import current_viewer
from magicgui import magicgui
from napari.utils.history import get_save_history, update_save_history 
import pathlib
import epicure.Utils as ut
from epicure.epicuring import EpiCure
import multiprocessing

"""
   Start EpiCure plugin
   Open the interface to select the movie and associated segmentation to process
"""

def start_epicure():
    hist = get_save_history()
    cdir = hist[0]
    viewer = current_viewer()
    Epic = EpiCure(viewer)
    caxis = None
    cval = 0
    ncpus = int(multiprocessing.cpu_count()*0.5)

    def set_visibility():
        get_files.output_dirname.visible = get_files.advanced_parameters.value
        get_files.show_other_chanels.visible = get_files.advanced_parameters.value
        get_files.process_frames_parallel.visible = get_files.advanced_parameters.value
        get_files.nbparallel_threads.visible = get_files.advanced_parameters.value
        get_files.junction_half_thickness.visible = get_files.advanced_parameters.value
        get_files.verbose_level.visible = get_files.advanced_parameters.value

    def load_movie():
        start_time = ut.start_time()
        nonlocal caxis, cval
        image_file = get_files.image_file.value
        caxis, cval = Epic.load_movie(image_file)
        if caxis is not None:
            get_files.junction_chanel.max = cval-1
            get_files.junction_chanel.visible = True
            set_chanel()
        #get_files.scale_xy.value = Epic.scale
        imgdir = ut.get_directory(image_file)
        get_files.segmentation_file.value = pathlib.Path(imgdir)
        labname = Epic.suggest_segfile( get_files.output_dirname.value )
        if labname is not None:
            get_files.segmentation_file.value = pathlib.Path(labname)
        ut.show_duration(start_time, header="Movie loaded in ")

    def show_others():
        """ Display other chanels from the initial movie """
        for ochan in range(cval):
            ut.remove_layer(viewer, "MovieOtherChanel_"+str(ochan))
        if get_files.show_other_chanels.value == True:
            Epic.add_other_chanels(int(get_files.junction_chanel.value), caxis)

    def set_chanel():
        """ Set the correct chanel that contains the junction signal """
        start_time = ut.start_time()
        Epic.set_chanel(int(get_files.junction_chanel.value), caxis)
        show_others()
        ut.show_duration(start_time, header="Movie chanel loaded in ")


    @magicgui(call_button="Start cure",
            junction_chanel={"widget_type": "Slider", "min":0, "max": 0},
            #scale_xy = {"widget_type": "LiteralEvalLineEdit"},
            #scale_t = {"widget_type": "LiteralEvalLineEdit"},
            junction_half_thickness={"widget_type": "LiteralEvalLineEdit"},
            nbparallel_threads = {"widget_type": "LiteralEvalLineEdit"},
            verbose_level={"widget_type": "Slider", "min":0, "max": 2},
            )
    def get_files( image_file = pathlib.Path(cdir),
                   junction_chanel = 0,
                   segmentation_file = pathlib.Path(cdir),
                   #scale_xy = 1,
                   #scale_t = 1,
                   advanced_parameters = False,
                   show_other_chanels = True,
                   process_frames_parallel = False,
                   nbparallel_threads = ncpus,
                   junction_half_thickness = 1,
                   output_dirname = "epics",
                   verbose_level = 1,
                   ):
        
        print("Starting")
        imname, imdir, outdir = ut.extract_names( image_file, output_dirname )
        update_save_history(imdir)
        ut.remove_widget(viewer, "Start EpiCure (epicure)")
        Epic.process_parallel = process_frames_parallel
        Epic.verbose = verbose_level
        Epic.nparallel = nbparallel_threads
        #Epic.load_segmentation(segmentation_file)
        Epic.set_thickness(junction_half_thickness)
        #Epic.set_scales(scale_xy, scale_t)
        Epic.go_epicure(outdir, segmentation_file)

    set_visibility()
    get_files.junction_chanel.visible = False
    get_files.advanced_parameters.clicked.connect(set_visibility)
    get_files.show_other_chanels.clicked.connect(show_others)
    get_files.image_file.changed.connect(load_movie)
    get_files.junction_chanel.changed.connect(set_chanel)
    return get_files

