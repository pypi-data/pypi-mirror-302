from qtpy.QtWidgets import QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QLineEdit, QComboBox, QLabel, QSpinBox, QCheckBox, QTableWidget, QTableWidgetItem, QGridLayout
from qtpy.QtCore import Qt
from napari import Viewer
import pandas as pand
import numpy as np
import epicure.Utils as ut
import roifile
from napari.utils.notifications import show_info
from skimage.measure import find_contours, regionprops_table
from skimage.morphology import binary_erosion, binary_dilation, disk
from skimage.segmentation import expand_labels
import os, time
import napari
from napari.utils import progress
from magicgui import magicgui

import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

try:
    from skimage.graph import RAG
except:
    from skimage.future.graph import RAG  ## older version of scikit-image

class Outputing(QWidget):

    def __init__(self, napari_viewer, epic):
        super().__init__()
        self.viewer = napari_viewer
        self.epicure = epic
        self.table = None
        self.table_selection = None
        self.seglayer = self.viewer.layers["Segmentation"]
        self.movlayer = self.viewer.layers["Movie"]
        self.selection_choices = ["All cells", "Only selected cell"]
        self.output_options = ["Export to extern plugins", "Export segmentations", "Measure cell features", "Measure track features"]
        self.tplots = None
        
        all_layout = QVBoxLayout()
        
        self.choose_output = QComboBox()
        all_layout.addWidget(self.choose_output)
        for option in self.output_options:
            self.choose_output.addItem(option)
        self.choose_output.currentIndexChanged.connect(self.show_output_option)
        
        ## Choice of active selection
        layout = QVBoxLayout()
        selection_layout = QHBoxLayout()
        selection_lab = QLabel()
        selection_lab.setText("Apply on")
        selection_layout.addWidget(selection_lab)
        self.output_mode = QComboBox()
        selection_layout.addWidget(self.output_mode)
        for sel in self.selection_choices:
            self.output_mode.addItem(sel)
        all_layout.addLayout(selection_layout)
       
        ## Choice of interface
        self.export_group = QGroupBox("Export to extern plugins")
        export_layout = QVBoxLayout()
        griot_btn = QPushButton("Current frame to Griottes", parent=self)
        export_layout.addWidget(griot_btn)
        griot_btn.clicked.connect(self.to_griot)
        ncp_btn = QPushButton("Current frame to Cluster-Plotter", parent=self)
        export_layout.addWidget(ncp_btn)
        ncp_btn.clicked.connect(self.to_ncp)
        self.export_group.setLayout(export_layout)
        self.export_group.setCheckable(True)
        self.export_group.clicked.connect(self.show_export_group)
        all_layout.addWidget(self.export_group)
        
        ## Option to export segmentation results
        self.export_seg_group = QGroupBox(self.output_options[1])
        self.save_rois = QPushButton("Save ROI(s)", parent=self)
        layout.addWidget(self.save_rois)
        self.save_rois.clicked.connect(self.roi_out)
        
        self.save_seg = QPushButton("Save segmentation(s)", parent=self)
        layout.addWidget(self.save_seg)
        self.save_seg.clicked.connect(self.save_segmentation)
        
        self.save_skel = QPushButton("Save Skeleton(s)", parent=self)
        layout.addWidget(self.save_skel)
        self.save_skel.clicked.connect(self.save_skeleton)

        self.export_seg_group.setCheckable(True)
        self.export_seg_group.clicked.connect(self.show_export_seg_group)
        self.export_seg_group.setLayout(layout)
        self.export_seg_group.hide()
        all_layout.addWidget(self.export_seg_group)
        
        #### Features group
        self.feature_group = QGroupBox(self.output_options[2])
        self.feature_group.setCheckable(True)
        featlayout = QVBoxLayout()
        self.feature_shape_cbox = QCheckBox(text="Shape features")
        self.feature_intensity_cbox = QCheckBox(text="Intensity features")
        self.measure_other_chanels_cbox = QCheckBox(text="Intensity in other chanels")
        self.feature_graph_cbox = QCheckBox(text="Neighboring features")
        featlayout.addWidget(self.feature_shape_cbox)
        featlayout.addWidget(self.feature_intensity_cbox)
        featlayout.addWidget(self.measure_other_chanels_cbox)
        featlayout.addWidget(self.feature_graph_cbox)
        self.feature_table = QPushButton("Create features table", parent=self)
        featlayout.addWidget(self.feature_table)
        self.feature_table.clicked.connect(self.show_table)
        self.featTable = FeaturesTable(self.viewer, self.epicure)
        featlayout.addWidget(self.featTable)
        
        self.temp_graph = QPushButton("Table to temporal graphs", parent=self)
        featlayout.addWidget(self.temp_graph)
        self.temp_graph.clicked.connect(self.temporal_graphs)
        self.temp_graph.setEnabled(False)
        
        featmap = QHBoxLayout()
        featmap_lab = QLabel()
        featmap_lab.setText("Draw feature map:")
        featmap.addWidget(featmap_lab)
        self.show_feature_map = QComboBox()
        featmap.addWidget(self.show_feature_map)
        self.show_feature_map.currentIndexChanged.connect(self.show_feature)
        featlayout.addLayout(featmap)
        
        self.save_table = QPushButton("Save features table", parent=self)
        featlayout.addWidget(self.save_table)
        self.save_table.clicked.connect(self.save_measure_features)
        if (self.epicure.others is None):
            self.measure_other_chanels_cbox.hide()
        
        self.feature_group.setLayout(featlayout)
        self.feature_group.clicked.connect(self.show_feature_group)
        self.feature_group.hide()
        all_layout.addWidget(self.feature_group)

        ## Track features
        self.trackfeat_group = QGroupBox(self.output_options[3])
        self.trackfeat_group.setCheckable(True)
        trackfeatlayout = QVBoxLayout()
        self.trackfeat_table = QPushButton("Track features table", parent=self)
        trackfeatlayout.addWidget(self.trackfeat_table)
        self.trackfeat_table.clicked.connect(self.show_trackfeature_table)
        self.trackTable = FeaturesTable(self.viewer, self.epicure)
        trackfeatlayout.addWidget(self.trackTable)
        
        self.trackfeat_group.setLayout(trackfeatlayout)
        self.trackfeat_group.clicked.connect(self.show_trackfeature_group)
        self.trackfeat_group.hide()
        all_layout.addWidget(self.trackfeat_group)
        
        ## Finished
        self.setLayout(all_layout)
        self.setStyleSheet('QGroupBox {color: grey; background-color: rgb(35,45,50)} ')

    def show_output_option(self):
        """ Show selected output panel """
        cur_option = self.choose_output.currentText()
        if cur_option == "Export to extern plugins":
            self.export_group.setChecked(True)
            self.export_group.show()
        if cur_option == "Export segmentations":
            self.export_seg_group.setChecked(True)
            self.export_seg_group.show()
        if cur_option == "Measure cell features":
            self.feature_group.setChecked(True)
            self.feature_group.show()
        if cur_option == "Measure track features":
            self.trackfeat_group.setChecked(True)
            self.trackfeat_group.show()
    
    def show_export_group(self):
        """ Show/Hide export group """
        if not self.export_group.isChecked():
            self.export_group.setChecked(True)
            self.export_group.hide()
    
    def show_export_seg_group(self):
        """ Show/Hide export segmentaion group """
        if not self.export_seg_group.isChecked():
            self.export_seg_group.setChecked(True)
            self.export_seg_group.hide()
    
    def show_feature_group(self):
        """ Show/Hide feature cell group """
        if not self.feature_group.isChecked():
            self.feature_group.setChecked(True)
            self.feature_group.hide()
    
    def show_trackfeature_group(self):
        """ Show/Hide feature cell group """
        if not self.trackfeat_group.isChecked():
            self.trackfeat_group.setChecked(True)
            self.trackfeat_group.hide()


    def get_selection_name(self):
        if self.output_mode.currentText() == "Only selected cell": 
            lab = self.epicure.seglayer.selected_label
            return "_cell_"+str(lab) 
        #if self.output_mode.currentText() == "Only checked cells":
        #    return "_checked_cells"
        if self.output_mode.currentText() == "All cells":
            return ""
        return "_"+self.output_mode.currentText()

    def save_measure_features(self):
        """ Save measures table to file whether it was created or not """
        if self.table is None or self.table_selection is None or self.selection_changed() :
            show_info("Create/update the table before")
            return
        outfile = self.epicure.outname()+"_features"+self.get_selection_name()+".xlsx"
        self.table.to_excel(outfile, sheet_name='EpiCureMeasures')
        show_info("Measures saved in "+outfile)

    def roi_out(self):
        """ Save ROI of cell contours in zip file by cell """
        if self.output_mode.currentText() == "Only selected cell": 
            lab = self.seglayer.selected_label
            self.save_one_roi(lab)
            show_info("Cell "+str(lab)+" saved to Fiji ROI")
            return
        else:
            if self.output_mode.currentText() == "All cells":
                ncells = 0
                for lab in np.unique(self.epicure.seglayer.data):
                    self.save_one_roi(lab)
                    ncells += 1
                show_info(str(ncells)+" cells saved to Fiji ROIs")
            else:
                ncells = 0
                group = self.output_mode.currentText()
                label_group = self.epicure.groups[group]
                for lab in label_group:
                    self.save_one_roi(lab)
                    ncells += 1
                show_info(str(ncells)+" cells saved to Fiji ROIs")

    def save_one_roi(self, lab):
        """ Save the Rois of cell with label lab """
        keep = self.seglayer.data == lab
        rois = []
        if np.sum(keep) > 0:
            ## add 2D case
            for iframe, frame in enumerate(keep):
                if np.sum(frame) > 0:
                    contour = find_contours(frame)
                    roi = self.create_roi(contour[0], iframe, lab)
                    rois.append(roi)

        roifile.roiwrite(self.epicure.outname()+"_rois_cell_"+str(lab)+".zip", rois, mode='w')

    def create_roi(self, contour, frame, label):
        croi = roifile.ImagejRoi()
        croi.version = 227
        croi.roitype = roifile.ROI_TYPE(0) ## polygon
        croi.n_coordinates = len(contour)
        croi.position = frame + 1
        croi.t_position = frame+1
        coords = []
        cent0 = 0
        cent1 = 0
        for cont in contour:
            coords.append([int(cont[1]), int(cont[0])])
            cent0 += cont[1]
            cent1 += cont[0]
        croi.integer_coordinates = np.array(coords)
        #croi.top = int(np.min(coords[0]))
        #croi.left = int(np.min(coords[1]))
        croi.name = str(frame+1).zfill(4)+'-'+str(int(cent0/len(contour))).zfill(4)+"-"+str(int(cent1/len(contour))).zfill(4)
        return croi
    
    def save_segmentation( self ):
        """ Save label movies of current output selection """
        if self.output_mode.currentText() == "Only selected cell": 
            lab = self.seglayer.selected_label
            tosave = np.zeros(self.seglayer.data.shape, dtype=self.epicure.dtype)
            if np.sum(self.seglayer.data==lab) > 0:
                tosave[self.seglayer.data==lab] = lab
            endname = "_cell_"+str(lab)+".tif"
        else: 
            endname = "_checked_cells.tif"
            if self.output_mode.currentText() == "All cells": 
                tosave = self.seglayer.data
                endname = "_labels.tif"
            else:
                tosave = np.zeros(self.seglayer.data.shape, dtype=self.epicure.dtype)
                endname = "_"+self.output_mode.currentText()+".tif"
                ncells = 0
                group = self.output_mode.currentText()
                label_group = self.epicure.groups[group]
                for lab in label_group:
                    tosave[self.seglayer.data==lab] = lab

        outname = os.path.join( self.epicure.outdir, self.epicure.imgname+endname )
        ut.writeTif(tosave, outname, self.epicure.scale, 'float32', what="Segmentation")

    def save_skeleton( self ):
        """ Save skeleton movies of current output selection """
        if self.output_mode.currentText() == "Only selected cell": 
            lab = self.seglayer.selected_label
            tosave = np.zeros(self.seglayer.data.shape, dtype=self.epicure.dtype)
            if np.sum(self.seglayer.data==lab) > 0:
                tosave[self.seglayer.data==lab] = lab
            endname = "_skeleton_cell_"+str(lab)+".tif"
        else: 
            endname = "_checked_cells.tif"
            if self.output_mode.currentText() == "All cells": 
                tosave = self.seglayer.data
                endname = "_skeleton.tif"
            else:
                tosave = np.zeros(self.seglayer.data.shape, dtype=self.epicure.dtype)
                endname = "_skeleton_"+self.output_mode.currentText()+".tif"
                ncells = 0
                group = self.output_mode.currentText()
                label_group = self.epicure.groups[group]
                for lab in label_group:
                    tosave[self.seglayer.data==lab] = lab

        tosave = ut.get_skeleton( tosave, verbose=self.epicure.verbose )
        outname = os.path.join( self.epicure.outdir, self.epicure.imgname+endname )
        ut.writeTif( tosave, outname, self.epicure.scale, 'uint8', what="Skeleton" )

    def measure_features(self):
        """ Measure features and put them to table """
        def intensities_inside_outside(regionmask, intensity):
            """ Measure the intensity only on the contour of regionmask """
            footprint = disk(radius=self.epicure.thickness)
            inside = binary_erosion(regionmask, footprint)
            inside_intensity = ut.mean_nonzero(intensity*inside)
            dil_regionmask = binary_dilation(regionmask, footprint)
            periph = dil_regionmask^inside
            periph_intensity = ut.mean_nonzero(intensity*(regionmask^inside))
            return inside_intensity, periph_intensity
        
        if self.epicure.verbose > 0:
            print("Measuring features")
        self.viewer.window._status_bar._toggle_activity_dock(True)
        start_time = time.time()
        if self.output_mode.currentText() == "Only selected cell": 
            meas = np.zeros(self.epicure.seglayer.data.shape, self.epicure.dtype)
            lab = self.epicure.seglayer.selected_label
            meas[self.epicure.seglayer.data==lab] = lab
        else:
            if self.output_mode.currentText() == "All cells": 
                meas = self.epicure.seglayer.data
            else:
                group = self.output_mode.currentText()
                meas = np.zeros(self.epicure.seglayer.data.shape, self.epicure.dtype)
                label_group = self.epicure.groups[group]
                for lab in label_group:
                    meas[self.epicure.seglayer.data==lab] = lab
            
        properties = ["label", "area", "centroid"]
        extra_properties = []
        if self.feature_shape_cbox.isChecked():
            properties = properties + ["area_convex", "axis_major_length", "axis_minor_length", "feret_diameter_max", "equivalent_diameter_area", "eccentricity", "orientation", "perimeter", "solidity"]
        if self.feature_intensity_cbox.isChecked():
            properties = properties + ["intensity_mean", "intensity_min", "intensity_max"]
            extra_properties = extra_properties + [intensities_inside_outside]
        self.table = None
        for iframe, frame in progress(enumerate(meas)):
            frame_table = self.measure_one_frame( frame, properties, extra_properties, iframe )
            if self.table is None:
                self.table = pand.DataFrame(frame_table)
            else:
                self.table = pand.concat([self.table, pand.DataFrame(frame_table)])

        if "intensities_inside_outside-0" in self.table.keys():
            self.table = self.table.rename(columns={"intensities_inside_outside-0": "intensity_cytoplasm", "intensities_inside_outside-1":"intensity_junction"})
        self.table_selection = self.selection_choices.index(self.output_mode.currentText())
        self.viewer.window._status_bar._toggle_activity_dock(False)
        show_info("Features measured in "+"{:.3f}".format((time.time()-start_time)/60)+" min")
        
    def measure_one_frame(self, img, properties, extra_properties, frame):
        """ Measure on one frame """
        if frame is not None:
            intimg = self.movlayer.data[frame]
        else:
            intimg = self.movlayer.data
        frame_table = regionprops_table(img, intensity_image=intimg, properties=properties, extra_properties=extra_properties)
        ndata = len(frame_table["label"])
        if frame is not None:
            frame_table["frame"] = np.repeat(frame, ndata)
        ## add info of the cell group
        frame_group = self.epicure.get_groups(list(frame_table["label"]), numeric=False)
        frame_table["group"] = frame_group

        ### Measure intensity features in other chanels if option is on
        if self.measure_other_chanels_cbox.isChecked():
            prop = ["intensity_mean", "intensity_min", "intensity_max"]
            extra_prop = extra_properties
            for ochan, oimg in zip(self.epicure.others_chanlist, self.epicure.others):
                if frame is not None:
                    intimg = oimg[frame]
                else:
                    intimg = oimg
                frame_tab = regionprops_table(img, intensity_image=intimg, properties=prop, extra_properties=extra_prop)
                for add_prop in prop:
                    frame_table[add_prop+"_Chanel"+str(ochan)] = frame_tab[add_prop]
                if "intensities_inside_outside-0" in frame_tab.keys():
                    frame_table["intensity_cytoplasm_Chanel"+str(ochan)] = frame_tab["intensities_inside_outside-0"]
                    frame_table["intensity_junction_Chanel"+str(ochan)] = frame_tab["intensities_inside_outside-1"]

        
        ## add features of neighbors relationship with graph
        if self.feature_graph_cbox.isChecked():
            touchlab = expand_labels(img, distance=3)  ## be sure that labels touch
            graph = RAG( touchlab, connectivity=2)
            adj_bg = []
            if 0 in graph.nodes:
                adj_bg = list(graph.adj[0])
                graph.remove_node(0)
            
            frame_table["NbNeighbors"] = np.repeat(-1, ndata)
            frame_table["External"] = np.repeat(-1, ndata)
            nodes = list(graph.nodes)
            for label in nodes:
                nneighbor = len(graph.adj[label])
                outer = int( label in adj_bg )
                rlabel = (frame_table["label"] == label)
                frame_table["NbNeighbors"][rlabel] = nneighbor
                frame_table["External"][rlabel] = outer

        return frame_table

    def selection_changed(self):
        if self.table_selection is None:
            return True
        return self.output_mode.currentText() != self.selection_choices[self.table_selection]

    def update_selection_list(self):
        """ Update the possible selection from group cell list """
        self.selection_choices = ["Only selected cell", "All cells"]
        for group in self.epicure.groups.keys():
            self.selection_choices.append(group)
        self.output_mode.clear()
        for sel in self.selection_choices:
            self.output_mode.addItem(sel)

    def show_table(self):
        """ Show the measurement table """
        #disable automatic update (slow)
        #if self.table is None:
            ## create the table and connect action to update it automatically
            #self.output_mode.currentIndexChanged.connect(self.show_table)
            #self.measure_other_chanels_cbox.stateChanged.connect(self.show_table)
            #self.feature_graph_cbox.stateChanged.connect(self.show_table)
            #self.feature_intensity_cbox.stateChanged.connect(self.show_table)
            #self.feature_shape_cbox.stateChanged.connect(self.show_table)
        
        ut.set_active_layer( self.viewer, "Segmentation" )
        self.show_feature_map.clear()
        self.show_feature_map.addItem("")
        laynames = [lay.name for lay in self.viewer.layers]
        for lay in laynames:
            if lay.startswith("Map_"):
                ut.remove_layer(self.viewer, lay)
        self.measure_features()
        self.featTable.set_table(self.table)
        featlist = self.table.keys()
        for feat in featlist:
            self.show_feature_map.addItem(feat)
        self.temp_graph.setEnabled(True)
        if self.tplots is not None:
            self.tplots.update_table(self.table)

    def show_feature(self):
        """ Add the image map of the selected feature """
        feat = self.show_feature_map.currentText()
        if (feat is not None) and (feat != ""):
            if feat in self.table.keys():
                values = list(self.table[feat])
                if feat == "group":
                    for i, val in enumerate(values):
                        if (val is None) or (val == 'None'):
                            values[i] = 0
                        else:
                            values[i] = list(self.epicure.groups.keys()).index(val) + 1
                labels = list(self.table["label"])
                frames = None
                if "frame" in self.table:
                    frames = list(self.table["frame"])
                self.draw_map(labels, values, frames, feat)

    def draw_map(self, labels, values, frames, featname):
        """ Add image layer of values by label """
        self.viewer.window._status_bar._toggle_activity_dock(True)
        mapfeat = np.empty(self.epicure.seg.shape, dtype="float16")
        mapfeat[:] = np.nan
        for ind, lab in progress(enumerate(labels)):
            if frames is not None:
                frame = frames[ind]
                cell = self.seglayer.data[frame]==lab
                (mapfeat[frame])[cell] = values[ind]
            else:
                cell = self.seglayer.data==lab
                mapfeat[cell] = values[ind]
        ut.remove_layer(self.viewer, "Map_"+featname)
        self.viewer.add_image(mapfeat, name="Map_"+featname)
        self.viewer.window._status_bar._toggle_activity_dock(False)

    def to_griot(self):
        """ Export current frame to new viewer and makes it ready for Griotte plugin """
        try:
            from napari_griottes import make_graph
        except:
            ut.show_error("Plugin napari-griottes is not installed")
            return
        gview = napari.Viewer()
        tframe = ut.current_frame(self.viewer)
        segt = self.epicure.seglayer.data[tframe]
        touching_frame = self.touching_labels(segt)
        gview.add_labels(touching_frame, name="TouchingCells", opacity=1)
        gview.window.add_dock_widget(make_graph(), name="Griottes")

    def touching_labels(self, labs):
        """ Dilate labels so that they all touch """
        from skimage.segmentation import find_boundaries
        from skimage.morphology import skeletonize
        from skimage.morphology import binary_closing, binary_opening
        from skimage.segmentation import expand_labels
        if self.epicure.verbose > 0:
            print("********** Generate touching labels image ***********")

        ## skeletonize it
        skel = skeletonize( binary_closing( find_boundaries(labs), footprint=np.ones((10,10)) ) )
        ext = np.zeros(labs.shape, dtype="uint8")
        ext[labs==0] = 1
        ext = binary_opening(ext, footprint=np.ones((2,2)))
        newimg = expand_labels(labs, distance=4)
        newimg[ext>0] = 0
        return newimg
    
    def to_ncp(self):
        """ Export current frame to new viewer and makes it ready for napari-cluster-plots plugin """
        try:
            import napari_skimage_regionprops as nsr
        except:
            ut.show_error("Plugin napari-skimage-regionprops is not installed")
            return
        gview = napari.Viewer()
        tframe = ut.current_frame(self.viewer)
        segt = self.epicure.seglayer.data[tframe]
        moviet = self.epicure.viewer.layers["Movie"].data[tframe]
        lab = gview.add_labels(segt, name="Segmentation[t="+str(tframe)+"]", blending="additive")
        im = gview.add_image(moviet, name="Movie[t="+str(tframe)+"]", blending="additive")
        if self.epicure.verbose > 0:
            print("Measure features with napari-skimage-regionprops plugin...")
        nsr.regionprops_table(im.data, lab.data, size=True, intensity=True, perimeter=True, shape=True, position=True, moments=True, napari_viewer=gview)
        try:
            import napari_clusters_plotter as ncp
        except:
            ut.show_error("Plugin napari-clusters-plotter is not installed")
            return
        gview.window.add_dock_widget(ncp.ClusteringWidget(gview))
        gview.window.add_dock_widget(ncp.PlotterWidget(gview))

    def temporal_graphs(self):
        """ New window with temporal graph of the current table selection """
        #self.temporal_viewer = napari.Viewer()
        self.tplots = TemporalPlots(self.viewer)
        self.tplots.setTable(self.table)
        self.plot_wid = self.viewer.window.add_dock_widget( self.tplots, name="Plots" )
        self.viewer.dims.events.current_step.connect(self.position_verticalline)
    
    def on_close_viewer(self):
        """ Temporal plots window is closed """
        if self.epicure.verbose > 1:
            print("Closed viewer")
        self.viewer.dims.events.current_step.disconnect(self.position_verticalline)
        self.temporal_viewer = None
        self.tplots = None

    def position_verticalline(self):
        """ Place the vertical line in the temporal graph to the current frame """
        try:
            wid = self.plot_wid
        except:
            self.on_close_viewer()
        if self.tplots is not None:
            self.tplots.move_framepos(self.viewer.dims.current_step[0])

    ### track features 
    def show_trackfeature_table(self):
        """ Show the measurement of tracks table """
        self.measure_track_features()
        self.trackTable.set_table( self.table )
    
    def measure_track_features(self):
        """ Measure track features and put them to table """
        if self.epicure.verbose > 0:
            print("Measuring track features")
        self.viewer.window._status_bar._toggle_activity_dock(True)
        start_time = time.time()

        if self.output_mode.currentText() == "Only selected cell": 
            track_ids = self.epicure.seglayer.selected_label
        else:
            if self.output_mode.currentText() == "All cells": 
                track_ids = self.epicure.tracking.get_track_list()
            else:
                group = self.output_mode.currentText()
                track_ids = []
                label_group = self.epicure.groups[group]
                for lab in label_group:
                    track_ids.append(lab)
            
        properties = ["label", "area", "centroid"]
        self.table = None

        if type(track_ids) == int:
            track_ids = [track_ids]
        for itrack, track_id in progress(enumerate(track_ids)):
                track_frame = self.measure_one_track( track_id )
                if self.table is None:
                    self.table = pand.DataFrame([track_frame])
                else:
                    self.table = pand.concat([self.table, pand.DataFrame([track_frame])])

        self.table_selection = self.selection_choices.index(self.output_mode.currentText())
        self.viewer.window._status_bar._toggle_activity_dock(False)
        show_info("Features measured in "+"{:.3f}".format((time.time()-start_time)/60)+" min")

    def measure_one_track( self, track_id ):
        """ Measure features of one track """
        track_features = self.epicure.tracking.measure_track_features( track_id )
        return track_features

        

