import numpy as np
import os, time, pickle
import napari
from qtpy.QtWidgets import QPushButton, QVBoxLayout, QTabWidget, QWidget
from napari.utils import progress
from magicgui.widgets import TextEdit
from skimage.segmentation import find_boundaries, watershed
from skimage.measure import label
from skimage.morphology import skeletonize, binary_closing, binary_opening
from skimage.util import apply_parallel
from skimage.measure import regionprops, regionprops_table
from multiprocessing.pool import ThreadPool as Pool
import pandas as pand

import epicure.Utils as ut
from epicure.editing import Editing
from epicure.tracking import Tracking
from epicure.suspecting import Suspecting
from epicure.outputing import Outputing
from epicure.displaying import Displaying

"""
    EpiCure main
    Open and initialize the files
    Launch the main widget composed of the segmentation and tracking editing features
"""

class EpiCure():
    
    def __init__(self, viewer=None):
        self.viewer = viewer
        if self.viewer is None:
            self.viewer = napari.Viewer(show=False)
        self.viewer.title = "Napari - EpiCure"
        self.img = None
        self.suspecting = None
        self.others = None
        self.imgshape2D = None    ## width, height of the image
        self.nframes = None       ## Number of time frames
        self.thickness = 4 ## thickness of junctions, wider
        self.minsize = 4   ## smallest number of pixels in a cell
        self.verbose = 1   ## level of printing messages (None/few, normal, debug mode)

        self.overtext = dict()
        self.help_index = 1   ## current display index of help overlay
        self.blabla = None    ## help window
        self.groups = {}
        self.tracked = 0 ## has done a tracking
        self.process_parallel = False ## Do some operations in parallel (n frames in parallel)
        self.nparallel = 4      ## number of parallel threads
        self.dtype = np.uint32  ## label type, default 32 but if less labels, reduce it
        self.outputing = None   ## non initialized yet


    def set_thickness( self, thick ):
        """ Thickness of junctions (half thickness) """
        self.thickness = thick

    def load_movie(self, imgpath):
        """ Load the intensity movie, and get metadata """
        self.imgpath = imgpath
        self.img, self.scale, nchan = ut.opentif( self.imgpath, verbose=self.verbose>1 )
        ## transform static image to movie (add temporal dimension)
        if len(self.img.shape) == 2:
            self.img = np.expand_dims(self.img, axis=0)
        caxis = None
        cval = 0
        if nchan>0 or len(self.img.shape) > 3:
            if nchan > 0 and len(self.img.shape) > 3:
                ## multiple chanels and multiple slices, order axis should be TCXY
                caxis = 1
                cval = nchan
            else:
                ## image has multiple chanels
                minshape = min(self.img.shape)
                caxis = self.img.shape.index(minshape)
                cval = minshape
            self.mov = self.img

        ## display the movie
        ut.remove_layer(self.viewer, "Movie")
        mview = self.viewer.add_image( self.img, name="Movie", blending="additive", colormap="gray" )
        mview.contrast_limits = self.quantiles()
        mview.gamma = 0.95
        
        self.imgshape = self.viewer.layers["Movie"].data.shape
        self.imgshape2D = self.imgshape[1:3]
        self.nframes = self.imgshape[0]
        return caxis, cval

    def quantiles(self):
        return tuple(np.quantile(self.img, [0.01, 0.9999]))

    def set_scales( self, scalexy, scalet ):
        """ Set the scaling units for outputs """
        self.scale = scalexy
        self.scale_time = scalet
        ut.show_info("Movie scales set to "+str(self.scale)+" (in x,y) and "+str(self.scale_time)+" (in time)")

    def set_chanel( self, chan, chanaxis ):
        """ Update the movie to the correct chanel """
        self.img = np.rollaxis(np.copy(self.mov), chanaxis, 0)[chan]
        if self.viewer is not None:
            mview = self.viewer.layers["Movie"]
            mview.data = self.img
            mview.contrast_limits=self.quantiles()
            mview.gamma=0.95
            mview.refresh()

    def add_other_chanels(self, chan, chanaxis): 
        """ Open other channels if option selected """
        self.others = np.delete(self.mov, chan, axis=chanaxis)
        self.others_chanlist = []
        if self.others is not None:
            self.others = np.rollaxis(self.others, chanaxis, 0)
            for ochan in range(self.others.shape[0]):
                purechan = ochan
                if purechan >= chan:
                    purechan = purechan + 1
                self.others_chanlist.append(purechan)
                mview = self.viewer.add_image( self.others[ochan], name="MovieOtherChanel_"+str(purechan), blending="additive", colormap="gray" )
                mview.contrast_limits=tuple(np.quantile(self.others[ochan],[0.01, 0.9999]))
                mview.gamma=0.95
                mview.visible = False
        
    def load_segmentation(self, segpath):
        """ Load the segmentation file """
        start_time = ut.start_time()
        self.segpath = segpath
        self.seg,_, _ = ut.opentif( self.segpath, verbose=self.verbose>1 )
        self.seg = np.uint32(self.seg)
        ## transform static image to movie (add temporal dimension)
        if len(self.seg.shape) == 2:
            self.seg = np.expand_dims(self.seg, axis=0)
        ## ensure that the shapes are correctly set
        self.imgshape = self.seg.shape
        self.imgshape2D = self.seg.shape[1:3]
        self.nframes = self.seg.shape[0]
        ## if the segmentation is a junction file, transform it to a label image 
        if ut.is_binary(self.seg):
            self.junctions_to_label()
            self.tracked = 0
        else:
            self.has_been_tracked()
            self.thin_boundaries()

        if np.max(self.seg) < 50000:
            self.dtype = np.uint16
            self.seg = np.uint16(self.seg)
        
        # display the segmentation file movie
        if self.viewer is not None:
            self.seglayer = self.viewer.add_labels( self.seg, name="Segmentation", blending="additive", opacity=0.5 )
            self.viewer.dims.set_point(0,0)
            self.seglayer.brush_size = 4 ## default label pencil drawing size 
        if self.verbose > 0:
            ut.show_duration(start_time, header="Segmentation loaded in ")

    def load_tracks( self, progress_bar ):
        """ From the segmentation, get all the metadata """
        tracked = "tracked"
        self.tracking.init_tracks()
        if self.tracked == 0:
            tracked = "untracked"
        else:
            progress_bar.set_description( "check and fix track gaps" )
            self.handle_gaps( track_list=None, verbose=1 )
        ut.show_info(""+str(len(self.tracking.get_track_list()))+" "+tracked+" cells loaded")


    def has_been_tracked(self):
        """ Look if has been tracked already (some labels are in several frames) """
        nb = 0
        for frame in range(self.seg.shape[0]):
            if frame > 0:
                inter = np.intersect1d(np.unique(self.seg[frame-1]), np.unique(self.seg[frame]))
                if len(inter)>1:
                    self.tracked = 1 
                    return
        self.tracked = 0
        return

    def suggest_segfile(self, outdir):
        """ Check if a segmentation file from EpiCure already exists """
        imgname, imgdir, out = ut.extract_names( self.imgpath, outdir, mkdir=False )
        return ut.suggest_segfile(out, imgname)

    def outname(self):
        return os.path.join(self.outdir, self.imgname)

    def set_names(self, outdir):
        """ Extract default names from imgpath """
        self.imgname, self.imgdir, self.outdir = ut.extract_names( self.imgpath, outdir, mkdir=True )

    def go_epicure(self, outdir, segmentation_file):
        """ Initialize everything and start the main widget """
        self.set_names( outdir )
        
        self.viewer.window._status_bar._toggle_activity_dock(True)
        progress_bar = progress(total=5)
        progress_bar.set_description( "Reading segmented image" )
        ## load the segmentation
        self.load_segmentation( segmentation_file )
        progress_bar.update(1)
        ut.set_active_layer( self.viewer, "Segmentation" )
        
        ## setup the main interface and shortcuts
        start_time = ut.start_time()
        progress_bar.set_description( "Active EpiCure shortcuts" )
        self.key_bindings()
        progress_bar.update(2)
        progress_bar.set_description( "Prepare widget" )
        self.main_widget()
        progress_bar.update(3)
        progress_bar.set_description( "Load tracks" )
        self.load_tracks( progress_bar )
        progress_bar.update(4)

        ## load graph if it exists
        epiname = os.path.join( self.outdir, self.imgname+"_epidata.pkl" )
        if os.path.exists(epiname):
            progress_bar.set_description( "Load EpiCure informations" )
            self.load_epicure_data(epiname)
        if self.verbose > 0:
            ut.show_duration(start_time, header="Tracks and graph loaded in ")
        progress_bar.update(5)
        progress_bar.close()
        self.viewer.window._status_bar._toggle_activity_dock(False)
    
    def main_widget(self):
        """ Open the main widget interface """
        main_widget = QWidget()
        
        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.setObjectName("main")
        layout.addWidget(tabs)
        main_widget.setLayout(layout)
        
        self.editing = Editing(self.viewer, self)
        tabs.addTab( self.editing, "Edit" )
        self.suspecting = Suspecting(self.viewer, self)
        tabs.addTab( self.suspecting, "Suspect" )
        self.tracking = Tracking(self.viewer, self)
        tabs.addTab( self.tracking, "Track" )
        self.outputing = Outputing(self.viewer, self)
        tabs.addTab( self.outputing, "Output" )
        self.display = Displaying(self.viewer, self)
        tabs.addTab( self.display, "Display" )
        main_widget.setStyleSheet('QPushButton {background-color: rgb(40, 60, 75)} QCheckBox::indicator {background-color: rgb(40,52,65)}')

        self.viewer.window.add_dock_widget( main_widget, name="Main" )

    def key_bindings(self):
        """ Activate shortcurs """
        self.text = "-------------- ShortCuts -------------- \n "
        self.text = self.text + "If Segmentation layer is active: \n"
        self.text = self.text + "  <h> show/next/hide this help message \n"
        self.text = self.text + "  <a> show ALL shortcuts in separate window \n"
        self.text = self.text + "  <s> save the updated segmentation \n"
        self.text = self.text + "  <Shift-s> save the movie with current display \n"
        self.text = self.text + "\n"
        
        if self.verbose > 0:
            print("Activating key shortcuts on segmentation layer")
            print("Press several times <h> to show all the shortcuts list or hide it")
        ut.setOverlayText(self.viewer, self.text, size=10)
        
        @self.seglayer.bind_key('h', overwrite=True)
        def switch_shortcuts(seglayer):
            index = (self.help_index+1)%(len(self.overtext.keys())+1)
            self.switchOverlayText(index)
        
        @self.seglayer.bind_key('a', overwrite=True)
        def list_all_shortcuts(seglayer):
            self.switchOverlayText(0)   ## hide display message in main window
            text = "**************** EPICURE *********************** \n"
            text += "\n"
            text += self.text
            text += "\n"
            text += ut.napari_shortcuts()
            for key, val in self.overtext.items():
                text += "\n"
                text += val
            self.update_text_window(text) 
        
        @self.seglayer.bind_key('s', overwrite=True)
        def save_seglayer(seglayer):
            self.save_epicures()
        
        @self.viewer.bind_key('Shift-s', overwrite=True)
        def save_movie(seglayer):
            endname = "_frames.tif"
            outname = os.path.join( self.outdir, self.imgname+endname )
            self.save_movie(outname)

