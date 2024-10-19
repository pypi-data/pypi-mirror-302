import numpy as np
import os
import napari
from skimage.measure import regionprops, label
from skimage import filters
from skimage.morphology import binary_erosion, binary_dilation, disk
from qtpy.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QWidget, QCheckBox, QSlider, QLabel, QDoubleSpinBox, QComboBox, QSpinBox, QLineEdit
from qtpy.QtCore import Qt
import epicure.Utils as ut
from skimage.segmentation import expand_labels
from napari.utils import progress
try:
    from skimage.graph import RAG
except:
    from skimage.future.graph import RAG  ## older version of scikit-image

"""
    EpiCure - Suspects interface
    Handle suspects and suggestion layer
"""

class Suspecting(QWidget):
    
    def __init__(self, napari_viewer, epic):
        super().__init__()
        self.viewer = napari_viewer
        self.epicure = epic
        self.seglayer = self.viewer.layers["Segmentation"]
        self.border_cells = None    ## list of cells that are on the border (touch the background)
        self.suspectlayer_name = "Suspects"
        self.suspects = None
        self.win_size = 10

        ## Print the current number of suspects
        self.nsuspect_print = QLabel("")
        self.update_nsuspects_display()
        
        self.create_suspectlayer()
        layout = QVBoxLayout()
        layout.addWidget( self.nsuspect_print )
        
        ### Reset: delete all suspects
        reset_suspect_btn = QPushButton("Reset suspects", parent=self)
        layout.addWidget(reset_suspect_btn)
        reset_suspect_btn.clicked.connect(self.reset_all_suspects)
        
        ## Error suggestions based on cell features
        outlier_vis = QCheckBox(text="Outliers options")
        outlier_vis.setChecked(False)
        layout.addWidget(outlier_vis)
        self.create_outliersBlock() 
        outlier_vis.stateChanged.connect(self.show_outlierBlock)
        layout.addWidget(self.featOutliers)
        
        ## Error suggestions based on tracks
        track_vis = QCheckBox(text="Track options")
        track_vis.setChecked(True)
        layout.addWidget(track_vis)
        self.create_tracksBlock() 
        track_vis.stateChanged.connect(self.show_tracksBlock)
        layout.addWidget(self.suspectTrack)
        
        ## Visualisation options
        suspect_disp = QCheckBox(text="Display options")
        suspect_disp.setChecked(True)
        layout.addWidget(suspect_disp)
        self.create_displaySuspectBlock() 
        suspect_disp.stateChanged.connect(self.show_displaySuspectBlock)
        layout.addWidget(self.displaySuspect)
        self.displaySuspect.setVisible(True)
        
        self.setLayout(layout)
        self.key_binding()

    def key_binding(self):
        """ active key bindings for suspects options """
        self.epicure.overtext["suspects"] = "---- Suspects editing ---- \n"
        self.epicure.overtext["suspects"] += "<Ctrl>+<Alt>+Left click to zoom on a suspect \n"
        self.epicure.overtext["suspects"] += "<Ctrl>+<Alt>+Right click to remove a suspect \n"
        self.epicure.overtext["suspects"] += "<Space bar> zoom on next suspect \n"
   
        @self.epicure.seglayer.mouse_drag_callbacks.append
        def handle_suspect(seglayer, event):
            if event.type == "mouse_press":
                if len(event.modifiers)==2:
                    if ("Control" in event.modifiers) and ('Alt' in event.modifiers):
                        if event.button == 2:
                            ind = ut.getCellValue( self.suspects, event ) 
                            if self.epicure.verbose > 1:
                                print("Removing clicked suspect, at index "+str(ind))
                            if ind is None:
                                ## click was not on a suspect
                                return
                            sid = self.suspects.properties["id"][ind]
                            if sid is not None:
                                self.exonerate_one(ind)
                            else:
                                if self.epicure.verbose > 1:
                                    print("Suspect with id "+str(sid)+" not found")
                            self.remove_suspicions( sid )
                            self.suspects.refresh()
                        if event.button == 1:
                            ind = ut.getCellValue( self.suspects, event ) 
                            sid = self.suspects.properties["id"][ind]
                            if self.epicure.verbose > 1:
                                print("Zoom on suspect with id "+str(sid)+"")
                            self.zoom_on_suspect( event.position, sid )

        @self.epicure.seglayer.bind_key('Space', overwrite=True)
        def go_next(seglayer):
            """ Select next suspect and zoom on it """
            num_suspect = int(self.suspect_num.value())
            if num_suspect < 0:
                if self.nb_suspects() == "_":
                    if self.epicure.verbose > 0:
                        print("No more suspect")
                    return  
                else:
                    self.suspect_num.setValue(0)
            else:
                self.suspect_num.setValue( (num_suspect+1)%(self.nb_suspects()) )
            self.go_to_suspect()       

    def create_suspectlayer(self):
        """ Create a point layer that contains the suspects """
        features = {}
        pts = []
        self.suspects = self.viewer.add_points( np.array(pts), properties=features, face_color="red", size = 10, symbol='x', name=self.suspectlayer_name, )
        self.suspicions = {}
        self.update_nsuspects_display()
        self.epicure.finish_update()

    def load_suspects(self, pts, features, suspicions, symbols=None, colors=None):
        """ Load suspects data from file and reinitialize layer with it"""
        ut.remove_layer(self.viewer, self.suspectlayer_name)
        if symbols is None:
            symbols = "x"
        if colors is None:
            colors = "red"
        symb = symbols
        self.suspects = self.viewer.add_points( np.array(pts), properties=features, face_color=colors, size = 10, symbol=symbols, name=self.suspectlayer_name, )
        self.suspicions = suspicions
        self.update_nsuspects_display()
        self.epicure.finish_update()

        
    ############### Display suspect options

    def update_nsuspects_display( self ):
        """ Update the display of number of suspect"""
        self.nsuspect_print.setText( str(self.nb_suspects())+" suspects" )

    def nb_suspects(self):
        """ Returns current number of suspects """
        if self.suspects is None:
            return "_"
        if self.suspects.properties is None:
            return "_"
        if "score" not in self.suspects.properties:
            return "_"
        return len(self.suspects.properties["score"])

    def show_displaySuspectBlock(self):
        self.displaySuspect.setVisible(not self.displaySuspect.isVisible())

    def create_displaySuspectBlock(self):
        ''' Block interface of displaying suspect layer options '''
        self.displaySuspect = QGroupBox("Display options")
        disp_layout = QVBoxLayout()
        
        ## Color mode
        colorlay = QHBoxLayout()
        color_label = QLabel()
        color_label.setText("Color by:")
        colorlay.addWidget(color_label)
        self.color_choice = QComboBox()
        colorlay.addWidget(self.color_choice)
        self.color_choice.addItem("None")
        self.color_choice.addItem("score")
        self.color_choice.addItem("tracking-2->1")
        self.color_choice.addItem("tracking-1-2-*")
        self.color_choice.addItem("track-length")
        self.color_choice.addItem("division")
        self.color_choice.addItem("area")
        self.color_choice.addItem("solidity")
        self.color_choice.addItem("intensity")
        self.color_choice.addItem("tubeness")
        self.color_choice.currentIndexChanged.connect(self.color_suspects)
        disp_layout.addLayout(colorlay)
        
        sizelay = QHBoxLayout()
        size_label = QLabel()
        size_label.setText("Point size:")
        sizelay.addWidget(size_label)
        self.suspect_size = QSlider(Qt.Horizontal)
        self.suspect_size.setMinimum(0)
        self.suspect_size.setMaximum(50)
        self.suspect_size.setSingleStep(1)
        self.suspect_size.setValue(10)
        self.suspect_size.valueChanged.connect(self.display_suspect_size)
        sizelay.addWidget(self.suspect_size)
        disp_layout.addLayout(sizelay)

        ### Interface to select a suspect and zoom on it
        chooselay = QHBoxLayout()
        choose_lab = QLabel()
        choose_lab.setText("Suspect n°")
        chooselay.addWidget(choose_lab)
        self.suspect_num = QSpinBox()
        self.suspect_num.setMinimum(0)
        self.suspect_num.setMaximum(len(self.suspects.data)-1)
        self.suspect_num.setSingleStep(1)
        self.suspect_num.setValue(0)
        chooselay.addWidget(self.suspect_num)
        disp_layout.addLayout(chooselay)
        go_suspect_btn = QPushButton("Go to suspect", parent=self)
        disp_layout.addWidget(go_suspect_btn)
        go_suspect_btn.clicked.connect(self.go_to_suspect)
        clear_suspect_btn = QPushButton("Exonerate current suspect", parent=self)
        disp_layout.addWidget(clear_suspect_btn)
        clear_suspect_btn.clicked.connect(self.clear_suspect)
        
        ## all features
        self.displaySuspect.setLayout(disp_layout)
       
    #####
    def reset_suspect_range(self):
        """ Reset the max num of suspect """
        nsus = len(self.suspects.data)-1
        if self.suspect_num.value() > nsus:
            self.suspect_num.setValue(0)
        self.suspect_num.setMaximum(nsus)

    def go_to_suspect(self):
        """ Zoom on the currently selected suspect """
        num_suspect = int(self.suspect_num.value())
        if num_suspect < 0:
            if self.nb_suspects() == "_":
                if self.epicure.verbose > 0:
                    print("No more suspect")
                return  
            else:
                self.suspect_num.setValue(0)
                num_suspect = 0      
        pos = self.suspects.data[num_suspect]
        suspect_id = self.suspects.properties["id"][num_suspect]
        self.zoom_on_suspect( pos, suspect_id )

    def zoom_on_suspect( self, suspect_pos, suspect_id ):
        """ Zoom on chose suspect at given position """
        self.viewer.camera.center = suspect_pos
        self.viewer.camera.zoom = 5
        self.viewer.dims.set_point( 0, int(suspect_pos[0]) )
        crimes = self.get_crimes(suspect_id)
        if self.epicure.verbose > 0:
            print("Suspected because of: "+str(crimes))

    def color_suspects(self):
        """ Color points by the selected mode """
        color_mode = self.color_choice.currentText()
        self.suspects.refresh_colors()
        if color_mode == "None":
            self.suspects.face_color = "white"
        elif color_mode == "score":
            self.set_colors_from_properties("score")
        else:
            self.set_colors_from_suspicion(color_mode)
        self.suspects.refresh_colors()

    def set_colors_from_suspicion(self, feature):
        """ Set colors from given suspicion feature (eg area, tracking..) """
        if self.suspicions.get(feature) is None:
            self.suspects.face_color="white"
            return
        posid = self.suspicions[feature]
        colors = ["white"]*len(self.suspects.data)
        ## change the color of all the positive suspects for the chosen feature
        for sid in posid:
            ind = self.index_from_id(sid)
            if ind is not None:
                colors[ind] = (0.8,0.1,0.1)
        self.suspects.face_color = colors

    def set_colors_from_properties(self, feature):
        """ Set colors from given propertie (eg score, label) """
        ncols = (np.max(self.suspects.properties[feature]))
        color_cycle = []
        for i in range(ncols):
            color_cycle.append( (0.25+float(i/ncols*0.75), float(i/ncols*0.85), float(i/ncols*0.75)) )
        self.suspects.face_color_cycle = color_cycle
        self.suspects.face_color = feature
    
    def update_display(self):
        self.suspects.refresh()
        self.color_suspects()

    def display_suspect_size(self):
        """ Change the size of the point display """
        size = int(self.suspect_size.value())
        self.suspects.size = size
        self.suspects.refresh()

    ############### Suspecting functions
    def get_crimes(self, sid):
        """ For a given suspect, get its suspicion(s) """
        crimes = []
        for feat in self.suspicions.keys():
            if sid in self.suspicions.get(feat):
                crimes.append(feat)
        return crimes

    def add_suspicion(self, ind, sid, feature):
        """ Add 1 to the suspicion score for given feature """
        #print(self.suspicions)
        if self.suspicions.get(feature) is None:
            self.suspicions[feature] = []
        self.suspicions[feature].append(sid)
        self.suspects.properties["score"][ind] = self.suspects.properties["score"][ind] + 1

    def first_suspect(self, pos, label, featurename):
        """ Addition of the first suspect (initialize all) """
        ut.remove_layer(self.viewer, "Suspects")
        features = {}
        sid = self.new_suspect_id()
        features["id"] = np.array([sid], dtype="uint16")
        features["label"] = np.array([label], dtype=self.epicure.dtype)
        features["score"] = np.array([0], dtype="uint8")
        pts = [pos]
        self.suspects = self.viewer.add_points( np.array(pts), properties=features, face_color="score", size = 10, symbol="x", name="Suspects", )
        self.add_suspicion(0, sid, featurename)
        self.suspects.refresh()
        self.update_nsuspects_display()

    def add_suspect(self, pos, label, reason, symb="x", color="white"):
        """ Add a suspect to the list, suspected by a feature """
        if (self.ignore_borders.isChecked()) and (self.border_cells is not None):
            tframe = int(pos[0])
            if label in self.border_cells[tframe]:
                return

        ## initialise if necessary
        if len(self.suspects.data) <= 0:
            self.first_suspect(pos, label, reason)
            return
        
        self.suspects.selected_data = []
       
       ## look if already suspected, then add the charge
        num, sid = self.find_suspect(pos[0], label)
        if num is not None:
            ## suspect already in the list. For same crime ?
            if self.suspicions.get(reason) is not None:
                if sid not in self.suspicions[reason]:
                    self.add_suspicion(num, sid, reason)
            else:
                self.add_suspicion(num, sid, reason)
        else:
            ## new suspect, add to the Point layer
            ind = len(self.suspects.data)
            sid = self.new_suspect_id()
            self.suspects.add(pos)
            self.suspects.properties["label"][ind] = label
            self.suspects.properties["id"][ind] = sid
            self.suspects.properties["score"][ind] = 0
            self.add_suspicion(ind, sid, reason)

        self.suspects.symbol.flags.writeable = True
        self.suspects.current_symbol = symb
        self.suspects.current_face_color = color
        self.suspects.refresh()
        self.reset_suspect_range()
        self.update_nsuspects_display()

    def new_suspect_id(self):
        """ Find the first unused id """
        sid = 0
        if self.suspects.properties.get("id") is None:
            return 0
        while sid in self.suspects.properties["id"]:
            sid = sid + 1
        return sid
    
    def reset_all_suspects(self):
        """ Remove all suspicions """
        features = {}
        pts = []
        ut.remove_layer(self.viewer, "Suspects")
        self.suspects = self.viewer.add_points( np.array(pts), properties=features, face_color="red", size = 10, symbol='x', name="Suspects", )
        self.suspicions = {}
        self.update_nsuspects_display()
        self.update_nsuspects_display()

    def reset_suspicion(self, feature, frame):
        """ Remove all suspicions of given feature, for current frame or all if frame is None """
        if self.suspicions.get(feature) is None:
            return
        idlist = self.suspicions[feature].copy()
        for sid in idlist:
            ind = self.index_from_id(sid)
            if ind is not None:
                if frame is not None:
                    if int(self.suspects.data[ind][0]) == frame:
                        self.suspicions[feature].remove(sid)
                        self.decrease_score(ind)
                else:
                    self.suspicions[feature].remove(sid)
                    self.decrease_score(ind)
        self.suspects.refresh()
        self.update_nsuspects_display()

    def remove_suspicions(self, sid):
        """ Remove all suspicions of given suspect id """
        for listval in self.suspicions.values():
            if sid in listval:
                listval.remove(sid)

    def decrease_score(self, ind):
        """ Decrease by one score of suspect at index ind. Delete it if reach 0"""
        self.suspects.properties["score"][ind] = self.suspects.properties["score"][ind] - 1
        if self.suspects.properties["score"][ind] == 0:
            self.exonerate_one(ind)

    def index_from_id(self, sid):
        """ From suspect id, find the corresponding index in the properties array """
        for ind, cid in enumerate(self.suspects.properties["id"]):
            if cid == sid:
                return ind
        return None

    def find_suspect(self, frame, label):
        """ Find if there is already a suspect at given frame and label """
        suspects = self.suspects.data
        suspects_lab = self.suspects.properties["label"]
        for i, lab in enumerate(suspects_lab):
            if lab == label:
                if suspects[i][0] == frame:
                    return i, self.suspects.properties["id"][i]
        return None, None

    def init_suggestion(self):
        """ Initialize the layer that will contains propostion of tracks/segmentations """
        suggestion = np.zeros(self.seglayer.data.shape, dtype="uint16")
        self.suggestion = self.viewer.add_labels(suggestion, blending="additive", name="Suggestion")
        
        @self.seglayer.mouse_drag_callbacks.append
        def click(layer, event):
            if event.type == "mouse_press":
                if 'Alt' in event.modifiers:
                    if event.button == 1:
                        pos = event.position
                        # alt+left click accept suggestion under the mouse pointer (in all frames)
                        self.accept_suggestion(pos)
    
    def accept_suggestion(self, pos):
        """ Accept the modifications of the label at position pos (all the label) """
        seglayer = self.viewer.layers["Segmentation"]
        label = self.suggestion.data[tuple(map(int, pos))]
        found = self.suggestion.data==label
        self.exonerate( found, seglayer ) 
        indices = np.argwhere( found )
        ut.setNewLabel( seglayer, indices, label, add_frame=None )
        self.suggestion.data[self.suggestion.data==label] = 0
        self.suggestion.refresh()
        self.update_nsuspects_display()
    
    def exonerate_one(self, ind):
        """ Remove one suspect at index ind """
        self.suspects.selected_data = [ind]
        self.suspects.remove_selected()
        self.update_nsuspects_display()

    def clear_suspect(self):
        """ Remove the current suspect """
        num_suspect = int(self.suspect_num.value())
        self.exonerate_one( num_suspect )

    def exonerate_from_event(self, event):
        """ Remove all suspects in the corresponding cell of position """
        label = ut.getCellValue( self.seglayer, event )
        if len(self.suspects.data) > 0:
            for ind, lab in enumerate(self.suspects.properties["label"]):
                if lab == label:
                    if self.suspects.data[ind][0] == event.position[0]:
                        sid = self.suspects.properties["id"][ind]
                        self.exonerate_one(ind)
                        self.remove_suspicions(sid)

    def exonerate(self, indices, seglayer):
        """ Remove suspects that have been corrected/cleared """
        seglabels = np.unique(seglayer.data[indices])
        selected = []
        if self.suspects.properties.get("label") is None:
            return
        for ind, lab in enumerate(self.suspects.properties["label"]):
            if lab in seglabels:
                ## label to remove from suspect list
                selected.append(ind)
        if len(selected) > 0:
            self.suspects.selected_data = selected
            self.suspects.remove_selected()
            self.update_nsuspects_display()
                

    #######################################"
    ## Outliers suggestion functions
    def show_outlierBlock(self):
        self.featOutliers.setVisible(not self.featOutliers.isVisible())

    def create_outliersBlock(self):
        ''' Block interface of functions for error suggestions based on cell features '''
        self.featOutliers = QGroupBox("Outliers highlight")
        feat_layout = QVBoxLayout()
        # option to avoid checked cell
        #self.feat_checked = QCheckBox(text="Ignore checked cells")
        #self.feat_checked.setChecked(True)
        #feat_layout.addWidget(self.feat_checked)
        
        self.feat_onframe = QCheckBox(text="Only current frame")
        self.feat_onframe.setChecked(True)
        feat_layout.addWidget(self.feat_onframe)
        
        ## area widget
        feat_area_btn = QPushButton("Area outliers", parent=self)
        feat_area_btn.clicked.connect(self.suspect_area)
        farea_layout = QHBoxLayout()
        farea_layout.addWidget(feat_area_btn)
        self.farea_out = QDoubleSpinBox()
        self.farea_out.setRange(0,20)
        self.farea_out.decimals = 2
        self.farea_out.setSingleStep(0.25)
        self.farea_out.setValue(3)
        farea_layout.addWidget(self.farea_out)
        feat_layout.addLayout(farea_layout)
        #self.feat_area.stateChanged.connect(self.show_areaOutliers)
        
        ## solid widget
        feat_solid_btn = QPushButton(text="Solidity outliers", parent=self)
        feat_solid_btn.clicked.connect(self.suspect_solidity)
        fsolid_layout = QHBoxLayout()
        fsolid_layout.addWidget(feat_solid_btn)
        self.fsolid_out = QDoubleSpinBox()
        self.fsolid_out.setRange(0,20)
        self.fsolid_out.decimals = 2
        self.fsolid_out.setSingleStep(0.25)
        self.fsolid_out.setValue(3)
        fsolid_layout.addWidget(self.fsolid_out)
        feat_layout.addLayout(fsolid_layout)
        
        ## intensity widget
        feat_intensity_btn = QPushButton(text="Intensity (inside/periphery)")
        feat_intensity_btn.clicked.connect(self.suspect_intensity)
        fintensity_layout = QHBoxLayout()
        fintensity_layout.addWidget(feat_intensity_btn)
        self.fintensity_out = QDoubleSpinBox()
        self.fintensity_out.setRange(0,10)
        self.fintensity_out.decimals = 2
        self.fintensity_out.setSingleStep(0.05)
        self.fintensity_out.setValue(1.0)
        fintensity_layout.addWidget(self.fintensity_out)
        feat_layout.addLayout(fintensity_layout)
        
        ## tubeness widget
        feat_tub_btn = QPushButton(text="Tubeness (inside/periph)", parent=self)
        feat_tub_btn.clicked.connect(self.suspect_tubeness)
        ftub_layout = QHBoxLayout()
        ftub_layout.addWidget(feat_tub_btn)
        self.ftub_out = QDoubleSpinBox()
        self.ftub_out.setRange(0,10)
        self.ftub_out.decimals = 2
        self.ftub_out.setSingleStep(0.05)
        self.ftub_out.setValue(1)
        ftub_layout.addWidget(self.ftub_out)
        feat_layout.addLayout(ftub_layout)
        
        ## all features
        self.featOutliers.setLayout(feat_layout)
        self.featOutliers.setVisible(False)
    
    def suspect_feature(self, featname, funcname ):
        """ Suspect in one frame or all frames the given feature """
        onframe = self.feat_onframe.isChecked()
        if onframe:
            tframe = ut.current_frame(self.viewer)
            self.reset_suspicion(featname, tframe)
            funcname(tframe)
        else:
            self.reset_suspicion(featname, None)
            for frame in range(self.seglayer.data.shape[0]):
                funcname(frame)
        self.update_display()
        ut.set_active_layer( self.viewer, "Segmentation" )
    
    def inspect_outliers(self, tab, props, tuk, frame, feature):
        q1 = np.quantile(tab, 0.25)
        q3 = np.quantile(tab, 0.75)
        qtuk = tuk * (q3-q1)
        for sign in [1, -1]:
            #thresh = np.mean(tab) + sign * np.std(tab)*tuk
            if sign > 0:
                thresh = q3 + qtuk
            else:
                thresh = q1 - qtuk
            for i in np.where((tab-thresh)*sign>0)[0]:
                position = ut.prop_to_pos( props[i], frame )
                self.add_suspect( position, props[i].label, feature )
    
    def suspect_area(self, state):
        """ Look for outliers in term of cell area """
        self.suspect_feature( "area", self.suspect_area_oneframe )
    
    def suspect_area_oneframe(self, frame):
        seglayer = self.seglayer.data[frame]
        props = regionprops(seglayer)
        ncell = len(props)
        areas = np.zeros((ncell,1), dtype="float")
        for i, prop in enumerate(props):
            if prop.label > 0:
                areas[i] = prop.area
        tuk = self.farea_out.value()
        self.inspect_outliers(areas, props, tuk, frame, "area")

    def suspect_solidity(self, state):
        """ Look for outliers in term ofz cell solidity """
        self.suspect_feature( "solidity", self.suspect_solidity_oneframe )

    def suspect_solidity_oneframe(self, frame):
        seglayer = self.seglayer.data[frame]
        props = regionprops(seglayer)
        ncell = len(props)
        sols = np.zeros((ncell,1), dtype="float")
        for i, prop in enumerate(props):
            if prop.label > 0:
                sols[i] = prop.solidity
        tuk = self.fsolid_out.value()
        self.inspect_outliers(sols, props, tuk, frame, "solidity")
    
    def suspect_intensity(self, state):
        """ Look for abnormal intensity inside/periph ratio """
        self.suspect_feature( "intensity", self.suspect_intensity_oneframe )
    
    def suspect_intensity_oneframe(self, frame):
        seglayer = self.seglayer.data[frame]
        intlayer = self.viewer.layers["Movie"].data[frame] 
        props = regionprops(seglayer)
        for i, prop in enumerate(props):
            if prop.label > 0:
                self.test_intensity( intlayer, prop, frame )
    
    def test_intensity(self, inten, prop, frame):
        """ Test if intensity inside is much smaller than at periphery """
        bbox = prop.bbox
        intbb = inten[bbox[0]:bbox[2], bbox[1]:bbox[3]]
        footprint = disk(radius=self.epicure.thickness)
        inside = binary_erosion(prop.image, footprint)
        ininten = np.mean(intbb*inside)
        dil_img = binary_dilation(prop.image, footprint)
        periph = dil_img^inside
        periphint = np.mean(intbb*periph)
        if (periphint<=0) or (ininten/periphint > self.fintensity_out.value()):
            position = ( frame, int(prop.centroid[0]), int(prop.centroid[1]) )
            self.add_suspect( position, prop.label, "intensity" )
    
    def suspect_tubeness(self, state):
        """ Look for abnormal tubeness inside vs periph """
        self.suspect_feature( "tubeness", self.suspect_tubeness_oneframe )
    
    def suspect_tubeness_oneframe(self, frame):
        seglayer = self.seglayer.data[frame]
        mov = self.viewer.layers["Movie"].data[frame]
        sated = np.copy(mov)
        sated = filters.sato(sated, black_ridges=False)
        props = regionprops(seglayer)
        for i, prop in enumerate(props):
            if prop.label > 0:
                self.test_tubeness( sated, prop, frame )

    def test_tubeness(self, sated, prop, frame):
        """ Test if tubeness inside is much smaller than tubeness on periph """
        bbox = prop.bbox
        satbb = sated[bbox[0]:bbox[2], bbox[1]:bbox[3]]
        footprint = disk(radius=self.epicure.thickness)
        inside = binary_erosion(prop.image, footprint)
        intub = np.mean(satbb*inside)
        periph = prop.image^inside
        periphtub = np.mean(satbb*periph)
        if periphtub <= 0:
            position = ( frame, int(prop.centroid[0]), int(prop.centroid[1]) )
            self.add_suspect( position, prop.label, "tubeness" )
        else:
            if intub/periphtub > self.ftub_out.value():
                position = ( frame, int(prop.centroid[0]), int(prop.centroid[1]) )
                self.add_suspect( position, prop.label, "tubeness" )


