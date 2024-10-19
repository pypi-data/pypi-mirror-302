import numpy as np
import os
from math import ceil
from qtpy.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QCheckBox, QSlider, QLabel, QDoubleSpinBox, QComboBox, QLineEdit
from qtpy.QtCore import Qt
from magicgui.widgets import TextEdit
import epicure.Utils as ut


class Displaying(QWidget):
    """ Propose some visualization options """

    def __init__(self, napari_viewer, epic):
        """ Create displaying widget instance """
        super().__init__()
        self.viewer = napari_viewer
        self.epicure = epic
        self.seglayer = self.viewer.layers["Segmentation"]
        self.gmode = 0  ## view only movie mode on/off
        self.dmode = 0  ## view with light segmentation on/off

        layout = QVBoxLayout()
        
        ## Show a text window with some summary of the file
        show_summary = QPushButton("Show summary", parent=self)
        layout.addWidget(show_summary)
        show_summary.clicked.connect(self.show_summary_window)
        
        ## Option show segmentation skeleton
        show_skeleton_line = QHBoxLayout()
        self.show_skeleton = QCheckBox(text="Show segmentation skeleton")
        show_skeleton_line.addWidget(self.show_skeleton)
        self.show_skeleton.stateChanged.connect(self.show_skeleton_segmentation)
        layout.addLayout(show_skeleton_line)
        self.show_skeleton.setChecked(False)
        
        ## Option show shifted segmentation
        show_shifted_line = QHBoxLayout()
        self.show_shifted = QCheckBox(text="Overlay previous segmentation")
        show_shifted_line.addWidget(self.show_shifted)
        self.show_shifted.stateChanged.connect(self.show_shifted_segmentation)
        layout.addLayout(show_shifted_line)
        self.show_shifted.setChecked(False)
        
        ## Option show shifted movie (previous or next)
        show_prevmovie_line = QHBoxLayout()
        self.show_previous_movie = QCheckBox(text="Overlay previous movie")
        show_prevmovie_line.addWidget(self.show_previous_movie)
        self.show_previous_movie.stateChanged.connect(self.show_shifted_previous_movie)
        layout.addLayout(show_prevmovie_line)
        self.show_previous_movie.setChecked(False)
        show_nextmovie_line = QHBoxLayout()
        self.show_next_movie = QCheckBox(text="Overlay next movie")
        show_nextmovie_line.addWidget(self.show_next_movie)
        self.show_next_movie.stateChanged.connect(self.show_shifted_next_movie)
        layout.addLayout(show_nextmovie_line)
        self.show_next_movie.setChecked(False)
        
        ## Option create/show grid
        self.show_grid_options = QCheckBox(text="Grid options")
        self.grid_parameters()
        layout.addWidget(self.show_grid_options)
        layout.addWidget(self.group_grid)
        self.show_grid_options.setChecked(False)
        self.show_grid_options.stateChanged.connect(self.grid_group_visibility)
        self.grid_group_visibility()
        
        self.add_display_overlay_message()
        self.key_bindings()        ## activate shortcuts for display options
        self.setLayout(layout)
        ut.set_active_layer( self.viewer, "Segmentation" )
    

    ######### overlay message
    def add_display_overlay_message(self):
        """ Shortcut list for display options """
        disptext = "--- Display options --- \n"
        disptext = disptext + "  <b> show/hide segmentation layer \n"
        disptext = disptext + "  <v> show/hide movie layer \n"
        disptext = disptext + "  <x> show/hide suspects layer \n"
        disptext = disptext + "  <c> show ONLY movie layer \n"
        disptext = disptext + "  <d> on/off light segmentation view \n"
        disptext = disptext + "  <Ctrl-c>/<Ctrl-d> increase/decrease label contour \n"
        disptext = disptext + "  <k> show/update segmentation skeleton \n"
        disptext = disptext + "  <g> show/hide grid \n"
        self.epicure.overtext["Display"] = disptext

    def show_summary_window(self):
        """ Show a text window with some infos """
        summwin = TextEdit()
        summwin.name = "Epicure summary"
        summwin.value = self.epicure.get_summary()
        summwin.show()


    ################  Key binging for display options
    def key_bindings(self):
        
        @self.seglayer.bind_key('b', overwrite=True)
        def see_segmentlayer(seglayer):
            seglayer.visible = not seglayer.visible
        
        @self.seglayer.bind_key('v', overwrite=True)
        def see_movielayer(seglayer):
            ut.inv_visibility(self.viewer, "Movie")
        
        @self.seglayer.bind_key('x', overwrite=True)
        def see_suspectslayer(seglayer):
            suslayer = self.viewer.layers["Suspects"]
            suslayer.visible = not suslayer.visible
        
        @self.seglayer.bind_key('k', overwrite=True)
        def show_skeleton(seglayer):
            """ On/Off show skeleton """
            if self.show_skeleton.isChecked():
                self.show_skeleton.setChecked(False)
            else:
                self.show_skeleton.setChecked(True)

        @self.seglayer.bind_key('Control-c', overwrite=True)
        def contour_increase(seglayer):
            if seglayer is not None:
                seglayer.contour = seglayer.contour + 1
        
        @self.seglayer.bind_key('Control-d', overwrite=True)
        def contour_decrease(seglayer):
            if seglayer is not None:
                if seglayer.contour > 0:
                    seglayer.contour = seglayer.contour - 1
        
        @self.seglayer.bind_key('c', overwrite=True)
        def see_onlymovielayer(seglayer):
            """ if in "g" mode, show only movie, else put back to previous views """
            if self.gmode == 0:
                self.lay_view = []
                for lay in self.viewer.layers:
                    self.lay_view.append( (lay, lay.visible) )
                    lay.visible = False
                ut.inv_visibility(self.viewer, "Movie")
                self.gmode = 1
            else:
                for lay, vis in self.lay_view:
                    lay.visible = vis
                self.gmode = 0

        @self.seglayer.bind_key('d', overwrite=True)
        def segmentation_lightmode(seglayer):
            """ if in "d" mode, show only movie and light segmentation, else put back to previous views """
            if self.dmode == 0:
                self.light_view = []
                for lay in self.viewer.layers:
                    self.light_view.append( (lay, lay.visible) )
                    lay.visible = False
                ut.inv_visibility(self.viewer, "Movie")
                ut.inv_visibility(self.viewer, "Segmentation")
                self.unlight_contour = self.seglayer.contour
                self.unlight_opacity = self.seglayer.opacity
                self.seglayer.contour = 1
                self.seglayer.opacity = 0.2
                self.dmode = 1
            else:
                for lay, vis in self.light_view:
                    lay.visible = vis
                self.seglayer.contour = self.unlight_contour
                self.seglayer.opacity = self.unlight_opacity
                self.dmode = 0
        
        @self.seglayer.bind_key('g', overwrite=True)
        def show_grid(seglayer):
            """ show/hide the grid to have a repere in space """
            self.show_grid()

    def show_skeleton_segmentation(self):
        """ Show/hide/update skeleton """
        if "Skeleton" in self.viewer.layers:
            ut.remove_layer(self.viewer, "Skeleton")
        if self.show_skeleton.isChecked():
            self.epicure.add_skeleton()
            ut.set_active_layer( self.viewer, "Segmentation" )


    def show_shifted_segmentation(self):
        """ Show/Hide temporally shifted segmentation on top of current one """
        if ("PrevSegmentation" in self.viewer.layers):
            if (not self.show_shifted.isChecked()):
                ut.remove_layer(self.viewer, "PrevSegmentation")
            else:
                lay = self.viewer.layers["PrevSegmentation"]
                lay.refresh()

        if ("PrevSegmentation" not in self.viewer.layers) and (self.show_shifted.isChecked()):
            if self.epicure.nframes > 1:
                layer = self.viewer.add_labels( self.seglayer.data, name="PrevSegmentation", blending="additive", opacity=0.4 )
                layer.contour = 2
                layer.translate = [1, 0, 0]
                self.seglayer.contour = 2
                self.seglayer.opacity = 0.6
            else:
                ut.show_warning("Still image, cannot show previous frames")

        ut.set_active_layer( self.viewer, "Segmentation" )
    
    def show_shifted_previous_movie(self):
        """ Show/Hide temporally shifted movie previous frame on top of current one """
        self.show_shifted_movie("PrevMovie", "red", 1)
    
    def show_shifted_next_movie(self):
        """ Show/Hide temporally shifted movie next frame on top of current one """
        self.show_shifted_movie("NextMovie", "green", -1)
    
    def show_shifted_movie(self, layname, color, translation):
        """ Show/Hide temporally shifted movie on top of current one """
        if (layname in self.viewer.layers):
            if (not self.show_previous_movie.isChecked()):
                ut.remove_layer(self.viewer, layname)
            else:
                lay = self.viewer.layers[layname]
                lay.refresh()

        if (layname not in self.viewer.layers) and (self.show_previous_movie.isChecked()):
            if self.epicure.nframes > 1:
                movlay = self.viewer.layers["Movie"]
                arr = movlay.data
                if translation == -1:
                    arr = movlay.data[1:,]
                layer = self.viewer.add_image( arr, name=layname, blending="additive", opacity=0.6, colormap=color )
                if translation == 1:
                    layer.translate = [translation, 0, 0]
                layer.contrast_limits=self.epicure.quantiles()
                layer.gamma=0.94
            else:
                ut.show_warning("Still image, cannot show previous frames")

        ut.set_active_layer( self.viewer, "Segmentation" )

    #### Show/load a grid to have a repere in space
    def grid_group_visibility(self):
        """ Show/hide grid parameters """
        self.group_grid.setVisible(self.show_grid_options.isChecked())

    def grid_parameters(self):
        """ Interface to get grid parameters """
        self.group_grid = QGroupBox("Grid setup")
        grid_layout = QVBoxLayout()
        ## nrows
        rows_line = QHBoxLayout()
        rows_lab = QLabel()
        rows_lab.setText("Nb rows:")
        rows_line.addWidget(rows_lab)
        self.nrows = QLineEdit()
        self.nrows.setText("3")
        rows_line.addWidget(self.nrows)
        grid_layout.addLayout(rows_line)
        ## ncols
        cols_line = QHBoxLayout()
        cols_lab = QLabel()
        cols_lab.setText("Nb columns:")
        cols_line.addWidget(cols_lab)
        self.ncols = QLineEdit()
        self.ncols.setText("3")
        cols_line.addWidget(self.ncols)
        grid_layout.addLayout(cols_line)
        ## grid edges width
        width_line = QHBoxLayout()
        width_lab = QLabel()
        width_lab.setText("Grid width:")
        width_line.addWidget(width_lab)
        self.gwidth = QLineEdit()
        self.gwidth.setText("4")
        width_line.addWidget(self.gwidth)
        grid_layout.addLayout(width_line)
        #self.gwidth.changed.connect(self.add_grid)
        ## go for grid
        btn_add_grid = QPushButton("Add grid", parent=self)
        grid_layout.addWidget(btn_add_grid)
        btn_add_grid.clicked.connect(self.add_grid)
        self.group_grid.setLayout(grid_layout)

    def add_grid(self):
        """ Create/Load a new grid and add it """
        ut.remove_layer(self.viewer, "EpicGrid")
        imshape = self.epicure.imgshape2D
        if imshape is None:
            ut.show_error("Load the image first")
            return
        nrows = int(self.nrows.text())
        ncols = int(self.ncols.text())
        wid = ceil(imshape[0]/nrows)
        hei = ceil(imshape[1]/ncols)
        rects = []
        rects_names = []
        gwidth = int(self.gwidth.text())
        for x in range(nrows):
            for y in range(ncols):
                rect = np.array([[x*wid, y*hei], [(x+1)*wid, (y+1)*hei]])
                rects.append(rect)
                rects_names.append(chr(65+x)+"_"+str(y))
        self.viewer.add_shapes(rects, name="EpicGrid", text=rects_names, face_color=[1,0,0,0], edge_color=[0.7,0.7,0.7,0.7], edge_width=gwidth, opacity=0.8)
        ut.set_active_layer( self.viewer, "Segmentation" )

    def show_grid(self):
        """ Interface to create/load a grid for repere """
        if "EpicGrid" not in self.viewer.layers:
            self.add_grid()
        else:
            gridlay = self.viewer.layers["EpicGrid"]
            gridlay.visible = not gridlay.visible