########### Texts 

    def switchOverlayText(self, index):
        """ Switch overlay display text to index """
        self.help_index = index
        if index == 0:
            ut.showOverlayText(self.viewer, vis=False)
            return
        else:
            ut.showOverlayText(self.viewer, vis=True)
        self.setCurrentOverlayText()

    def init_text_window(self):
        """ Create and display help text window """
        self.blabla = TextEdit()
        self.blabla.name = "Epicure shortcuts"
        self.blabla.show()

    def update_text_window(self, message):
        """ Update message in separate window """
        if self.blabla is None:
            self.init_text_window()
        self.blabla.value = message

    def setCurrentOverlayText(self):
        """ Set overlay help text message to current selected options list """
        text = self.text
        dispkey = list(self.overtext.keys())[self.help_index-1]
        text += self.overtext[dispkey]
        ut.setOverlayText(self.viewer, text, size=10)
    
    def get_summary(self):
        """ Get a summary of the infos of the movie """
        summ = "----------- EpiCure summary ----------- \n"
        summ += "--- Image infos \n"
        summ += "Movie name: "+str(self.imgpath)+"\n"
        summ += "Movie size (x,y): "+str(self.imgshape2D)+"\n"
        if self.nframes is not None:
            summ += "Nb frames: "+str(self.nframes)+"\n"
        summ += "\n"
        summ += "--- Segmentation infos \n"
        summ += "Segmentation file: "+str(self.segpath)+"\n"
        summ += "Nb tracks: "+str(len(self.tracking.get_track_list()))+"\n"
        tracked = "yes"
        if self.tracked == 0:
            tracked = "no"
        summ += "Tracked: "+tracked+"\n"
        nb_labels, mean_duration, mean_area = ut.summary_labels( self.seg )
        summ += "Nb cells: "+str( nb_labels )+"\n"
        summ += "Average track lengths: "+str(mean_duration)+" frames\n"
        summ += "Average cell area: "+str(mean_area)+" pixels^2\n"
        summ += "Nb suspect tracks: "+str(self.suspecting.nb_suspects())+"\n"
        summ += "\n"
        summ += "--- Parameter infos \n"
        summ += "Junction thickness: "+str(self.thickness)+"\n"
        return summ

    def set_contour( self, width ):
        self.seglayer.contour = width