############# Suspect based on track

    def show_tracksBlock(self):
        self.suspectTrack.setVisible(not self.suspectTrack.isVisible())

    def create_tracksBlock(self):
        ''' Block interface of functions for error suggestions based on tracks '''
        self.suspectTrack = QGroupBox("Tracks")
        track_layout = QVBoxLayout()
        
        self.get_div = QCheckBox(text="Get potential divisions")
        self.get_div.setChecked(True)
        track_layout.addWidget(self.get_div)
        
        self.ignore_borders = QCheckBox(text="Ignore cells on border")
        self.ignore_borders.setChecked(False)
        track_layout.addWidget(self.ignore_borders)

        ## track length suspicions
        ilengthlay = QHBoxLayout()
        self.check_length = QCheckBox(text="Flag tracks smaller than")
        self.check_length.setChecked(True)
        ilengthlay.addWidget(self.check_length)
        self.min_length = QLineEdit()
        self.min_length.setText("1")
        ilengthlay.addWidget(self.min_length)
        track_layout.addLayout(ilengthlay)
        
        ## Variability in feature suspicion
        self.check_size, self.size_variability = self.add_feature_gui( track_layout, "Size variation" )
        self.check_shape, self.shape_variability = self.add_feature_gui( track_layout, "Shape variation" )
        self.shape_variability.setText("2.0")

        ## merge/split combinaisons 
        track_btn = QPushButton("Inspect track", parent=self)
        track_btn.clicked.connect(self.inspect_tracks)
        track_layout.addWidget(track_btn)
        
        ## tmp test
        test_btn = QPushButton("Test", parent=self)
        test_btn.clicked.connect(self.track_features)
        track_layout.addWidget(test_btn)
        
        ## all features
        self.suspectTrack.setLayout(track_layout)

    def add_feature_gui( self, layout, feature_name ):
        """ Interface for a track feature check option """
        featlay = QHBoxLayout()
        check_item = QCheckBox(text=feature_name)
        check_item.setChecked(False)
        featlay.addWidget( check_item )
        var_item = QLineEdit()
        var_item.setText("1")
        featlay.addWidget( var_item )
        layout.addLayout( featlay )
        return check_item, var_item
        

    def reset_tracking_suspect(self):
        """ Remove suspects from tracking """
        self.reset_suspicion("tracking-1-2-*", None)
        self.reset_suspicion("tracking-2->1", None)
        self.reset_suspicion("division", None)
        self.reset_suspicion("track_length", None)
        self.reset_suspicion("track_size", None)
        self.reset_suspicion("track_shape", None)
        self.reset_suspect_range()

    def track_length(self):
        """ Find all cells that are only in one frame """
        max_len = int(self.min_length.text())
        labels, lengths, positions = self.epicure.tracking.get_small_tracks( max_len )
        for label, nframe, pos in zip(labels, lengths, positions):
            if self.epicure.verbose > 1:
                print("Suspect track length "+str(nframe)+": "+str(label)+" frame "+str(pos[0]) )
            self.add_suspect(pos, label, "track-length")

    def inspect_tracks(self):
        """ Look for suspicious tracks """
        self.viewer.window._status_bar._toggle_activity_dock(True)
        progress_bar = progress(total=6)
        progress_bar.update(0)
        self.reset_tracking_suspect()
        progress_bar.update(1)
        if self.ignore_borders.isChecked():
            progress_bar.set_description("Identifying border cells")
            self.get_border_cells()
        progress_bar.update(2)
        if self.check_length.isChecked():
            progress_bar.set_description("Identifying too small tracks")
            self.track_length()
        progress_bar.update(3)
        progress_bar.set_description("Inspect tracks 2->1")
        self.track_21()
        progress_bar.update(4)
        if (self.check_size.isChecked()) or self.check_shape.isChecked():
            progress_bar.set_description("Inspect track features")
            self.track_features()
        progress_bar.update(5)
        progress_bar.close()
        self.viewer.window._status_bar._toggle_activity_dock(False)

    def track_21(self):
        """ Look for suspect track: 2->1 """
        if self.epicure.tracking.tracklayer is None:
            ut.show_error("No tracking done yet!")
            return

        graph = self.epicure.tracking.graph
        divisions = dict()
        undiv = []
        if graph is not None:
            for child, parent in graph.items():
                ## 2->1, merge, suspect
                if len(parent) == 2:
                    onetwoone = False
                    ## was it only one before ?
                    if (parent[0] in graph.keys()) and (parent[1] in graph.keys()):
                        if graph[parent[0]][0] == graph[parent[1]][0]:
                            pos = self.epicure.tracking.get_mean_position([parent[0], parent[1]])
                            if pos is not None:
                                if self.epicure.verbose > 1:
                                    print("Suspect 1->2->1 track: "+str(graph[parent[0]][0])+"-"+str(parent)+"-"+str(child)+" frame "+str(pos[0]) )
                                self.add_suspect(pos, parent[0], "tracking-1-2-*")
                                undiv.append(graph[parent[0]][0])
                                onetwoone = True
                
                    if not onetwoone:
                        pos = self.epicure.tracking.get_mean_position(child, only_first=True)     
                        if pos is not None:
                            if self.epicure.verbose > 1:
                                print("Suspect 2->1 track: "+str(parent)+"-"+str(child)+" frame "+str(int(pos[0])) )
                            self.add_suspect(pos, parent[0], "tracking-2->1")
                        else:
                            if self.epicure.verbose > 1:
                                print("Something weird, "+str(child)+" mean position")
                ## 1->2, potential division
                else:
                    if self.get_div.isChecked():
                        if parent[0] not in divisions:
                            divisions[parent[0]] = [child]
                        else:
                            divisions[parent[0]].append(child)

        if self.get_div.isChecked():
            self.potential_divisions(divisions, undiv)
        self.epicure.finish_update()

    def get_border_cells(self):
        """ Return list of cells that are at the border (touching background) """
        self.border_cells = dict()
        for tframe in range(self.epicure.nframes):
            img = self.epicure.seg[tframe]
            self.border_cells[tframe] = self.get_border_cells_frame(img)        
        
    def get_border_cells_frame(self, imframe):
        """ Return cells on border in current image """ 
        touchlab = expand_labels(imframe, distance=3)  ## be sure that labels touch
        graph = RAG( touchlab, connectivity=2)
        adj_bg = []
        if 0 in graph.nodes:
            adj_bg = list(graph.adj[0])
        return adj_bg
            
    def potential_divisions(self, divisions, undivisions):
        """ Look at splitting events """
        for parent, childs in divisions.items():
            if parent not in undivisions:
                indexes = self.epicure.tracking.get_track_indexes(childs)
                if len(indexes) <= 0:
                    ## something wrong in the graph or in the tracks, ignore for now
                    continue
                ## One of the child exist only in one frame, suspicious
                if len(indexes) <= 3:
                    pos = self.epicure.tracking.mean_position(indexes, only_first=True)     
                    if self.epicure.verbose > 1:
                        print("Suspect 1-2-0 track: "+str(parent)+"-"+str(childs)+" frame "+str(pos[0]) )
                    self.add_suspect(pos, parent, "tracking-1-2-*")
                else:
                    ## get the average first position of the childs just after division
                    pos = self.epicure.tracking.mean_position(indexes, only_first=True)     
                    self.add_suspect(pos, parent, "division", symb="o", color="#0055ffff")

    def track_features(self):
        """ Look at outliers in track features """
        track_ids = self.epicure.tracking.get_track_list()
        features = []
        featType = {}
        if self.check_size.isChecked():
            features = features + ["Area", "Perimeter"]
            featType["Area"] = "size"
            featType["Perimeter"] = "size"
            size_factor = float(self.size_variability.text())
        if self.check_shape.isChecked():
            features = features + ["Eccentricity", "Solidity"]
            featType["Eccentricity"] = "shape"
            featType["Solidity"] = "shape"
            shape_factor = float(self.shape_variability.text())
        for tid in track_ids:
            track_indexes = self.epicure.tracking.get_track_indexes( tid )
            ## track should be long enough to make sense to look for outlier
            if len(track_indexes) > 3:
                track_feats = self.epicure.tracking.measure_features( tid, features )
                for feature, values in track_feats.items():
                    if featType[feature] == "size":
                        factor = size_factor
                    if featType[feature] == "shape":
                        factor = shape_factor
                    outliers = self.find_jump( values, factor=factor )
                    for out in outliers:
                        tdata = self.epicure.tracking.get_frame_data( tid, out )
                        if self.epicure.verbose > 1:
                            print("Suspect track "+feature+": "+str(tdata[0])+" "+" frame "+str(tdata[1]) )
                        self.add_suspect(tdata[1:4], tid, "track_"+featType[feature])

        
    def find_jump( self, tab, factor=1 ):
        """ Detect brutal jump in the values """
        jumps = []
        tab = np.array(tab)
        diff = tab[:(len(tab)-2)] - 2*tab[1:(len(tab)-1)] + tab[2:]
        diff = [(tab[1]-tab[0])] + diff.tolist() + [tab[len(tab)-1]-tab[len(tab)-2]] 
        avg = (tab[:(len(tab)-2)] + tab[2:])/2
        avg = [(tab[1]+tab[0])/2] + avg.tolist() + [(tab[len(tab)-1]+tab[len(tab)-2])/2]
        eps = 0.000000001
        diff = np.array(diff, dtype=np.float32)
        avg = np.array(avg, dtype=np.float32)
        diff = abs(diff+eps)/(avg+eps)
        ## keep only local max above threshold
        for i, diffy in enumerate(diff):
            if (i>0) and (i<len(diff)-1):
                if diffy > factor:
                    if (diffy > diff[i-1]) and (diffy > diff[i+1]):
                        jumps.append(i)
            else:
                if diffy > factor:
                    jumps.append(i)
        #jumps = (np.where( diff > factor )[0]).tolist()
        return jumps

    def find_outliers_tuk( self, tab, factor=3, below=True, above=True ):
        """ Returns index of outliers from Tukey's like test """
        q1 = np.quantile(tab, 0.2)
        q3 = np.quantile(tab, 0.8)
        qtuk = factor * (q3-q1)
        outliers = []
        if below:
            outliers = outliers + (np.where((tab-q1+qtuk)<0)[0]).tolist()
        if above:
            outliers = outliers + (np.where((tab-q3-qtuk)>0)[0]).tolist()
        return outliers

    def weirdo_area(self):
        """ look at area trajectory for outliers """
        track_df = self.epicure.tracking.track_df
        for tid in np.unique(track_df["track_id"]):
            rows = track_df[track_df["track_id"]==tid].copy()
            if len(rows) >= 3:
                rows["smooth"] = rows.area.rolling(self.win_size, min_periods=1).mean()
                rows["diff"] = (rows["area"] - rows["smooth"]).abs()
                rows["diff"] = rows["diff"].div(rows["smooth"])
                if self.epicure.verbose > 2:
                    print(rows)