class FeaturesTable(QWidget):
    """ Widget to visualize and interact with the measurement table """

    def __init__(self, napari_viewer, epicure):
        super().__init__()
        self.viewer = napari_viewer
        self.epicure = epicure
        self.wid_table = QTableWidget()
        self.wid_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setLayout(QGridLayout())
        self.layout().addWidget(self.wid_table)
        self.wid_table.clicked.connect(self.show_label)
        self.wid_table.setSortingEnabled(True)

    def show_label(self):
        """ When click on the table, show selected cell """
        if self.wid_table is not None:
            row = self.wid_table.currentRow()
            self.epicure.seglayer.show_selected_label = False
            headers = [self.wid_table.horizontalHeaderItem(ind).text() for ind in range(self.wid_table.columnCount()) ]
            labelind = None
            if "label" in headers:
                labelind = headers.index("label") 
            if "Label" in headers:
                labelind = headers.index("Label") 
            frameind = None
            if "frame" in headers:
                frameind = headers.index("frame") 
            if labelind is not None and labelind >= 0:
                lab = int(self.wid_table.item(row, labelind).text())
                if frameind is not None:
                    ## set current frame to the selected row
                    frame = int(self.wid_table.item(row, frameind).text())
                    ut.set_frame(self.viewer, frame)
                else:
                    ## set current frame to the first frame where label or track is present
                    frame = self.epicure.tracking.get_first_frame( lab )
                    if frame is not None:
                        ut.set_frame(self.viewer, frame)
                self.epicure.seglayer.selected_label = lab
                self.epicure.seglayer.show_selected_label = True


    def get_features_list(self):
        """ Return list of measured features """
        return [ self.wid_table.horizontalHeaderItem(ind).text() for ind in range(self.wid_table.columnCount()) ]

    def set_table(self, table):
        self.wid_table.clear()
        self.wid_table.setRowCount(table.shape[0])
        self.wid_table.setColumnCount(table.shape[1])

        for c, column in enumerate(table.keys()):
            column_name = column
            self.wid_table.setHorizontalHeaderItem(c, QTableWidgetItem(column_name))
            for r, value in enumerate(table.get(column)):
                item = QTableWidgetItem()
                item.setData( Qt.EditRole, value)
                self.wid_table.setItem(r, c, item)