############ Layers

    def check_layers(self):
        """ Check that the necessary layers are present """
        if self.editing.shapelayer_name not in self.viewer.layers:
            if self.verbose > 0:
                print("Reput shape layer")
            self.editing.create_shapelayer()
        if self.suspecting.suspectlayer_name not in self.viewer.layers:
            if self.verbose > 0:
                print("Reput suspect layer")
            self.suspecting.create_suspectlayer()
        if "Movie" not in self.viewer.layers:
            if self.verbose > 0:
                print("Reput movie layer")
            mview = self.viewer.add_image( self.img, name="Movie", blending="additive", colormap="gray" )
            #mview.reset_contrast_limits()
            mview.contrast_limits=self.quantiles()
            mview.gamma=0.95
        if "Segmentation" not in self.viewer.layers:
            if self.verbose > 0:
                print("Reput segmentation")
            self.seglayer = self.viewer.add_labels( self.seg, name="Segmentation", blending="additive", opacity=0.5 )

        self.finish_update()


    def finish_update(self, contour=None):
        if contour is not None:
            self.seglayer.contour = contour
        ut.set_active_layer( self.viewer, "Segmentation" )
        self.seglayer.refresh()
        duplayers = ["PrevSegmentation"]
        for dlay in duplayers:
            if dlay in self.viewer.layers:
                (self.viewer.layers[dlay]).refresh()
        
    def save_epicures( self, imtype="float32" ):
        outname = os.path.join( self.outdir, self.imgname+"_labels.tif" )
        ut.writeTif(self.seg, outname, self.scale, imtype, what="Segmentation")
        epiname = os.path.join( self.outdir, self.imgname+"_epidata.pkl" )
        outfile = open(epiname, "wb")
        if self.groups is not None:
            pickle.dump(self.groups, outfile)
        else:
            pickle.dump({}, outfile)
        if self.tracking.graph is not None:
            pickle.dump(self.tracking.graph, outfile)
        else:
            pickle.dump({}, outfile)
        if self.suspecting is not None and self.suspecting.suspects is not None:
            if self.suspecting.suspects.data is not None:
                pickle.dump(self.suspecting.suspects.data, outfile)
            else:
                pickle.dump(None, outfile)
            pickle.dump(self.suspecting.suspects.properties, outfile)
            pickle.dump(self.suspecting.suspicions, outfile)
            pickle.dump(self.suspecting.suspects.symbol, outfile)
            pickle.dump(self.suspecting.suspects.face_color, outfile)
        outfile.close()
    
    def read_group_data( self, infile ):
        """ Read the group EpiCure data from opened file """
        try:
            groups = pickle.load(infile)
            if self.verbose > 0:
                print("Loaded cell groups info: "+str(groups))
            return groups
        except:
            if self.verbose > 1:
                print("No group infos found")
            return None

    def read_graph_data( self, infile ):
        """ Read the graph EpiCure data from opened file """
        try:
            graph = pickle.load(infile)
            if self.verbose > 0:
                print("Graph (lineage) loaded")
            return graph
        except:
            if self.verbose > 1:
                print("No graph infos found")
            return None

    def read_suspicions_data(self, infile):
        """ Read info of EpiCure suspicions from opened file """
        try:
            suspects_pts = pickle.load(infile)
            if suspects_pts is not None:
                suspects_props = pickle.load(infile)
                suspicions = pickle.load(infile)
                try:
                    symbols = pickle.load(infile)
                    colors = pickle.load(infile)
                except: 
                    if self.verbose > 1:
                        print("No suspects display info found")
                    symbols = None
                    colors = None
                return suspects_pts, suspects_props, suspicions, symbols, colors
            else:
                return None, None, None, None, None
        except:
            if self.verbose > 1:
                print("Suspects info not complete")
            return None, None, None, None, None

    def load_epicure_data(self, epiname):
        """ Load saved infos from file """
        infile = open(epiname, "rb")
        ## Load groups information
        self.groups = self.read_group_data( infile )
        self.outputing.update_selection_list()
        ## Load graph (lineage) informations
        self.tracking.graph = self.read_graph_data( infile )
        if self.tracking.graph is not None:
            self.tracking.tracklayer.refresh()
        ## Load suspects information 
        pts, props, suspicions, symbols, colors = self.read_suspicions_data( infile )
        if pts is not None:
            if len(pts) > 0:
                self.suspecting.load_suspects(pts, props, suspicions, symbols, colors)
                if len(pts) > 0 and self.verbose > 0:
                    print("Suspects loaded")
                    ut.show_info("Loaded "+str(len(pts))+" suspects")
        infile.close()

    def save_movie(self, outname):
        """ Save movie with current display parameters, except zoom """
        save_view = self.viewer.camera.copy()
        save_frame = ut.current_frame(self.viewer)
        ## place the view to see the whole image
        self.viewer.reset_view()
        #self.viewer.camera.zoom = 1
        sizex = (self.imgshape2D[0]*self.viewer.camera.zoom)/2
        sizey = (self.imgshape2D[1]*self.viewer.camera.zoom)/2
        if os.path.exists(outname):
            os.remove(outname)

        ## take a screenshot of each frame
        for frame in range(self.nframes):
            self.viewer.dims.set_point(0, frame)
            shot = self.viewer.window.screenshot(canvas_only=True, flash=False)
            ## remove border: movie is at the center
            centx = int(shot.shape[0]/2)+1
            centy = int(shot.shape[1]/2)+1
            shot = shot[int(centx-sizex):int(centx+sizex), int(centy-sizey):int(centy+sizey),]
            ut.appendToTif(shot, outname)
        self.viewer.camera.update(save_view)
        if save_frame is not None:
            self.viewer.dims.set_point(0, save_frame)
        ut.show_info("Movie "+outname+" saved")

    def reset_data( self ):
        """ Reset EpiCure data (group, suspect, graph) """
        self.suspecting.reset_all_suspects()
        self.reset_groups()
        self.outputing.update_selection_list()
        self.tracking.graph = None

    def junctions_to_label(self):
        """ convert epyseg/skeleton result (junctions) to labels map """
        cmax = 0
        for z in range(self.seg.shape[0]):
            self.label_one_frame(z)
            ## shift all the labels with the previous max
            if z > 0:
                nonzero = self.seg[z] > 0
                self.seg[z,nonzero] = self.seg[z,nonzero] + cmax
            cmax = np.max(self.seg[z])

    def shift_labels(self):
        """ Shift the labels of each frame so they never overlap """
        cmax = 0
        for z in range(self.seg.shape[0]):
            if z > 0:
                nonzero = self.seg[z] > 0
                self.seg[z,nonzero] = self.seg[z,nonzero] + cmax
            cmax = np.max(self.seg[z])

    def label_one_frame(self, z):
        """ From segmentation of junctions of one frame, get it as a label frame """
        skel = skeletonize( self.seg[z]/np.max(self.seg[z] ))
        skel = self.copy_border( skel, self.seg[z] )
        self.seg[z] = label( skel, background=1, connectivity=1)
        return

    def copy_border( self, skel, bin ):
        """ Copy the pixel border onto skeleton image """
        skel[0,:] = bin[0,:] ## borders
        skel[:,0] = bin[:,0]
        skel[skel.shape[0]-1,:] = bin[skel.shape[0]-1,:]
        skel[:,skel.shape[1]-1] = bin[:,skel.shape[1]-1]
        return skel
        
    def thin_boundaries(self):
        """" Assure that all boundaries are only 1 pixel thick """
        if self.process_parallel:
            pool = Pool(self.nparallel)
            pool.map( self.thin_seg_one_frame, range(self.seg.shape[0]) )
            pool.close()
        else:
            for z in range(self.seg.shape[0]):
                self.thin_seg_one_frame(z)

    def skeleton_to_label( self, skel, labelled ):
        """ Transform a skeleton to label image with numbers from labelled image """
        newlab = label( skel, background=np.max(skel), connectivity=1 )
        props = regionprops( newlab )  
        newlab = np.zeros( newlab.shape, np.uint32 )   
        for prop in props:
            if prop.label != 0:
                labvals, counts = np.unique(labelled[prop.bbox[0]:prop.bbox[2],prop.bbox[1]:prop.bbox[3]][prop.image], return_counts=True )
                labval = labvals[ np.argmax(counts) ]
                newlab[prop.bbox[0]:prop.bbox[2],prop.bbox[1]:prop.bbox[3]][prop.image] = labval
        return newlab

    def thin_seg_one_frame(self, tframe):
        """ Boundaries of the frame one pixel thick """
        bin_img = binary_closing( find_boundaries(self.seg[tframe], connectivity=2, mode="outer"), footprint=np.ones((3,3)) )
        skel = skeletonize( bin_img )
        skel = self.copy_border( skel, bin_img )
        self.seg[tframe] = self.skeleton_to_label( skel, self.seg[tframe] )

    def frame_to_skeleton(self, frame, connectivity=1):
        """ convert labels frame to skeleton (thin boundaries) """
        return skeletonize( find_boundaries(frame, connectivity=connectivity, mode="outer") )

    def add_skeleton(self):
        """ add a layer containing the skeleton movie of the segmentation """
        # display the segmentation file movie
        if self.viewer is not None:
            skel = np.zeros(self.seg.shape, dtype="uint8")
            skel[self.seg==0] = 1
            skel = self.get_skeleton()
            ut.remove_layer(self.viewer, "Skeleton")
            skellayer = self.viewer.add_image( skel, name="Skeleton", blending="additive", opacity=1 )
            skellayer.reset_contrast_limits()
            skellayer.contrast_limits = (0,1)
    
    def get_skeleton(self):
        """ convert labels movie to skeleton (thin boundaries) """
        if self.seg is None:
            return None
        return ut.get_skeleton( self.seg, verbose = self.verbose )

    def to_skeleton(self, mode):
        """ convert labels movie to skeleton (thin boundaries) """
        if self.seg is not None:
            start_time = ut.start_time()
            skel = np.zeros(self.seg.shape, dtype="uint8")
            for z in range(self.seg.shape[0]):
                skel[z,] = apply_parallel( self.frame_to_skeleton, self.seg[z,], depth=5, compute=True )
        if self.verbose > 0:
            ut.show_duration(start_time)
        return skel


    ############ Label functions

    def get_free_labels(self, nlab):
        """ Get the nlab smallest unused labels """
        used = set(self.tracking.get_track_list())
        return ut.get_free_labels( used, nlab )

    def get_free_label(self):
        """ Return the first free label """
        return self.get_free_labels(1)[0]

    def has_label(self, label):
        """ Check if label is present in the tracks """
        return self.tracking.has_track(label)

    def nlabels(self):
        """ Number of unique tracks """
        return self.tracking.nb_tracks()

    def get_labels(self):
        """ Return list of labels in tracks """
        return list(self.tracking.get_track_list())

    ########## Edit tracks
    def delete_tracks(self, tracks):
        """ Remove all the tracks from the Track layer """
        self.tracking.remove_tracks( tracks )

    def delete_track(self, label, frame=None):
        """ Remove the track """
        if frame is None:
            self.tracking.remove_track(label)
        else:
            self.tracking.remove_one_frame(label, frame)

    def update_centroid(self, label, frame):
        """ Track label has been change at given frame """
        if label not in self.tracking.has_track(label):
            if self.verbose > 1:
                print("Track "+str(label)+" not found")
            return
        self.tracking.update_centroid(label, frame)

    ########## Edit label
    def get_label_indexes (self, label, start_frame=0 ):
        """ Returns the indexes where label is present in segmentation, starting from start_frame """
        indmodif = []
        while start_frame < self.nframes:
            found_label = np.argwhere( self.seg[start_frame] == label )
            if found_label is None:
                break   ### if lose a label, stop there (don't allow gap frame)
            inds = ut.shiftFrameIndices( found_label.tolist(), start_frame )
            indmodif = indmodif + inds
            start_frame = start_frame + 1
        return indmodif

    def replace_label( self, label, new_label, start_frame=0 ):
        """ Replace label with new_label from start_frame """
        indmodif = self.get_label_indexes( label, start_frame )
        new_labels = [new_label]*len(indmodif)
        self.change_labels( indmodif, new_labels )
    
    def change_labels(self, indmodif, new_labels):
        """ Change the value at pixels indmodif to new_labels and update tracks/graph """
        if len(indmodif)>0:
            bbox = ut.getBBoxFromPts( indmodif, extend=0, imshape=self.imgshape, outdim=3 )
            ## get effectively changed labels
            indmodif, new_labels, old_labels = ut.setNewLabel( self.seglayer, indmodif, new_labels, add_frame=None )
            if len(new_labels) > 0:
                self.update_changed_labels( indmodif, new_labels, old_labels )
        self.seglayer.refresh()

    def get_mask( self, label, start=None, end=None ):
        """ Get mask of label from frame start to frame end """
        if (start is None) or (end is None):
            start, end = self.tracking.get_extreme_frames( label )
        crop = self.seg[start:(end+1)]
        mask = np.isin( crop, [label] )*1
        return mask

    def get_label_movie( self, label, extend=1.25 ):
        """ Get movie centered on label """
        start, end = self.tracking.get_extreme_frames( label )
        mask = self.get_mask( label, start, end )
        boxes = []
        centers = []
        max_box = 0
        for frame in mask:
            props = regionprops( frame )
            bbox = props[0].bbox
            boxes.append(bbox)
            centers.append(props[0].centroid)
            for i in range(2):
                max_box = max( max_box, bbox[i+2]-bbox[i] )
        
        box_size = int(max_box*extend)
        movie = np.zeros((end-start+1, box_size, box_size))
        for i, frame in enumerate(range(start, end+1)):
            xmin = int(centers[i][0] - box_size/2)
            xminshift=0
            if xmin < 0:
                xminshift = -xmin
                xmin = 0
            xmax = xmin + box_size - xminshift
            xmaxshift = box_size
            if xmax > self.imgshape2D[0]:
                xmaxshift = self.imgshape2D[0] - xmax
                xmax = self.imgshape2D[0]

            ymin = int(centers[i][1] - max_box/2)
            yminshift=0
            if ymin < 0:
                yminshift = -ymin
                ymin = 0
            ymax = ymin + box_size - yminshift
            ymaxshift = box_size
            if ymax > self.imgshape2D[1]:
                ymaxshift = self.imgshape2D[1] - ymax
                ymax = self.imgshape2D[1]

            movie[ i, xminshift:xmaxshift, yminshift:ymaxshift ] = self.img[ frame, xmin:xmax, ymin:ymax ]
        return movie 



    ###### Synchronize tracks whith labels changed
    def add_label( self, labels, frame=None ):
        """ Add a label to the tracks """
        if frame is not None:
            if np.isscalar(labels):
                labels = [labels]
            self.tracking.add_one_frame( labels, frame, refresh=True )
        else:
            if self.verbose > 1:
                print("TODO add label no frame")
    
    def add_one_label_to_track( self, label ):
        """ Add the track data of a given label if missing """
        iframe = 0
        while (iframe < self.nframes) and (label not in self.seg[iframe]):
            iframe = iframe + 1
        while (iframe < self.nframes) and (label in self.seg[iframe]):
            self.tracking.add_one_frame( [label], iframe )
            iframe = iframe + 1

    def update_label(self, label, frame):
        """ Update the given label at given frame """
        self.tracking.update_track_on_frame([label], frame)

    def update_changed_labels( self, indmodif, new_labels, old_labels ):
        """ Check what had been modified, and update tracks from it """
        ## check all the old_labels if still present or not
        min_frame = np.min(indmodif[0])
        max_frame = np.max(indmodif[0])
        start_time = time.time()
        all_deleted = []
        for frame in range(min_frame, max_frame+1):
            if self.verbose > 1:
                print("Updating labels at frame "+str(frame))
            keep = np.where(indmodif[0] == frame)[0]
            nlabels = np.unique(new_labels[keep])
            olabels = np.unique(old_labels[keep])
            ## check old labels if totally removed or not
            deleted = np.setdiff1d( olabels, self.seg[frame] )
            if deleted.shape[0] > 0:
                self.tracking.remove_one_frame( deleted, frame, handle_gaps=False, refresh=False )
                all_deleted = all_deleted + list(set(deleted) - set(all_deleted))
            if nlabels.shape[0] > 0:
                self.tracking.update_track_on_frame( nlabels, frame )
            if self.verbose > 1:
                print("Labels deleted "+str(deleted)+" or added "+str(nlabels))

        ## Check if some gaps has been created in tracks (remove middle(s) frame(s))
        if len(all_deleted) > 0:
            self.handle_gaps( all_deleted, verbose=0 )

        if self.verbose > 1:
            ut.show_duration(start_time, "updated tracks in ")

    def handle_gaps(self, track_list, verbose=None):
        """ Check and fix gaps in tracks """
        if verbose is None:
            verbose = self.verbose
        gaped = self.tracking.check_gap( track_list, verbose=verbose )
        if len(gaped) > 0:
            if self.verbose > 0:
                print("Relabelling tracks with gaps")
            self.fix_gaps(gaped)
            
    def fix_gaps(self, gaps):
        """ Fix when some gaps has been created in tracks """
        for gap in gaps:
            gap_frames = self.tracking.gap_frames( gap )
            cur_gap = gap
            for gapy in gap_frames:
                new_value = self.get_free_label()
                self.replace_label( cur_gap, new_value, gapy )
                cur_gap = new_value

    def swap_labels( self, lab, olab, frame ):
        """ Exchange two labels """
        self.tracking.swap_frame_id(lab, olab, frame)

    def swap_tracks( self, lab, olab, start_frame ):
        """ Exchange two tracks """
        ## split the two labels to unused value
        tmp_labels = self.get_free_labels( 2 )
        for i, laby in enumerate([lab, olab]):
            self.replace_label( laby, tmp_labels[i], start_frame )
            
        ## replace the two initial labels, in inversed order
        self.replace_label( tmp_labels[0], olab, start_frame )
        self.replace_label( tmp_labels[1], lab, start_frame )
        

    def update_changed_labels_img( self, img_before, img_after, added=True, removed=True ):
        """ Update tracks from changes between the two labelled images """
        if self.verbose > 1:
            print("Updating changed labels from images")
        indmodif = np.argwhere( img_before != img_after ).tolist()
        if len(indmodif) <= 0:
            return
        indmodif = tuple( np.array(indmodif).T )
        new_labels = img_after[indmodif]
        old_labels = img_before[indmodif]
        self.update_changed_labels( indmodif, new_labels, old_labels )

    
    def added_labels_oneframe( self, frame, img_before, img_after ):
        """ Update added tracks between the two labelled images at frame """
        ## Look for added labels
        added_labels = np.setdiff1d( img_after, img_before )
        self.tracking.add_one_frame( added_labels, frame, refresh=True )
    
    def removed_labels( self, img_before, img_after, frame=None ):
        """ Update removed tracks between the two labelled images """
        ## Look for added labels
        deleted_labels = np.setdiff1d( img_before, img_after )
        if frame is None:
            self.tracking.remove_tracks( deleted_labels )
        else:
            self.tracking.remove_one_frame( track_id=deleted_labels.tolist(), frame=frame, handle_gaps=True)

    def remove_label(self, label, force=False):
        """ Remove a given label if allowed """
        ut.changeLabel(self.seglayer, label, 0)
        self.tracking.remove_tracks(label)
        self.seglayer.refresh()

    def remove_labels(self, labels, force=False):
        """ Remove all allowed labels """
        inds = []
        for lab in labels:
            #if (force) or (not self.locked_label(label)):
            inds = inds + ut.getLabelIndexes(self.seglayer.data, lab, None)
        ut.setNewLabel(self.seglayer, inds, 0)
        self.tracking.remove_tracks(labels)
    
    def keep_labels(self, labels, force=True):
        """ Remove all other labels that are not in labels """
        inds = []
        toremove = list( set(self.tracking.get_track_list()) - set(labels) )
        #for lab in self.tracking.get_track_list():
        #    if lab not in labels:
                #if (force) or (not self.locked_label(label)):
        for lab in toremove:
            inds = inds + ut.getLabelIndexes(self.seglayer.data, lab, None)
        #        toremove.append(lab)
        ut.setNewLabel(self.seglayer, inds, 0)
        self.tracking.remove_tracks(toremove)

    def get_frame_features( self, frame, props ):
        """ Measure the label properties of given frame """
        return regionprops_table( self.seg[frame], properties=props )

    #######################
    ## Classified cells options
    def get_all_groups(self, numeric=False):
        """ Add all groups info """
        if numeric:
            groups = [0]*self.nlabels()
        else:
            groups = ["None"]*self.nlabels()
        for igroup, gr in self.groups.keys():
            indexes = self.tracking.get_track_indexes(self.groups[gr])
            if numeric:
                groups[indexes] = igroup + 1
            else:
                groups[indexes] = gr
        return groups 
    
    def get_groups(self, labels, numeric=False):
        """ Add the group info of the given labels (repeated) """
        if numeric:
            groups = [0]*len(labels)
        else:
            groups = ["None"]*len(labels)
        for lab in np.unique(labels):
            gr = self.find_group( lab )
            if numeric:
                gr = self.groups.keys().index() + 1
            indexes = (np.argwhere(labels==lab)).flatten()
            for ind in indexes:
                groups[ind] = gr
        return groups 
    
    def cell_ingroup(self, label, group):
        """ Put the cell "label" in group group, add it if new group """
        if not self.has_label(label):
            if self.verbose > 1:
                print("Cell "+str(label)+" missing")
            return
        if group not in self.groups.keys():
            self.groups[group] = []
            if self.outputing is not None:
                self.outputing.update_selection_list()
        if label not in self.groups[group]:
            self.groups[group].append(label)

    def find_group(self, label):
        """ Find in which group the label is """
        for gr, labs in self.groups.items():
            if label in labs:
                return gr
        return None


    def cell_removegroup(self, label):
        """ Detach the cell from its group """
        if not self.has_label(label):
            if self.verbose > 1:
                print("Cell "+str(label)+" missing")
        group = self.find_group(label)
        if group is not None:
            self.groups[group].remove(label)
            if len(self.groups[group]) <= 0:
                del self.groups[group]
                self.outputing.update_selection_list()

    def reset_groups(self):
        """ Remove all group information for all cells """
        self.groups = {} 
        self.outputing.update_selection_list()

    def draw_groups(self):
        """ Draw all the epicells colored by their group """
        grouped = np.zeros(self.seg.shape, np.uint8)
        if (self.groups is None) or len(self.groups.keys()) == 0:
            return grouped
        for group, labels in self.groups.items():
            igroup = self.get_group_index(group) + 1
            np.place(grouped, np.isin(self.seg, labels), igroup)
        return grouped

    def get_group_index(self, group):
        """ Get the index of group in the list of groups """
        igroup = (list(self.groups.keys())).index(group)
        return igroup
    

    ######### ROI

    def only_current_roi(self, frame):
        """ Put 0 everywhere outside the current ROI """
        roi_labels = self.editing.get_labels_inside()
        if roi_labels is None:
            return None
        # remove all other labels that are not in roi_labels
        roilab = np.copy(self.seg[frame])
        inds = []
        np.place(roilab, np.isin(roilab, roi_labels, invert=True), 0) 
        return roilab