class TemporalPlots(QWidget):
    """ Widget to visualize and interact with temporal plots """

    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.features_list = ["frame"]
        self.parameter_gui()
        self.vline = None
        #self.viewer.window.add_dock_widget( self.plot_wid, name="Temporal plot" )
   
    def parameter_gui(self):
        """ add widget to choose plotting parameters """
        
        layout = QVBoxLayout()

        feat_choice = QHBoxLayout()
        feat_choice_lab = QLabel()
        feat_choice_lab.setText("Plot feature")
        feat_choice.addWidget(feat_choice_lab)
        self.feature_choice = QComboBox()
        feat_choice.addWidget(self.feature_choice)
        layout.addLayout(feat_choice)

        self.avg_group = QCheckBox(text="Average by groups")
        layout.addWidget(self.avg_group)
        self.avg_group.setChecked(False)

        self.plot_wid = self.create_plotwidget()
        layout.addWidget(self.plot_wid)
        self.setLayout(layout)
        self.feature_choice.currentIndexChanged.connect(self.plot_feature)
        self.avg_group.stateChanged.connect(self.plot_feature)

    def setTable(self, table):
        """ Data table to plot """
        self.table = table
        self.features_list = self.table.keys()
        self.update_feature_list()

    def update_table(self, table):
        """ Update the current plot with the updated table """
        self.table = table
        curchoice = self.feature_choice.currentText()
        self.features_list = self.table.keys()
        self.update_feature_list()
        if curchoice in self.features_list:
            ind = list(self.features_list).index(curchoice)
            self.feature_choice.setCurrentIndex(ind)
        self.plot_feature()

    def update_feature_list(self):
        """ Update the list of feature in the GUI """
        self.feature_choice.clear()
        for feat in self.features_list:
            self.feature_choice.addItem(feat)
    
    def plot_feature(self):
        """ Plot the selected feature in the temporal graph """
        feat = self.feature_choice.currentText()
        if feat == "label":
            return
        if feat == "":
            return
        self.ax.cla()
        tab = list(zip(self.table["frame"], self.table[feat], self.table["label"], self.table["group"]))
        df = pand.DataFrame( tab, columns=["frame", feat, "label", "group"] )
        #df["group"] = df["group"].replace("None", "Ungrouped")
        df.set_index('frame', inplace=True)
        #self.ax.plot(self.table["frame"], self.table[feat])
        if self.avg_group.isChecked():
            dfmean = df.groupby(['group', 'frame'])[feat].mean().reset_index()
            dfmean.set_index('frame', inplace=True)
            df.columns.name = 'group'
            dfmean.groupby('group')[feat].plot(legend=False, ax=self.ax)
            self.ax.legend(np.unique(dfmean['group']))
        else:
            df.groupby('label')[feat].plot(legend=False, ax=self.ax)
        self.ax.set_ylabel(''+feat)
        self.ax.set_xlabel('Time (frame)')
        self.fig.canvas.draw_idle()
        self.ymin, self.ymax = self.ax.get_ylim()

    def move_framepos(self, frame):
        """ Move the vertical line showing the current frame position in the main window """
        if self.ax is not None:
            if self.vline is not None:
                self.vline.remove()
            ymin = float(self.ymin*1.01)
            ymax = float(self.ymax*0.99)
            self.vline = self.ax.vlines(x=frame, ymin=ymin, ymax=ymax, ls=':', color="0.6")
            self.fig.canvas.draw_idle()

    def create_plotwidget(self):
        """ Create plot window """
        mpl_widget = FigureCanvas( Figure(figsize=(6,6) ) )
        self.fig = mpl_widget.figure
        self.ax = mpl_widget.figure.subplots()
        return mpl_widget

    

