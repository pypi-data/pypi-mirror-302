import numpy as np
from skimage.segmentation import watershed, expand_labels, clear_border, find_boundaries, random_walker
from skimage.measure import regionprops, label, points_in_poly
from skimage.morphology import binary_closing, binary_dilation, binary_erosion, disk
from qtpy.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QCheckBox, QSlider, QLabel, QDoubleSpinBox, QComboBox, QLineEdit
from qtpy.QtCore import Qt
from napari.layers.labels._labels_utils import interpolate_coordinates
from scipy.ndimage import binary_fill_holes, distance_transform_edt, generate_binary_structure
from scipy.ndimage import label as ndlabel 
from multiprocessing.pool import ThreadPool as Pool
from napari.layers.labels._labels_utils import sphere_indices
import epicure.Utils as ut
import time
from napari.utils import progress
import edt

class Editing(QWidget):
    """ Handle user interaction to edit the segmentation """

    def __init__(self, napari_viewer, epic):
        super().__init__()
        self.viewer = napari_viewer
        self.epicure = epic
        self.old_mouse_drag = None
        self.tracklayer_name = "Tracks"
        self.shapelayer_name = "ROIs"
        self.grouplayer_name = "Groups"
        self.updated_labels = None   ## keep which labels are being edited

        layout = QVBoxLayout()
        
        ## Option to remove all border cells
        clean_line = QHBoxLayout()
        clean_vis = QCheckBox(text="Cleaning options")
        clean_line.addWidget(clean_vis)
        clean_helpbtn = QPushButton("Help", parent=self)
        clean_helpbtn.clicked.connect(self.help_clean)
        clean_line.addWidget(clean_helpbtn)
        layout.addLayout(clean_line)
        clean_vis.stateChanged.connect(self.show_cleaningBlock)
        self.create_cleaningBlock()
        layout.addWidget(self.gCleaned)
        clean_vis.setChecked(False)
        self.gCleaned.hide()

        ## handle grouping cells into categories
        group_line = QHBoxLayout()
        group_vis = QCheckBox(text="Group cells options")
        group_line.addWidget(group_vis)
        group_helpbtn = QPushButton("Help", parent=self)
        group_helpbtn.clicked.connect(self.help_group)
        group_line.addWidget(group_helpbtn)
        layout.addLayout(group_line)
        group_vis.stateChanged.connect(self.show_groupCellsBlock)
        self.create_groupCellsBlock()
        layout.addWidget(self.gGroup)
        group_vis.setChecked(False)
        self.gGroup.hide()
        
        ## Selection option: crop, remove cells
        select_line = QHBoxLayout()
        self.select_vis = QCheckBox(text="ROI options")
        select_line.addWidget(self.select_vis)
        help_selectbtn = QPushButton("Help", parent=self)
        help_selectbtn.clicked.connect(self.help_selection)
        select_line.addWidget(help_selectbtn)
        layout.addLayout(select_line)
        self.select_vis.stateChanged.connect(self.show_selectBlock)
        self.create_selectBlock()
        layout.addWidget(self.gSelect)
        self.select_vis.setChecked(False)
        self.gSelect.hide()
        
        ## Put seeds and do watershed from it
        seed_line = QHBoxLayout()
        self.seed_vis = QCheckBox(text="Seeds options")
        seed_line.addWidget(self.seed_vis)
        help_seedbtn = QPushButton("Help", parent=self)
        help_seedbtn.clicked.connect(self.help_seeds)
        seed_line.addWidget(help_seedbtn)
        layout.addLayout(seed_line)
        self.seed_vis.stateChanged.connect(self.show_hide_seedMapBlock)
        self.create_seedsBlock()
        layout.addWidget(self.gSeed)
        self.seed_vis.setChecked(False)
        self.gSeed.hide()
        
        self.setLayout(layout)
        
        ## interface done, ready to work 
        self.create_shapelayer()
        self.modify_cells()
        self.key_tracking_binding()
        self.add_overlay_message()

        ## catch filling/painting operations
        self.napari_fill = self.epicure.seglayer.fill
        self.epicure.seglayer.fill = self.epicure_fill
        self.napari_paint = self.epicure.seglayer.paint
        self.epicure.seglayer.paint = self.epicure_paint
        ### scale and radius for paiting
        self.paint_scale = np.array([self.epicure.seglayer.scale[i+1] for i in range(2)], dtype=float)
        self.epicure.seglayer.events.brush_size.connect( self.paint_radius )
        self.paint_radius()
        self.disk_one = disk(radius=1)
   
    def paint_radius( self ):
        """ Update painitng radius with brush size """
        self.radius = np.floor(self.epicure.seglayer.brush_size / 2) + 0.5
        self.brush_indices = sphere_indices(self.radius, tuple(self.paint_scale)) 

    def setParent(self, epy):
        self.epicure = epy

    def get_filename(self, endname):
        return ut.get_filename(self.epicure.outdir, self.epicure.imgname+endname )
        
    def get_values(self, coord):
        """ Get the label value under coord, the current frame, prepare the coords """
        int_coord = tuple(np.round(coord).astype(int))
        tframe = int(coord[0])
        segdata = self.epicure.seglayer.data[tframe]
        int_coord = int_coord[1:3]
        # get value of the label that will be painted over
        prev_label = int(segdata[int_coord])
        return int_coord, tframe, segdata, prev_label

    ### Get fill or paint action and assure compatibility with structure
    def epicure_fill(self, coord, new_label, refresh=True):
        """ Check if the filled cell is already registered """
        if new_label == 0:
            if self.epicure.verbose > 0:
                ut.show_warning("Fill with 0 (background) not allowed \n Use Eraser tool (press <1>) to erase")
                return
        int_coord, tframe, segdata, prev_label = self.get_values( coord )

        hascell = self.epicure.has_label( new_label )
        if hascell:
            ## already present, check that it is at the same place
            ## label before
            mask_before = segdata==new_label
            if np.sum(mask_before) <= 0:
                ut.show_warning("Label "+str(new_label)+" is already used in other frames. Choose another label")
                return
        
        ## if try to fill an empty zone, ensure that it doesn't fill the skeletons
        if prev_label == 0:
            skel = self.epicure.frame_to_skeleton( segdata )
            skel_fill = max(np.max(segdata)+2, new_label+1)
            segdata[skel] = skel_fill
            skel = None
            
        if hascell:
            # if contiguous replace only selected connected component, calculate how it would be changed
            matches = (segdata == prev_label)
            labeled_matches, num_features = label(matches, return_num=True)
            if num_features != 1:
                match_label = labeled_matches[int_coord]
                matches = np.logical_and( matches, labeled_matches == match_label )
           
            # check if touch the already present cell
            ok = self.touching_masks(mask_before, matches)
            if not ok:
                ut.show_warning("Label "+str(new_label)+" added do not touch already present cell. Choose another label or draw contiguously")
                ## reset if necessary
                if prev_label == 0:
                    segdata[segdata==skel_fill] = 0  ## put skeleton back to 0
                return
            ut.setNewLabel( self.epicure.seglayer, (np.argwhere(matches)).tolist(), new_label, add_frame=tframe )
            if prev_label == 0:
                segdata[skel] = 0  ## put skeleton back to 0
        else:
            ## new cell, add it to the tracks list
            self.napari_fill(coord, new_label, refresh=True)
            if prev_label == 0:
                segdata[segdata==skel_fill] = 0  ## put skeleton back to 0
                self.remove_boundaries(segdata)
            self.epicure.add_label(new_label, tframe)
        
        ## Finish filling step to ensure everything's fine
        self.epicure.seglayer.refresh()
        ## put the active mode of the layer back to the zoom one
        self.epicure.seglayer.mode = "pan_zoom"
        if prev_label != 0: 
            self.epicure.tracking.remove_one_frame( [prev_label], tframe )

    def epicure_paint(self, coord, new_label, refresh=True):
        """ Action when trying to edit a label with paint tool """
        tframe, int_coord = ut.convert_coords( coord )
        mask_indices = np.array( int_coord ) + self.brush_indices
        bbox = ut.getBBoxFromPts( mask_indices, extend=0, imshape=self.epicure.imgshape2D )
        bbox = ut.extendBBox2D( bbox, extend_factor=4, imshape=self.epicure.imgshape2D )
        cropdata = ut.cropBBox2D( self.epicure.seglayer.data[tframe], bbox )
        crop_indices = ut.positions2DIn2DBBox( mask_indices, bbox )
        prev_labels = np.unique( cropdata[ tuple(np.array(crop_indices).T) ] ).tolist()
        if 0 in prev_labels:
            prev_labels.remove(0)

        if new_label > 0:
            ## painting a new or extending a cell
            hascell = self.epicure.has_label( new_label )
            if hascell:
                ## check that label is in current frame
                mask_before = cropdata==new_label
                if not np.isin(1, mask_before):
                    ut.show_warning("Label "+str(new_label)+" is already used in other frames. Choose another label")
                    return

                ## already present, check that it is at the same place
                #### Test if painting touch previous label
                mask_after = np.zeros(cropdata.shape)
                mask_after[ tuple(np.array(crop_indices).T) ] = 1
                ok = self.touching_masks(mask_before, mask_after)
                if not ok:
                    ut.show_warning("Label "+str(new_label)+" added do not touch already present cell. Choose another label or draw contiguously")
                    return
            else:
                ## drawing new cell, fill it at the end
                if self.epicure.verbose > 1:
                    print("Painting a new cell")

        ## Paint and update everything    
        painted = np.copy(cropdata)
        painted[ tuple(np.array(crop_indices).T) ] = new_label
        if new_label > 0:
            painted = binary_fill_holes( painted==new_label )
            crop_indices = np.argwhere(painted>0)    
        mask_indices = ut.toFullMoviePos( crop_indices, bbox, tframe )
        new_labels = np.repeat(new_label, len(mask_indices)).tolist()

        ## Update label boundaries if necessary
        cind_bound = self.ind_boundaries( painted )
        ind_bound = [ ind for ind in cind_bound if cropdata[tuple(ind)] in prev_labels ]
        if (new_label>0) and (len( ind_bound ) > 0):
            bound_ind = ut.toFullMoviePos( ind_bound, bbox, tframe )
            bound_labels = np.repeat(0, len(bound_ind)).tolist()
            mask_indices = np.vstack( (mask_indices, bound_ind) )
            new_labels = new_labels + bound_labels

        ## Go, apply the change, and update the tracks
        self.epicure.change_labels( mask_indices, new_labels )
        
    def touching_masks(self, maska, maskb):
        """ Check if the two mask touch """
        maska = binary_dilation(maska, footprint=self.disk_one)
        return np.sum(np.logical_and(maska, maskb))>0
    
    def touching_indices(self, maska, indices):
        """ Check if the indices touch the mask """
        maska = binary_dilation(maska, footprint=self.disk_one)
        return np.isin(1, maska[indices]) > 0


    ## Merging/splitting cells functions
    def modify_cells(self):
        self.epicure.overtext["labels"] = "---- Labels editing ---- \n"
        self.epicure.overtext["labels"] += "  <n> to set the current label to unused value and go to paint mode \n"
        self.epicure.overtext["labels"] += "  <Shift+n> to set the current label to unused value and go to fill mode \n"
        self.epicure.overtext["labels"] += "  Right-click, erase the cell \n"
        self.epicure.overtext["labels"] += "  <Control>+Left click, from one cell to another to merge them \n"
        self.epicure.overtext["labels"] += "  <Control>+Right click, accross a junction to split in 2 cells \n"
        self.epicure.overtext["labels"] += "  <Alt>+Right click drag, draw a junction to split in 2 cells \n"
        self.epicure.overtext["labels"] += "  <Alt>+Left click drag, draw a junction to correct it \n"
        #self.epicure.overtext["mergesplit"] += "<Alt>+Left click on a suggestion to accept it \n"
        self.epicure.overtext["labels"] += "  <w> then <Control>+Left click on one cell to another to swap their values \n"
        
        self.epicure.overtext["grouped"] = "---- Group cells ---- \n"
        self.epicure.overtext["grouped"] += "  Shift+left click to add a cell to the current group \n"
        self.epicure.overtext["grouped"] = self.epicure.overtext["grouped"] + "  Shift+right click to remove the cell from its group \n"
        #self.epicure.overtext["checked"] = self.epicure.overtext["checkmap"] + "<c> to show/hide checkmap \n"
        
        self.epicure.overtext["seed"] = "---- Seed options --- \n"
        self.epicure.overtext["seed"] += "  <e> then left-click to place a seed \n"
        #self.epicure.overtext["seed"] = self.epicure.overtext["seed"] +  "\n"
        
        @self.epicure.seglayer.mouse_drag_callbacks.append
        def set_checked(layer, event):
            if event.type == "mouse_press":
                if (len(event.modifiers)==1) and ('Shift' in event.modifiers):
                    if event.button == 1:
                        if self.epicure.verbose > 0:
                            print("Mark cell in group "+self.group_group.text())
                        self.add_cell_to_group(event)

                    if event.button == 2:
                        if self.epicure.verbose > 0:
                            print("Remove cell from its group")
                        self.remove_cell_group(event)

        @self.epicure.seglayer.bind_key("Control-z", overwrite=False)
        def undo_operations(seglayer):
            if self.epicure.verbose > 0:
                print("Undo previous action")
            img_before = np.copy(self.epicure.seg)
            self.epicure.seglayer.undo()
            self.epicure.update_changed_labels_img( img_before, self.epicure.seglayer.data )

        @self.epicure.seglayer.bind_key('n', overwrite=True)
        def set_nextlabel(layer):
            lab = self.epicure.get_free_label()
            ut.show_info( "Unused label "+": "+str(lab) )
            ut.set_label(layer, lab)
        
        @self.epicure.seglayer.bind_key('Shift-n', overwrite=True)
        def set_nextlabel_paint(layer):
            lab = self.epicure.get_free_label()
            ut.show_info( "Unused label "+": "+str(lab) )
            ut.set_label(layer, lab)
            layer.mode = "FILL"
    
        @self.epicure.seglayer.bind_key('w', overwrite=True)
        def key_swap(layer):
            """ Active key bindings for label swapping options """
            ut.show_info("Begin swap mode: Control and click to swap two labels")
            self.old_mouse_drag, self.old_key_map = ut.clear_bindings( self.epicure.seglayer )

            @self.epicure.seglayer.mouse_drag_callbacks.append
            def click(layer, event):
                """ Swap the labels from first to last position of the pressed mouse """
                if event.type == "mouse_press":
                    if len(event.modifiers) > 0:
                        start_label = self.epicure.seglayer.get_value(position=event.position, view_direction = event.view_direction, dims_displayed=event.dims_displayed, world=True)
                        start_pos = event.position
                        yield
                        while event.type == 'mouse_move':
                            yield
                        end_label = self.epicure.seglayer.get_value(position=event.position, view_direction = event.view_direction, dims_displayed=event.dims_displayed, world=True)
                        end_pos = event.position
                        tframe = int(event.position[0])
                    
                        if start_label == 0 or end_label == 0:
                            if self.epicure.verbose > 0:
                                print("One position is not a cell, do nothing")
                            return

                        if (event.button == 1) and ("Control" in event.modifiers):
                            # Left-click: swap labels at each end of the click
                            if self.epicure.verbose > 0:
                                print("Swap cell "+str(start_label)+" and "+str(end_label))
                            self.swap_labels(tframe, start_label, end_label)
                    
                ut.reactive_bindings( self.epicure.seglayer, self.old_mouse_drag, self.old_key_map )
                ut.show_info("End swap")

        @self.epicure.seglayer.bind_key('e', overwrite=True)
        def place_seed(layer):
            """ Add a seed if left click after pressing <e> """
            
            ## desactivate other click-binding
            self.old_mouse_drag = self.epicure.seglayer.mouse_drag_callbacks.copy()
            self.epicure.seglayer.mouse_drag_callbacks = []
            ut.show_info("Left-click to place a new seed")

            @self.epicure.seglayer.mouse_drag_callbacks.append
            def click(layer, event):
                if (event.type == "mouse_press") and (len(event.modifiers)==0) and (event.button==1):
                    ## single left-click place a seed
                    if "Seeds" not in self.viewer.layers:
                        self.reset_seeds()
                    self.place_seed(event.position)
                    self.show_seedMapBlock()
                else:
                    self.end_place_seed()


        @self.epicure.seglayer.mouse_drag_callbacks.append
        def click(layer, event):
            if event.type == "mouse_press":
                if len(event.modifiers) == 0:
                    if event.button == 2:
                        # single right-click: erase the cell
                        tframe = ut.current_frame(self.viewer)

                        ## erase the cell and get its value
                        erased = ut.setLabelValue(self.epicure.seglayer, self.epicure.seglayer, event, 0, tframe, tframe)
                        if erased is not None:
                            self.epicure.delete_track(erased, tframe)
                        
                if (len(event.modifiers)==1) and ('Control' in event.modifiers):
                    # on move
                    start_label = self.epicure.seglayer.get_value(position=event.position, view_direction = event.view_direction, dims_displayed=event.dims_displayed, world=True)
                    start_pos = event.position
                    yield
                    while event.type == 'mouse_move':
                        yield
                    end_label = self.epicure.seglayer.get_value(position=event.position, view_direction = event.view_direction, dims_displayed=event.dims_displayed, world=True)
                    end_pos = event.position
                    tframe = int(event.position[0])
                    
                    if start_label == 0 or end_label == 0:
                        if self.epicure.verbose > 0:
                            print("One position is not a cell, do nothing")
                        return

                    if event.button == 1:
                        # Control left-click: merge labels at each end of the click
                        if start_label != end_label:
                            if self.epicure.verbose > 0:
                                print("Merge cell "+str(start_label)+" with "+str(end_label))
                            self.merge_labels(tframe, start_label, end_label)
                    
                    if event.button == 2:
                        # Control right-click: split label at each end of the click
                        if start_label == end_label:
                            if self.epicure.verbose > 0:
                                print("Split cell "+str(start_label))
                            self.split_label(tframe, start_label, start_pos, end_pos)
                        else:
                            if self.epicure.verbose > 0:
                                print("Not the same cell already, do nothing")
                
                if (len(event.modifiers)==1) and ('Alt' in event.modifiers):
                    if self.shapelayer_name not in self.viewer.layers:
                        self.create_shapelayer()
                    shape_lay = self.viewer.layers[self.shapelayer_name]
                    shape_lay.mode = "add_path"
                    shape_lay.visible = True
                    pos = [event.position]
                    yield
                    ## record all the successives position of the mouse while clicked
                    while event.type == 'mouse_move':
                        pos.append(event.position)
                        shape_lay.data = np.array(pos)
                        shape_lay.shape_type = "path"
                        shape_lay.refresh()
                        yield
                    pos.append(event.position)
                    shape_lay.data = np.array(pos)
                    shape_lay.shape_type = "path"
                    shape_lay.refresh()
                    ut.set_active_layer(self.viewer, "Segmentation")
                    tframe = int(event.position[0])
                    if event.button == 1:
                        # ALT leftt-click: modify junction along the drawn line
                        if self.epicure.verbose > 0:
                            print("Correct junction with the drawn line ")
                        self.redraw_along_line(tframe, pos)
                        shape_lay.data = []
                        shape_lay.refresh()
                        shape_lay.visible = False
                    if event.button == 2:
                        # ALT right-click: split labels along the drawn line
                        if self.epicure.verbose > 0:
                            print("Split cell along the drawn line ")
                        self.split_along_line(tframe, pos)
                        shape_lay.data = []
                        shape_lay.refresh()
                        shape_lay.visible = False

    def split_label(self, tframe, startlab, start_pos, end_pos):
        """ Split the label in two cells based on the two seeds """
        segt = self.epicure.seglayer.data[tframe]
        labelBB = ut.getBBox2D(segt, startlab)
        labelBB = ut.extendBBox2D( labelBB, extend_factor=1.25, imshape=self.epicure.imgshape2D )

        mov = self.viewer.layers["Movie"].data[tframe]
        imgBB = ut.cropBBox2D(mov, labelBB)
        segBB = ut.cropBBox2D(segt, labelBB)
        maskBB = np.zeros(segBB.shape, dtype="uint8")
        maskBB[segBB==startlab] = 1
        spos = ut.positionIn2DBBox( start_pos, labelBB )
        epos = ut.positionIn2DBBox( end_pos, labelBB )

        markers = np.zeros(maskBB.shape, dtype=self.epicure.dtype)
        markers[spos] = startlab
        markers[epos] = self.epicure.get_free_label()
        splitted = watershed( imgBB, markers=markers, mask=maskBB )
        if (np.sum(splitted==startlab) < self.epicure.minsize) or (np.sum(splitted==markers[epos]) < self.epicure.minsize):
            if self.epicure.verbose > 0:
                print("Sorry, split failed, one cell smaller than "+str(self.epicure.minsize)+" pixels")
        else:
            if len(np.unique(splitted)) > 2:
                curframe = np.zeros(segBB.shape, dtype="uint8")
                labels = []
                for i, splitlab in enumerate(np.unique(splitted)):
                    if splitlab > 0:
                        curframe[splitted==splitlab] = i+1
                        labels.append(i+1)

                curframe = self.remove_boundaries(curframe)
                ## apply the split and propagate the label to descendant label
                self.propagate_label_change( curframe, labels, labelBB, tframe, [startlab] )
            else:
                if self.epicure.verbose > 0:
                    print("Split failed, no boundary in pixel intensities found")

    def remove_boundaries(self, img):
        """ Put the boundaries pixels between two labels as 0 """
        bound = self.epicure.frame_to_skeleton( img, connectivity=1 )
        img[bound>0] = 0
        return img
    
    def ind_boundaries(self, img):
        """ Get indices of the boundaries pixels between two labels """
        bound = self.epicure.frame_to_skeleton( img, connectivity=1 )
        return np.argwhere(bound>0)

    def redraw_along_line(self, tframe, positions):
        """ Redraw the two labels separated by a line drawn manually """
        bbox = ut.getBBox2DFromPts( positions, extend=0, imshape=self.epicure.imgshape2D )
        #bbox = ut.extendBBox2D( bbox, extend_factor=1.25, imshape=self.epicure.imgshape2D )

        segt = self.epicure.seglayer.data[tframe]
        cropt = ut.cropBBox2D( segt, bbox )
        crop_positions = ut.positionsIn2DBBox( positions, bbox )

        # get the value of the cells to update (most frequent label along the line)
        curlabels = []
        prev_pos = None
        # Find closest zero elements in the inverted image (same as closest non-zero for image)
        
        crop_zeros = distance_transform_edt(cropt, return_distances=False, return_indices=True)

        for pos in crop_positions:
            if (prev_pos is None) or ((round(pos[0]) != round(prev_pos[0])) and (round(pos[1]) != round(prev_pos[1]) )):
                ## find closest pixel that is 0 (on a junction)
                juncpoint = crop_zeros[:, round(pos[0]), round(pos[1])]
                labs = np.unique( cropt[ (juncpoint[0]-2):(juncpoint[0]+2), (juncpoint[1]-2):(juncpoint[1]+2) ] )
                for clab in labs:
                    if clab > 0:
                        curlabels.append(clab)
                prev_pos = pos
                
        sort_curlabel = sorted(set(curlabels), key=curlabels.count)
        ## external junction: only one cell
        if len(sort_curlabel) < 2:
            if self.epicure.verbose > 0:
                print("Only one cell along the junction: can't do it")
                return
        flabel = sort_curlabel[-1]
        slabel = sort_curlabel[-2]
        if self.epicure.verbose > 0:
            print("Cells to update: "+str(flabel)+" "+str(slabel))
        
        ## crop around selected label
        bbox, _ = ut.getBBox2DMerge( segt, flabel, slabel )
        bbox = ut.extendBBox2D( bbox, extend_factor=1.25, imshape=self.epicure.imgshape2D )
        init_cropt = ut.cropBBox2D( segt, bbox )
        curlabel = flabel
        ## merge the two labels together
        binlab = np.isin( init_cropt, [flabel, slabel] )*1
        footprint = disk(radius=2)
        cropt = flabel*binary_closing(binlab, footprint)
        crop_positions = ut.positionsIn2DBBox( positions, bbox )

        # draw the line only in the cell to split
        line = np.zeros(cropt.shape, dtype="uint8")
        for i, pos in enumerate(crop_positions):
            if cropt[round(pos[0]), round(pos[1])] == curlabel:
                line[round(pos[0]), round(pos[1])] = 1
            if (i > 0):
                prev = (crop_positions[i-1][0], crop_positions[i-1][1])
                cur = (pos[0], pos[1])
                interp_coords = interpolate_coordinates(prev, cur, 1)
                for ic in interp_coords:
                    line[tuple(np.round(ic).astype(int))] = 1
        self.move_in_crop( curlabel, init_cropt, cropt, crop_positions, line, bbox, tframe, retry=0)
    
    def move_in_crop(self, curlabel, init_cropt, cropt, crop_positions, line, bbox, frame, retry):
        """ Move the junction in the cropped region """
        dis = retry
        footprint = disk(radius=dis)
        dilline = binary_dilation(line, footprint=footprint)

        # get the two splitted regions and relabel one of them
        clab = np.zeros(cropt.shape, dtype="uint8")
        clab[cropt==curlabel] = 1
        clab[dilline] = 0
        labels = label(clab, background=0, connectivity=1)
        if (np.max(labels) == 2) & (np.sum(labels==1)>self.epicure.minsize) & (np.sum(labels==2)>self.epicure.minsize):
            ## get new image with the 2 cells to retrack
            labels = expand_labels(labels, distance=dis+1)
            indmodif = []
            newlabels = []
            for i in range(2):
                imodif = ( (labels==(i+1)) & (cropt==curlabel) )
                val, counts = np.unique( init_cropt[ imodif ], return_counts=True) 
                init_label = val[np.argmax(counts)]
                imodif = np.argwhere(imodif).tolist()
                indmodif = indmodif + imodif
                newlabels = newlabels + np.repeat( init_label, len(imodif) ).tolist()
            
            indmodif = ut.toFullMoviePos( indmodif, bbox, frame )
            
            # remove the boundary between the two updated labels only
            cind_bound = self.ind_boundaries( labels )
            ind_bound = [ ind for ind in cind_bound if cropt[tuple(ind)]==curlabel ]
            ind_bound = ut.toFullMoviePos( ind_bound, bbox, frame )
            indmodif = np.vstack((indmodif, ind_bound))
            newlabels = newlabels + np.repeat(0, len(ind_bound)).tolist()
            
            self.epicure.change_labels( indmodif, newlabels )
            ## udpate the centroid of the modified labels
            #for clabel in np.unique(newlabels):
            #    if clabel > 0:
            #        self.epicure.update_centroid( clabel, frame )
        else:
            if (retry > 6) :
                if self.epicure.verbose > 0:
                    print("Update failed "+str(np.max(labels)))
                return
            retry = retry + 1
            self.move_in_crop(curlabel, init_cropt, cropt, crop_positions, line, bbox, frame, retry=retry)

    def split_along_line(self, tframe, positions):
        """ Split a label along a line drawn manually """

        bbox = ut.getBBox2DFromPts( positions, extend=0, imshape=self.epicure.imgshape2D )
        bbox = ut.extendBBox2D( bbox, extend_factor=1.25, imshape=self.epicure.imgshape2D )

        segt = self.epicure.seglayer.data[tframe]
        cropt = ut.cropBBox2D( segt, bbox )
        crop_positions = ut.positionsIn2DBBox( positions, bbox )

        # get the value of the cell to split (most frequent label along the line)
        curlabels = []
        prev_pos = None
        for pos in crop_positions:
            if (prev_pos is None) or ((round(pos[0]) != round(prev_pos[0])) and (round(pos[1]) != round(prev_pos[1]) )):
                clab = cropt[round(pos[0]), round(pos[1])]
                curlabels.append(clab)
                prev_pos = pos
                
        curlabel = max(set(curlabels), key=curlabels.count)
        if self.epicure.verbose > 0:
            print("Cell to split: "+str(curlabel))
        if curlabel == 0:
            if self.epicure.verbose > 0:
                print("Refusing to split background")
            return               
                        
        ## crop around selected label
        bbox = ut.getBBox2D(segt, curlabel)
        bbox = ut.extendBBox2D( bbox, extend_factor=1.5, imshape=self.epicure.imgshape2D )
        cropt = ut.cropBBox2D( segt, bbox )
        crop_positions = ut.positionsIn2DBBox( positions, bbox )

        # draw the line only in the cell to split
        line = np.zeros(cropt.shape, dtype="uint8")
        for i, pos in enumerate(crop_positions):
            if cropt[round(pos[0]), round(pos[1])] == curlabel:
                line[round(pos[0]), round(pos[1])] = 1
            if (i > 0):
                prev = (crop_positions[i-1][0], crop_positions[i-1][1])
                cur = (pos[0], pos[1])
                interp_coords = interpolate_coordinates(prev, cur, 1)
                for ic in interp_coords:
                    line[tuple(np.round(ic).astype(int))] = 1
        self.split_in_crop( curlabel, cropt, crop_positions, line, bbox, tframe, retry=0)

    def split_in_crop(self, curlabel, cropt, crop_positions, line, bbox, frame, retry):
        """ Find the split to do in the cropped region """
        dis = retry
        footprint = disk(radius=dis)
        dilline = binary_dilation(line, footprint=footprint)

        # get the two splitted regions and relabel one of them
        clab = np.zeros(cropt.shape, dtype="uint8")
        clab[cropt==curlabel] = 1
        clab[dilline] = 0
        labels = label(clab, background=0, connectivity=1)
        if (np.max(labels) == 2) & (np.sum(labels==1)>self.epicure.minsize) & (np.sum(labels==2)>self.epicure.minsize):
            ## get new image with the 2 cells to retrack
            labels = expand_labels(labels, distance=dis+1)
            curframe = np.zeros( cropt.shape, dtype="uint8" )
            for i in range(2):
                curframe[ (labels==(i+1)) & (cropt==curlabel) ] = i+1
            
            curframe = self.remove_boundaries(curframe)
            self.propagate_label_change( curframe, [1,2], bbox, frame, [curlabel] )

        else:
            if (retry > 6) :
                if self.epicure.verbose > 0:
                    print("Split failed "+str(np.max(labels)))
                return
            retry = retry + 1
            self.split_in_crop(curlabel, cropt, crop_positions, line, bbox, frame, retry=retry)

    def merge_labels(self, tframe, startlab, endlab, extend_factor=1.25):
        """ Merge the two given labels """
        start_time = time.time()
        segt = self.epicure.seglayer.data[tframe]
        
        ## Crop around labels to work on smaller field of view
        bbox, merged = ut.getBBox2DMerge( segt, startlab, endlab )
        
        ## keep only the region of interest
        bbox = ut.extendBBox2D( bbox, extend_factor, self.epicure.imgshape2D )
        segt_crop = ut.cropBBox2D( segt, bbox )

        if self.epicure.verbose > 1:
            ut.show_duration(start_time, "Merging: bbox cropped ")

        ## check that labels can be merged
        touch = ut.checkTouchingLabels( segt_crop, startlab, endlab )
        if not touch:
            ut.show_warning("Labels not touching, I refuse to merge them")
            return

        ## merge the two labels together
        joinlab = ut.cropBBox2D( merged, bbox )
        footprint = disk(radius=2)
        joinlab = endlab * binary_closing(joinlab, footprint)
        
        if self.epicure.verbose > 1:
            ut.show_duration(start_time, "Merged in ")

        ## update and propagate the change
        self.propagate_label_change(joinlab, [endlab], bbox, tframe, [startlab, endlab])
        if self.epicure.verbose > 1:
            ut.show_duration(start_time, "Merged and propagated in ")

    def touching_labels(self, img, lab, olab):
        """ Check if the two labels are neighbors or not """
        flab = find_boundaries(img==lab)
        folab = find_boundaries(img==olab)
        return np.sum(np.logical_and(flab, folab))>0
    
    def swap_labels(self, tframe, lab, olab):
        """ Swap two labels """
        segt = self.epicure.seglayer.data[tframe]
        ## Get the two labels position to swap
        modiflab = np.argwhere(segt==lab).tolist()
        modifolab = np.argwhere(segt==olab).tolist()
        newlabs = np.repeat(olab, len(modiflab)).tolist() + np.repeat(lab, len(modifolab)).tolist()
        ## Change the labels
        ut.setNewLabel( self.epicure.seglayer, modiflab+modifolab, newlabs, add_frame=tframe )
        ## Update the tracks and graph with swap
        self.epicure.swap_labels( lab, olab, tframe )
        self.epicure.seglayer.refresh()


    ######################
    ## Erase border cells
    def remove_border(self):
        """ Remove all cells that touch the border """
        start_time = time.time()
        self.viewer.window._status_bar._toggle_activity_dock(True)
        for i in progress(range(0, self.epicure.nframes)):
            self.remove_pixel_border( np.copy(self.epicure.seglayer.data[i]), i)
        self.viewer.window._status_bar._toggle_activity_dock(False)
        self.epicure.seglayer.refresh()
        if self.epicure.verbose > 0:
            ut.show_duration( start_time, "Border cells removed in ")

    def remove_smalls( self ):
        """ Remove all cells smaller than given area (in nb pixels) """
        start_time = time.time()
        self.viewer.window._status_bar._toggle_activity_dock(True)
        for i in progress(range(0, self.epicure.nframes)):
            self.remove_small_cells( np.copy(self.epicure.seglayer.data[i]), i)
        self.viewer.window._status_bar._toggle_activity_dock(False)
        if self.epicure.verbose > 0:
            ut.show_duration( start_time, "Small cells removed in ")

    def remove_small_cells(self, img, frame):
        """ Remove if few the cell is only few pixels """
        #init_labels = set(np.unique(img))
        minarea = int(self.small_size.text())
        props = regionprops( img )
        resimg = np.copy( img )
        for prop in props:
            if prop.area < minarea:
                (resimg[prop.bbox[0]:prop.bbox[2], prop.bbox[1]:prop.bbox[3]])[prop.image] = 0
        ## update the tracks after the potential disappearance of some cells
        self.epicure.seglayer.data[frame] = resimg
        self.epicure.removed_labels( img, resimg, frame )
    
    def merge_inside_cells( self ):
        """ Merge cell that falls inside another cell with ut """
        start_time = time.time()
        self.viewer.window._status_bar._toggle_activity_dock(True)
        for i in progress(range(0, self.epicure.nframes)):
            self.merge_inside_cell(self.epicure.seglayer.data[i], i)
        self.viewer.window._status_bar._toggle_activity_dock(False)
        if self.epicure.verbose > 0:
            ut.show_duration( start_time, "Inside cells merged in ")

    def merge_inside_cell( self, img, frame ):
        """ Merge cells that fits inside the convex hull of a cell with it """
        try:
            from skimage.graph import RAG
        except:
            from skimage.future.graph import RAG  ## older version of scikit-image
        touchlab = expand_labels(img, distance=3)  ## be sure that labels touch
        graph = RAG( touchlab, connectivity=2)
        adj_bg = []
        
        nodes = list(graph.nodes)
        for label in nodes:
            nneighbor = len(graph.adj[label])
            if nneighbor == 1:
                neigh_label = graph.adj[label]
                for lab in neigh_label.keys():
                    nlabel = int( lab )
                # both labels are still present in the current frame
                if nlabel>0 and sum( np.isin( [label, nlabel], self.epicure.seglayer.data[frame] ) ) == 2:
                    self.merge_labels( frame, label, nlabel, 1.05 )
                    if self.epicure.verbose > 0:
                        print( "Merged label "+str(label)+" into label "+str(nlabel)+" at frame "+str(frame) )
               
            

    def remove_pixel_border(self, img, frame):
        """ Remove if few pixels wide along border (cellpose) """
        size = int(self.border_size.text())
        if size == 0:
            resimg = clear_border(img)
        else:
            crop_img = img[size:(img.shape[0]-size-1), size:(img.shape[1]-size-1)]
            crop_img = clear_border( crop_img )
            resimg = np.zeros(img.shape)
            resimg[size:(resimg.shape[0]-size-1), size:(resimg.shape[1]-size-1)] = crop_img
        ## update the tracks after the potential disappearance of some cells
        self.epicure.seglayer.data[frame] = resimg
        self.epicure.removed_labels( img, resimg, frame )


    ###############
    ## Shapes functions
    def create_shapelayer(self):
        """ Create the layer that handle temporary drawings """
        shapes = []
        shap = self.viewer.add_shapes(shapes, name=self.shapelayer_name, blending="additive", opacity=1, edge_width=2)
        shap.visible = False

    ######################################"
    ## Seeds and watershed functions
    def show_hide_seedMapBlock(self):
        self.gSeed.setVisible(not self.gSeed.isVisible())
        if not self.gSeed.isVisible():
            ut.remove_layer(self.viewer, "Seeds")
    
    def show_seedMapBlock(self):
        """ Show the seeds """
        self.gSeed.setVisible(True)
        self.seed_vis.setChecked(True)

    def create_seedsBlock(self):
        self.gSeed = QGroupBox("Seeds")
        seed_layout = QVBoxLayout()
        seed_createbtn = QPushButton("Create seeds layer", parent=self)
        seed_createbtn.clicked.connect(self.reset_seeds)
        seed_layout.addWidget(seed_createbtn)
        seed_loadbtn = QPushButton("Load seeds from previous time point", parent=self)
        seed_loadbtn.clicked.connect(self.get_seeds_from_prev)
        seed_layout.addWidget(seed_loadbtn)
        
        ## choose method and segment from seeds
        gseg = QGroupBox("Seed based segmentation")
        gseg_layout = QVBoxLayout()
        seed_btn = QPushButton("Segment cells from seeds", parent=self)
        seed_btn.clicked.connect(self.segment_from_points)
        gseg_layout.addWidget(seed_btn)
        self.seed_method = QComboBox()
        self.seed_method.addItem("Intensity-based (watershed)")
        self.seed_method.addItem("Distance-based")
        self.seed_method.addItem("Diffusion-based")
        gseg_layout.addWidget(self.seed_method)
        maxdist = QHBoxLayout()
        maxdist_lab = QLabel()
        maxdist_lab.setText("Max cell radius")
        maxdist.addWidget(maxdist_lab)
        self.max_distance = QLineEdit()
        self.max_distance.setText("100.0")
        maxdist.addWidget(self.max_distance)
        gseg_layout.addLayout(maxdist)
        gseg.setLayout(gseg_layout)
        
        seed_layout.addWidget(gseg)
        self.gSeed.setLayout(seed_layout)

    def help_seeds(self):
        ut.show_documentation_page("Seeds")

    def create_seedlayer(self):
        pts = []
        points = self.viewer.add_points( np.array(pts), face_color="blue", size = 7,  edge_width=0, name="Seeds" )

    def reset_seeds(self):
        ut.remove_layer(self.viewer, "Seeds")
        self.create_seedlayer()

    def get_seeds_from_prev(self):
        #self.reset_seeds()
        if "Seeds" not in self.viewer.layers:
            self.create_seedlayer()
        tframe = int(self.viewer.cursor.position[0])
        segt = self.epicure.seglayer.data[tframe]
        if tframe > 0:
            pts = self.viewer.layers["Seeds"].data
            segp = self.epicure.seglayer.data[tframe-1]
            props = regionprops(segp)
            for prop in props:
                cent = prop.centroid
                ## create a seed in the centroid only in empty spaces
                if int(segt[int(cent[0]), int(cent[1])]) == 0:
                    pts = np.append(pts, [[cent[0], cent[1]]], axis=0)
            self.viewer.layers["Seeds"].data = pts
            self.viewer.layers["Seeds"].refresh()
        
    def end_place_seed(self):
        """ Finish placing seeds mode """
        if self.old_mouse_drag is not None:
            self.epicure.seglayer.mouse_drag_callbacks = self.old_mouse_drag
            ut.show_info("End seed")
        ut.set_active_layer( self.viewer, "Segmentation" )

    def place_seed(self, event_pos):
        """ Add a seed under the cursor """
        tframe = int(self.viewer.cursor.position[0])
        segt = self.epicure.seglayer.data[tframe]
        pts = self.viewer.layers["Seeds"].data
        cent = event_pos[1:]
        ## create a seed in the centroid only in empty spaces
        if int(segt[int(cent[0]), int(cent[1])]) == 0:
            pts = np.append(pts, [[cent[0], cent[1]]], axis=0)
            self.viewer.layers["Seeds"].data = pts
            self.viewer.layers["Seeds"].refresh()
        ut.set_active_layer( self.viewer, "Segmentation" )


    def segment_from_points(self):
        """ Do cells segmentation from seed points """
        if not "Seeds" in self.viewer.layers:
            ut.show_warning("No seeds placed")
            return
        if len(self.viewer.layers["Seeds"].data) <= 0:
            ut.show_warning("No seeds placed")
            return

        ## get crop of the image around seeds
        tframe = ut.current_frame(self.viewer)
        segBB, markers, maskBB, labelBB = self.crop_around_seeds( tframe )
        ## save current labels to compare afterwards
        before_seeding = np.copy(segBB)

        ## segment current seeds from points with selected method
        if self.seed_method.currentText() == "Intensity-based (watershed)":
            self.watershed_from_points( tframe, segBB, markers, maskBB, labelBB )
        if self.seed_method.currentText() == "Distance-based":
            self.distance_from_points( tframe, segBB, markers, maskBB, labelBB )
        if self.seed_method.currentText() == "Diffusion-based":
            self.diffusion_from_points( tframe, segBB, markers, maskBB, labelBB )

        ## finish segmentation: thin to have one pixel boundaries, update all
        skelBB = self.epicure.frame_to_skeleton( segBB, connectivity=1 )
        segBB[ skelBB>0 ] = 0
        self.reset_seeds()
        ## update the list of tracks with the potential new cells
        self.epicure.added_labels_oneframe( tframe, before_seeding, segBB )
        self.end_place_seed()
        self.epicure.seglayer.refresh()

    def crop_around_seeds(self, tframe):
        """ Get cropped image around the seeds """
        ## crop around the seeds, with a margin
        seeds = self.viewer.layers["Seeds"].data
        segt = self.epicure.seglayer.data[tframe]
        extend = int(float(self.max_distance.text())*1.1)
        labelBB = ut.getBBox2DFromPts(seeds, extend, segt.shape)
        segBB = ut.cropBBox2D(segt, labelBB)
        ## mask where there are cells
        maskBB = np.copy(segBB)
        maskBB = 1*(maskBB==0)
        maskBB = np.uint8(maskBB)
        ## fill the borders
        maskBB = binary_erosion(maskBB, footprint=self.disk_one)
        ## place labels in the seed positions
        pos = ut.positions2DIn2DBBox( seeds, labelBB )
        markers = np.zeros(maskBB.shape, dtype="int32")
        freelabs = self.epicure.get_free_labels( len(pos) )
        slab = freelabs[0]
        for freelab, p in zip(freelabs, pos):
            markers[p] = freelab
        return segBB, markers, maskBB, labelBB
    
    def diffusion_from_points(self, tframe, segBB, markers, maskBB, labelBB):
        """ Segment from seeds with a diffusion based method (gradient intensity slows it) """
        movt = self.viewer.layers["Movie"].data[tframe]
        imgBB = ut.cropBBox2D(movt, labelBB)
        markers[maskBB==0] = -1 ## block filled area 
        ## fill from seeds with diffusion method
        splitted = random_walker( imgBB, labels=markers, beta=700, tol=0.01 )
        splitted = label(splitted)
        new_labels = np.unique(markers)
        i = 0
        for lab in set(splitted.flatten()):
            if lab > 0:
                splitted[splitted==lab] = new_labels[i]
                i = i + 1
        segBB[(maskBB>0)*(splitted>0)] = splitted[(maskBB>0)*(splitted>0)]
        return segBB

    def watershed_from_points(self, tframe, segBB, markers, maskBB, labelBB):
        """ Performs watershed from the seed points """
        movt = self.viewer.layers["Movie"].data[tframe] 
        imgBB = ut.cropBBox2D(movt, labelBB)
        splitted = watershed( imgBB, markers=markers, mask=maskBB )
        segBB[splitted>0] = splitted[splitted>0]
        return segBB
    
    def distance_from_points(self, tframe, segBB, markers, maskBB, labelBB):
        """ Segment cells from seed points with Voronoi method """
        # iteratif to block when meet other fixed labels 
        maxdist = float(self.max_distance.text())
        dist = 0
        while dist <= maxdist:
            markers = expand_labels( markers, distance=1 )
            markers[maskBB==0] = 0
            dist = dist + 1
        segBB[(maskBB>0) * (markers>0)] = markers[(maskBB>0) * (markers>0)]
        return segBB
        

    ######################################
    ## Cleaning options

    def create_cleaningBlock(self):
        """ GUI for cleaning segmentation """
        self.gCleaned = QGroupBox("Cleaning")
        clean_layout = QVBoxLayout()
        ## cells on border
        border_line = QHBoxLayout()
        border_btn = QPushButton("Remove border cells (width pixels)", parent=self)
        border_btn.clicked.connect(self.remove_border)
        border_line.addWidget(border_btn)
        self.border_size = QLineEdit()
        self.border_size.setText("1")
        border_line.addWidget(self.border_size)
        clean_layout.addLayout(border_line)
        
        ## too small cells
        small_line = QHBoxLayout()
        small_btn = QPushButton("Remove mini cells (area pixels)", parent=self)
        small_btn.clicked.connect(self.remove_smalls)
        small_line.addWidget(small_btn)
        self.small_size = QLineEdit()
        self.small_size.setText("4")
        small_line.addWidget(self.small_size)
        clean_layout.addLayout(small_line)

        ## Cell inside another cell
        inside_btn = QPushButton("Cell inside another: merge", parent=self)
        inside_btn.clicked.connect(self.merge_inside_cells)
        clean_layout.addWidget(inside_btn)

        ## sanity check
        sanity_btn = QPushButton("Sanity check", parent=self)
        sanity_btn.clicked.connect(self.sanity_check)
        clean_layout.addWidget(sanity_btn)

        ## reset labels
        reset_btn = QPushButton("Reset all", parent=self)
        reset_btn.clicked.connect(self.reset_all)
        clean_layout.addWidget(reset_btn)

        self.gCleaned.setLayout(clean_layout)

    def show_cleaningBlock(self):
        """ Show/hide cleaning interface """
        self.gCleaned.setVisible(not self.gCleaned.isVisible())

    ####################################
    ## Sanity check/correction options
    def sanity_check(self):
        """ Check if everything looks okayish, in case some bug or weird editions broke things """
        self.viewer.window._status_bar._toggle_activity_dock(True)
        progress_bar = progress(total=5)
        progress_bar.set_description("Sanity check:")
        progress_bar.update(0)
        ## check layers presence
        ut.show_info("Check and reopen if necessary EpiCure layers")
        self.epicure.check_layers()
        ## check that each label is unique
        progress_bar.update(1)
        progress_bar.set_description("Sanity check: label unicity")
        label_list = np.unique(self.epicure.seglayer.data)
        if self.epicure.verbose > 0:
            print("Checking label unicity...")
        self.check_unique_labels( label_list, progress_bar )
        ## check and update if necessary tracks 
        progress_bar.update(2)
        progress_bar.set_description("Sanity check: track gaps")
        ut.show_info("Check if some tracks contain gaps")
        gaped = self.epicure.handle_gaps( track_list=None )
        ## check that labels and tracks correspond
        progress_bar.set_description("Sanity check: label-track")
        progress_bar.update(3)
        if self.epicure.verbose > 0:
            print("Checking labels-tracks correspondance...")
        track_list = self.epicure.tracking.get_track_list()
        untracked = list(set(label_list) - set(track_list))
        if 0 in untracked:
            untracked.remove(0)
        if len(untracked) > 0:
            ut.show_warning("! Labels "+str(untracked)+" not in Tracks -- Adding it now")
            for untrack in untracked:
                self.epicure.add_one_label_to_track( untrack )
        
        ## update label list with changes that might have been done
        label_list = np.unique(self.epicure.seglayer.data)
        track_list = self.epicure.tracking.get_track_list()
        ## check if all tracks have associated labels in the image
        phantom_tracks = list(set(track_list) - set(label_list))
        if len(phantom_tracks) > 0:
            print("! Phantom tracks "+str(phantom_tracks)+" found")
            self.epicure.delete_tracks(phantom_tracks)
            print("-> Phantom tracks deleted from Tracks")
        
        ## finished
        if self.epicure.verbose > 0:
            print("Checking finished")
        progress_bar.close()
        self.viewer.window._status_bar._toggle_activity_dock(False)

    def check_unique_labels(self, label_list, progress_bar):
        """ Check that all labels are contiguous and not present several times (only by frame) """
        found = 0
        s = generate_binary_structure(2,2)
        pbtmp = progress(total=len(label_list), desc="Check labels", nest_under=progress_bar)
        for i, lab in enumerate(label_list):
            pbtmp.update(i)
            if lab > 0:
                for frame in self.epicure.seglayer.data:
                    if lab in frame:
                        labs, num_objects = ndlabel(binary_dilation(frame==lab, footprint=s), structure=s)
                        if num_objects > 1:
                            ut.show_warning("! Problem, label "+str(lab)+" found several times")
                            found = found + 1
                            continue
        pbtmp.close()
        if found <= 0:
            ut.show_info("Labels unicity ok")

    ###############
    ## Resetting

    def reset_all( self ):
        """ Reset labels through skeletonization, reset tracks, suspects, groups """
        if self.epicure.verbose > 0:
            ut.show_info( "Resetting everything ")
        self.viewer.window._status_bar._toggle_activity_dock(True)
        progress_bar = progress(total=5)
        progress_bar.set_description("Reset: get skeleton")
        progress_bar.update(0)
        ## get skeleton and relabel (ensure label unicity)
        #skel = np.zeros(self.epicure.seg.shape, dtype="uint8")
        #skel[self.epicure.seg==0] = 1
        skel = self.epicure.get_skeleton()
        skel = np.uint32( skel )
        self.epicure.seg = skel
        self.epicure.seglayer.data = skel
        progress_bar.update(1)
        progress_bar.set_description("Reset: relabel")
        self.epicure.reset_data()
        self.epicure.tracking.reset()
        self.epicure.junctions_to_label()
        self.epicure.seglayer.data = self.epicure.seg      
        progress_bar.update(2)
        progress_bar.set_description("Reset: reinit tracks")
        self.epicure.tracked = 0
        self.epicure.load_tracks(progress_bar)
        if self.epicure.verbose > 0:
            print("Resetting done")
        progress_bar.close()
        self.viewer.window._status_bar._toggle_activity_dock(False)



    ######################################
    ## Selection options
    def help_selection(self):
        ut.show_documentation_page("Selection options")

    def create_selectBlock(self):
        """ GUI for handling selection with shapes """
        self.gSelect = QGroupBox("Selection options")
        select_layout = QVBoxLayout()
        ## create/select the ROI
        draw_btn = QPushButton("Draw/Select ROI", parent=self)
        draw_btn.clicked.connect(self.draw_shape)
        select_layout.addWidget(draw_btn)
        remove_sel_btn = QPushButton("Remove cells inside ROI", parent=self)
        remove_sel_btn.clicked.connect(self.remove_cells_inside)
        select_layout.addWidget(remove_sel_btn)
        remove_line = QHBoxLayout()
        removeout_sel_btn = QPushButton("Remove cells outside ROI", parent=self)
        removeout_sel_btn.clicked.connect(self.remove_cells_outside)
        remove_line.addWidget(removeout_sel_btn)
        self.keep_new_cells = QCheckBox(text="Keep new cells")
        self.keep_new_cells.setChecked(True)
        remove_line.addWidget(self.keep_new_cells)
        select_layout.addLayout(remove_line)

        self.gSelect.setLayout(select_layout)

    def show_selectBlock(self):
        """ Show/hide select options block """
        self.gSelect.setVisible(not self.gSelect.isVisible())

    def draw_shape(self):
        """ Draw/select a shape in the Shapes layer """
        if self.shapelayer_name not in self.viewer.layers:
            self.create_shapelayer()
        ut.set_active_layer(self.viewer, self.shapelayer_name)
        lay = self.viewer.layers[self.shapelayer_name]
        lay.visible = True
        lay.opacity = 0.5

    def get_selection(self):
        """ Get the active (or first) selection """
        if self.shapelayer_name not in self.viewer.layers:
            return None
        lay = self.viewer.layers[self.shapelayer_name]
        selected = lay.selected_data
        if len(selected) == 0:
            if len(lay.shape_type) == 1:
                if self.epicure.verbose > 1:
                    print("No shape selected, use the only one present")
                lay.selected_data.add(0)
                selected = lay.selected_data
            else:
                ut.show_warning("No shape selected, do nothing")
                return None
        return lay.data[list(selected)[0]] 

    def get_labels_inside(self):
        """ Get the list of labels inside the current ROI """
        current_shape = self.get_selection()
        if current_shape is None:
            return None
        self.current_bbox = ut.getBBox2DFromPts(current_shape, 30, self.epicure.imgshape2D)
        self.current_cropshape = ut.positions2DIn2DBBox(current_shape, self.current_bbox )

        tframe = ut.current_frame(self.viewer)
        segt = self.epicure.seglayer.data[tframe]
        croped = ut.cropBBox2D(segt, self.current_bbox)
        labprops = regionprops(croped)
        inside = points_in_poly( [lab.centroid for lab in labprops], self.current_cropshape )
        toedit = [lab.label for i, lab in enumerate(labprops) if inside[i] ]
        return toedit

    def remove_cells_outside(self):
        """ Remove all labels centroids outside the selected ROI """
        tokeep = self.get_labels_inside()
        if self.keep_new_cells.isChecked():
            tframe = ut.current_frame(self.viewer)
            segt = self.epicure.seglayer.data[tframe]
            toremove = set(np.unique(segt).flatten()) - set(tokeep)
            self.epicure.remove_labels(list(toremove))
        else:
            self.epicure.keep_labels(tokeep)
        lay = self.viewer.layers[self.shapelayer_name]
        lay.remove_selected()
        self.epicure.finish_update()

    def remove_cells_inside(self):
        """ Remove all labels centroids inside the selected ROI """
        toremove = self.get_labels_inside()
        self.epicure.remove_labels(toremove)
        lay = self.viewer.layers[self.shapelayer_name]
        lay.remove_selected()
        self.epicure.finish_update()

    def lock_cells_inside(self):
        """ Check all cells inside the selected ROI into current group """
        tocheck = self.get_labels_inside()
        for lab in tocheck:
            self.check_label(lab)
        if self.epicure.verbose > 0:
            print(str(len(tocheck))+" cells checked in group "+str(self.check_group.text()))
        lay = self.viewer.layers[self.shapelayer_name]
        lay.remove_selected()
        self.epicure.finish_update()

    def group_cells_inside(self):
        """ Put all cells inside the selected ROI into current group """
        tocheck = self.get_labels_inside()
        if tocheck is None:
            if self.epicure.verbose > 0:
                print("No cell to add to group")
            return
        for lab in tocheck:
            self.group_label(lab)
        if self.epicure.verbose > 0:
            print(str(len(tocheck))+" cells assigend to group "+str(self.group_group.text()))
        lay = self.viewer.layers[self.shapelayer_name]
        lay.remove_selected()
        self.epicure.finish_update()


    ######################################
    ## Group cells functions
    def show_groupCellsBlock(self):
        self.gGroup.setVisible(not self.gGroup.isVisible())

    def create_groupCellsBlock(self):
        self.gGroup = QGroupBox("Group cells")
        group_layout = QVBoxLayout()
        groupgr = QHBoxLayout()
        groupgr_lab = QLabel()
        groupgr_lab.setText("Group name")
        groupgr.addWidget(groupgr_lab)
        self.group_group = QLineEdit()
        self.group_group.setText("Positive")
        groupgr.addWidget(self.group_group)
        group_layout.addLayout(groupgr)

        self.group_show = QCheckBox(text="Show groups")
        self.group_show.stateChanged.connect(self.see_groups)
        self.group_show.setChecked(False)
        group_layout.addWidget(self.group_show)

        #group_loadbtn = QPushButton("Load groups", parent=self)
        #group_loadbtn.clicked.connect(self.load_groups)
        #group_layout.addWidget(group_loadbtn)
        #group_savebtn = QPushButton("Save groups", parent=self)
        #group_savebtn.clicked.connect(self.save_group)
        #group_layout.addWidget(group_savebtn)
        group_resetbtn = QPushButton("Reset groups", parent=self)
        group_resetbtn.clicked.connect(self.reset_group)
        group_layout.addWidget(group_resetbtn)
        #self.lock_checked = QCheckBox("Lock checked cells")
        #self.lock_checked.setChecked(True)
        #check_layout.addWidget(self.lock_checked)
        group_sel_btn = QPushButton("Cells inside ROI to group", parent=self)
        group_sel_btn.clicked.connect(self.group_cells_inside)
        group_layout.addWidget(group_sel_btn)
        self.gGroup.setLayout(group_layout)

    def help_group(self):
        ut.show_documentation_page("Edit#group-options")
    
    def help_clean(self):
        ut.show_documentation_page("Edit#cleaning-options")

    def load_checked(self):
        cfile = self.get_filename("_checked.txt")
        with open(cfile) as infile:
            labels = infile.read().split(";")
        for lab in labels:
            self.check_load_label(lab)
        ut.show_info("Checked cells loaded")

    def reset_group(self):
        self.epicure.reset_groups()
        if self.group_show.isChecked():
            grouped = self.viewer.layers[self.grouplayer_name]
            grouped.data = np.zeros(grouped.data.shape, np.uint8)
            grouped.refresh()
            ut.set_active_layer(self.viewer, "Segmentation")

    def save_groups(self):
        groupfile = self.get_filename("_groups.txt")
        with open(groupfile, 'w') as out:
            out.write(";".join(group.write_group() for group in self.epicure.groups))
        ut.show_info("Cell groups saved in "+groupfile)


    def see_groups(self):
        if self.group_show.isChecked():
            ut.remove_layer(self.viewer, self.grouplayer_name)
            data = self.epicure.seglayer.data
            grouped = self.epicure.draw_groups()
            grouplayer = self.viewer.add_labels(grouped, name=self.grouplayer_name, opacity=0.75, blending="additive")
            ut.set_active_layer(self.viewer, "Segmentation")
        else:
            ut.remove_layer(self.viewer, self.grouplayer_name)
            ut.set_active_layer(self.viewer, "Segmentation")
    
    def group_label(self, label):
        """ Add label to group """
        group = self.group_group.text()
        self.group_ingroup(label, group)
       
    def check_label(self, label):
        """ Mark label as checked """
        group = self.check_group.text()
        self.check_ingroup(label, group)
        
    def group_ingroup(self, label, group):
        """ Add the given label to chosen group """
        self.epicure.cell_ingroup( label, group )
        if self.grouplayer_name in self.viewer.layers:
            self.redraw_label_group( label, group )
       
    def check_load_label(self, labelstr):
        """ Read the label to check from file """
        res = labelstr.split("-")
        cellgroup = res[0]
        celllabel = int(res[1])
        self.check_ingroup(celllabel, cellgroup)
        
    def add_cell_to_group(self, event):
        """ Add cell under click to the current group """
        label = ut.getCellValue( self.epicure.seglayer, event ) 
        self.group_label(label)

    def remove_cell_group(self, event):
        """ Remove the cell from the group it's in if any """
        label = ut.getCellValue( self.epicure.seglayer, event ) 
        self.epicure.cell_removegroup( label )
        if self.grouplayer_name in self.viewer.layers:
            self.redraw_label_group( label, 0 )

    def redraw_label_group(self, label, group):
        """ Update the Group layer for label """
        lay = self.viewer.layers[self.grouplayer_name]
        if group == 0:
            lay.data[self.epicure.seg==label] = 0
        else:
            igroup = self.epicure.get_group_index(group) + 1
            lay.data[self.epicure.seg==label] = igroup
        lay.refresh()

    ######### overlay message
    def add_overlay_message(self):
        over = self.epicure.text
        text = over + "\n"
        #for txt in self.epicure.overtext.values():
        #    text += txt
        ut.setOverlayText(self.viewer, text, size=10)

    ################## Track editing functions

    def key_tracking_binding(self):
        """ active key bindings for tracking options """
        self.epicure.overtext["trackedit"] = "---- Track editing ---- \n"
        self.epicure.overtext["trackedit"] += "  <r> to show/hide the tracks \n"
        self.epicure.overtext["trackedit"] += "  <t> for tracks editing mode \n"
        self.epicure.overtext["trackedit"] += "  <t>, <t> end tracks editing mode \n"
        self.epicure.overtext["trackedit"] += "  <t>, (Left-Right) clicks to merge two tracks (temporally or spatially) \n"
        self.epicure.overtext["trackedit"] += "  <t>, <Control>+Left clicks manually do a new track \n(<Control>+Right click to end it) \n"
        self.epicure.overtext["trackedit"] += "  <t>, <Shift>+Right clicks split the track temporally \n"
        self.epicure.overtext["trackedit"] += "  <t>, <Shift>+Left drag-click swap 2 tracks from current frame \n"
        self.epicure.overtext["trackedit"] += "  <t>, <Alt>+(Left-Right) clicks to interpolate labels temporally \n"
        self.epicure.overtext["trackedit"] += "  <t>, Double-Right click to delete all the track from current frame \n"
        
        @self.epicure.seglayer.bind_key('r', overwrite=True)
        def see_tracks(seglayer):
            if self.tracklayer_name in self.viewer.layers:
                tlayer = self.viewer.layers[self.tracklayer_name]
                tlayer.visible = not tlayer.visible

        @self.epicure.seglayer.bind_key('t', overwrite=True)
        def edit_track(layer):
            self.label_tr = None 
            self.start_label = None
            self.interp_labela = None
            self.interp_labelb = None
            ut.show_info("Tracks editing mode")
            self.old_mouse_drag, self.old_key_map = ut.clear_bindings(self.epicure.seglayer)

            @self.epicure.seglayer.mouse_drag_callbacks.append
            def click(layer, event):
                """ Edit tracking """
                if event.type == "mouse_press":
                  
                    if len(event.modifiers)== 0 and event.button == 1:
                        """ Merge two tracks, spatially or temporally: left click, select the first label """
                        self.start_label = self.epicure.seglayer.get_value(position=event.position, view_direction = event.view_direction, dims_displayed=event.dims_displayed, world=True)
                        self.start_pos = event.position
                        # move one frame after for next cell to link
                        #ut.set_frame( self.epicure.viewer, event.position[0]+1 )
                        return
                    if len(event.modifiers)== 0 and event.button == 2:
                        """ Merge two tracks, spatially or temporally: right click, select the second label """
                        if self.start_label is None:
                            if self.epicure.verbose > 0:
                                print("No left click done before right click, don't merge anything")
                            return
                        end_label = self.epicure.seglayer.get_value(position=event.position, view_direction = event.view_direction, dims_displayed=event.dims_displayed, world=True)
                        end_pos = event.position
                        if self.epicure.verbose > 0:
                            print("Merging track "+str(self.start_label)+" with track "+str(end_label))
                        
                        if self.start_label is None or self.start_label == 0 or end_label == 0:
                            if self.epicure.verbose > 0:
                                print("One position is not a cell, do nothing")
                            return
                        ## ready, merge
                        self.merge_tracks( self.start_label, self.start_pos, end_label, end_pos )
                        self.end_track_edit()
                        return

                    if (len(event.modifiers) == 1) and ("Shift" in event.modifiers):
                        if event.button == 2:
                            ### Split the track in 2: new label for the next frames 
                            start_frame = int(event.position[0])
                            label = ut.getCellValue(self.epicure.seglayer, event) 
                            new_label = self.epicure.get_free_label()
                            self.epicure.replace_label( label, new_label, start_frame )
                            if self.epicure.verbose > 0:
                                ut.show_info("Split track "+str(label)+" from frame "+str(start_frame))
                            self.end_track_edit()
                            return
                        
                        if event.button == 1:
                            ### Swap the two track from the current frame 
                            start_frame = int(event.position[0])
                            label = ut.getCellValue(self.epicure.seglayer, event) 
                            yield
                            while event.type == 'mouse_move':
                                yield
                            end_label = self.epicure.seglayer.get_value(position=event.position, view_direction = event.view_direction, dims_displayed=event.dims_displayed, world=True)                           
                            
                            if label == 0 or end_label == 0:
                                if self.epicure.verbose > 0:
                                    print("One position is not a cell, do nothing")
                                return

                            self.epicure.swap_tracks( label, end_label, start_frame )
                            
                            if self.epicure.verbose > 0:
                                ut.show_info("Swapped track "+str(label)+" with track "+str(end_label)+" from frame "+str(start_frame))
                            self.end_track_edit()
                            return

                    if (len(event.modifiers) == 1) and ("Control" in event.modifiers):
                        if event.button == 1:
                            ### Manual tracking: get a new label and spread it to clicked cells on next frames
                            zpos = int(event.position[0])
                            if self.label_tr is None:
                                ## first click: get the track label
                                self.label_tr = ut.getCellValue(self.epicure.seglayer, event) 
                            else:
                                old_label = ut.setCellValue(self.epicure.seglayer, self.epicure.seglayer, event, self.label_tr, layer_frame=zpos, label_frame=zpos)
                                self.epicure.tracking.remove_one_frame( old_label, zpos )
                                self.epicure.add_label( [self.label_tr], zpos )
                            ## advance to next frame, ready for a click
                            self.viewer.dims.set_point(0, zpos+1)
                            ## if reach the end, stops here for this track
                            if (zpos+1) >= self.epicure.seglayer.data.shape[0]:
                                self.end_track_edit()
                            return
                        if event.button == 2:
                            self.end_track_edit()
                            return
                    
                    if (len(event.modifiers) == 1) and ("Alt" in event.modifiers):
                        if event.button == 1:
                            ## left click, first cell
                            self.interp_labela = ut.getCellValue(self.epicure.seglayer, event) 
                            self.interp_framea = int(event.position[0])
                            return
                        if event.button == 2:
                            ## right click, second cell
                            labelb = ut.getCellValue(self.epicure.seglayer, event) 
                            interp_frameb = int(event.position[0])
                            if self.interp_labela is not None:
                                if abs(self.interp_framea - interp_frameb) <= 1:
                                    print("No frames to interpolate, exit")
                                    self.end_track_edit()
                                    return
                                if self.interp_framea < interp_frameb:
                                    self.interpolate_labels(self.interp_labela, self.interp_framea, labelb, interp_frameb)
                                else:
                                    self.interpolate_labels(labelb, interp_frameb, self.interp_labela, self.interp_framea )
                                self.end_track_edit()
                                return
                            else:
                                print("No cell selected with left click before. Exit mode")
                                self.end_track_edit()
                                return

                ## A right click or other click stops it
                self.end_track_edit()

            @self.epicure.seglayer.mouse_double_click_callbacks.append
            def double_click(layer, event):
                """ Edit tracking : double click options """
                if event.type == "mouse_double_click":      
                    if len(event.modifiers)== 0 and event.button == 2:
                        """ Double right click: delete all the track from the current frame """
                        tframe = int(event.position[0])
                        label = ut.getCellValue(self.epicure.seglayer, event)
                        if label > 0:
                            self.epicure.replace_label( label, 0, tframe )
                            if self.epicure.verbose > 0:
                                print("Track "+str(label)+" deleted from frame "+str(tframe))
                        self.end_track_edit()
                        return
                    
                ## A double click with nothing else stop the mode
                self.end_track_edit()
        
            @self.epicure.seglayer.bind_key('t', overwrite=True)
            def end_edit_track(layer):
                self.end_track_edit()

    def end_track_edit(self):
        self.start_label = None
        self.interp_labela = None
        self.interp_labelb = None
        ut.reactive_bindings( self.epicure.seglayer, self.old_mouse_drag, self.old_key_map )
        ut.show_info("End track edit mode")

    def merge_tracks(self, labela, posa, labelb, posb):
        """ 
            Merge track with label a with track of label b, temporally or spatially 
        """
        if int(posb[0]) == int(posa[0]):
            self.tracks_spatial_merging( labela, posa, labelb, posb )
        else:
            self.tracks_temporal_merging( labela, posa, labelb, posb )

    def tracks_spatial_merging( self, labela, posa, labelb, posb ):
        """ Merge spatially two tracks: labels have to be touching all along the common frames """
        ## get last common frame
        lasta = self.epicure.tracking.get_last_frame( labela )
        lastb = self.epicure.tracking.get_last_frame( labelb )
        lastcommon = min(lasta, lastb)
        ## check if labels are touching from first frame (posa[0]) to the last common frame
        touched = True
        for frame in range( int(posa[0]), lastcommon+1 ):
            bbox, mask = ut.getBBox2DMerge( self.epicure.seg[frame], labela, labelb )
            bbox = ut.extendBBox2D( bbox, 1.05, self.epicure.imgshape2D )
            segt_crop = ut.cropBBox2D( self.epicure.seg[frame], bbox )
            touched = ut.checkTouchingLabels( segt_crop, labela, labelb )
            if not touched:
                print("Labels "+str(labela)+" and "+str(labelb)+" are not always touching. Refusing to merge them")
                return 

        ## Looks, ok, create a new track and merge the two tracks in it
        new_label = self.epicure.get_free_label()
        new_labels = []
        ind_tomodif = None
        for frame in range( int(posa[0]), lastcommon+1 ):
            bbox, merged = ut.getBBox2DMerge( self.epicure.seg[frame], labela, labelb )
            bbox = ut.extendBBox2D( bbox, 1.05, self.epicure.imgshape2D )
            segt_crop = ut.cropBBox2D( self.epicure.seg[frame], bbox )
            
            ## merge the two labels together
            joinlab = ut.cropBBox2D( merged, bbox )
            footprint = disk(radius=3)
            joinlab = new_label * binary_closing(joinlab, footprint)
           
            ## get the index and new values to change
            indmodif = self.ind_boundaries( joinlab )
            indmodif = ut.toFullMoviePos( indmodif, bbox, frame )
            if ind_tomodif is None:
                ind_tomodif = indmodif
            else:
                ind_tomodif = np.vstack((ind_tomodif, indmodif))
            new_labels = new_labels + np.repeat(0, len(indmodif)).tolist()
            curmodif = np.argwhere( joinlab == new_label )
            new_labels = new_labels + [new_label]*curmodif.shape[0]
            curmodif = ut.toFullMoviePos( curmodif, bbox, frame )
            ind_tomodif = np.vstack((ind_tomodif, curmodif))
        
        ## update the labels and the tracks
        self.epicure.change_labels(ind_tomodif, new_labels)
        if self.epicure.verbose > 0:
            ut.show_info("Merged spatially "+str(labela)+" with "+str(labelb)+" from frame "+str(int(posa[0]))+" to frame "+str(lastcommon)+"\n New track label is "+str(new_label))


    def tracks_temporal_merging( self, labela, posa, labelb, posb ):
        """ 
        Merge track with label a with track of label b if consecutives frames. 
        It does not check if label are close in distance, assume it is.
        """
        if abs(int(posb[0]) - int(posa[0])) != 1:
            if self.epicure.verbose > 0:
                print("Frames to merge are not consecutives, refused")
            return

        ## Frames are consecutives, swap so that a is first if necessary
        if posa[0] > posb[0]:
            posc = np.copy(posa)
            posa = posb
            posb = posc
            labelc = labela
            labela = labelb
            labelb = labelc

        ## Check that posa is last frame of label a and pos b first frame of label b
        if int(posa[0]) != self.epicure.tracking.get_last_frame( labela ):
            if self.epicure.verbose > 0:
                print("Clicked label "+str(labela)+" at frame "+str(posa[0])+" is not the last frame of the track, refused")
            return

        if posb[0] != self.epicure.tracking.get_first_frame( labelb ):
            if self.epicure.verbose > 0:
                print("Clicked label "+str(labelb)+" at frame "+str(posb[0])+" is not the first frame of the track, refused")
            return

        self.epicure.replace_label( labelb, labela, int(posb[0]) )
        

    def get_parents(self, twoframes, labels):
        """ Get parent of all labels """
        return self.epicure.tracking.find_parents( labels, twoframes )
    
    def get_position_label_2D(self, img, labels, parent_labels):
        """ Get position of each label to update with parent label """
        #start_time = time.time()
        indmodif = None
        new_labels = []
        ## get possible free labels, to be sure that it will not take the same ones
        free_labels = self.epicure.get_free_labels(len(labels))
        for i, lab in enumerate(labels):
            parent_label = parent_labels[i]
            if parent_label is None:
                parent_label = free_labels[i]
                parent_labels[i] = parent_label
            curmodif = np.argwhere( img==lab )
            if indmodif is None:
                indmodif = curmodif
            else:
                indmodif = np.vstack((indmodif, curmodif))
            new_labels = new_labels + ([parent_label]*curmodif.shape[0])
        #ut.show_info("Pos label in "+"{:.3f}".format((time.time()-start_time)/60)+" min")
        return indmodif, new_labels, parent_labels

    def inherit_parent_labels(self, myframe, labels, bbox, frame):
        """ Get parent labels if any and indices to modify with it """
        if ( self.epicure.tracked == 0 ) or (frame<=0):
            parent_labels = [None]*len(labels)
            indmodif, new_labels, parent_labels = self.get_position_label_2D(myframe, labels, parent_labels)
        else:
            twoframes = ut.crop_twoframes( self.epicure.seglayer.data, bbox, frame )
            twoframes[1] = np.copy(myframe) # merge of the labels and 0 outside
            orig_frame = ut.cropBBox2D(self.epicure.seglayer.data[frame], bbox)
            ut.keep_orphans(twoframes, orig_frame, labels)
            
            parent_labels = self.get_parents( twoframes, labels )
        
            indmodif, new_labels, parent_labels = self.get_position_label_2D(twoframes[1], labels, parent_labels)

        if self.epicure.verbose > 0:
            print("Set value (from parent or new): "+str(np.unique(new_labels)))
        ## back to movie position
        indmodif = ut.toFullMoviePos( indmodif, bbox, frame )
        return indmodif, new_labels, parent_labels
    
    def inherit_child_labels(self, myframe, labels, bbox, frame, parent_labels, keep_labels):
        """ Get child labels if any and indices to modify with it """
        #start_time = time.time()
        if (self.epicure.tracked == 0 ) or (frame>=self.epicure.nframes-1):
            return [], []
        else:
            twoframes = np.copy( ut.cropBBox2D(self.epicure.seglayer.data[frame+1], bbox) )
            ## check if the new value to set is present in the following frame, in that case don't do any propagation
            for par in parent_labels:
                if np.any( twoframes==par ):
                    if self.epicure.verbose > 1:
                        print("Propagating: not because new value present in labels: "+str(par))
                    return [], []

            twoframes = np.stack( (twoframes, np.copy(myframe)) )
            orig_frame = ut.cropBBox2D(self.epicure.seglayer.data[frame], bbox)
            prev = np.copy(twoframes[0])
            ut.keep_orphans(twoframes, orig_frame, keep_labels)
            child_labels = self.get_parents( twoframes, labels )
            
            if self.epicure.verbose > 0:
                print("Propagate  the new value to: "+str(child_labels))
            if child_labels is None:
                return [], []
        
        # get position of each child label to update with current label
        indmodif = []
        new_labels = []
        for i, lab in enumerate(child_labels):
            if lab is not None:
                after_frame = frame+1
                inds = self.epicure.get_label_indexes( lab, after_frame )
                indmodif = indmodif + inds
                new_labels = new_labels + np.repeat(parent_labels[i], len(inds)).tolist()
        return indmodif, new_labels

    def propagate_label_change(self, myframe, labels, bbox, frame, keep_labels):
        """ Propagate the new labelling to match parent/child labels """
        start_time = time.time()
        indmodif = self.ind_boundaries( myframe )
        indmodif = ut.toFullMoviePos( indmodif, bbox, frame )
        #ut.show_info("Boundaries in "+"{:.3f}".format((time.time()-start_time)/60)+" min")
        new_labels = np.repeat(0, len(indmodif)).tolist()

        ## get parent labels if any for each label
        indmodif2, new_labels2, parent_labels = self.inherit_parent_labels(myframe, labels, bbox, frame)
        if indmodif2 is not None:
            indmodif = np.vstack((indmodif, indmodif2))
            new_labels = new_labels+new_labels2
        if self.epicure.verbose > 1:
            ut.show_duration(start_time, "Propagation, parents found, ")

        ## propagate the split: get child labels if any for each label
        indmodif_child, new_labels_child = self.inherit_child_labels(myframe, labels, bbox, frame, parent_labels, keep_labels)
        if indmodif_child != []:
            indmodif = np.vstack((indmodif, indmodif_child))
            new_labels = new_labels + new_labels_child
        if self.epicure.verbose > 1:
            ut.show_duration(start_time, "Propagation, childs found, ")
        
        ## go, do the update
        self.epicure.change_labels(indmodif, new_labels)


    ############# Test
    def interpolate_labels( self, labela, framea, labelb, frameb ):
        """ 
            Interpolate the label shape in between two labels 
            Based on signed distance transform, like Fiji ROIs interpolation
        """
        if self.epicure.verbose > 1:
            print("Interpolating between "+str(labela)+" and "+str(labelb))
            print("From frame "+str(framea)+" to frame "+str(frameb))
            start_time = time.time()
        
        sega = self.epicure.seglayer.data[framea]
        maska = np.isin( sega, [labela] )
        segb = self.epicure.seglayer.data[frameb]
        maskb = np.isin( segb, [labelb] )

        ## get merged bounding box, and crop around it
        mask = maska | maskb
        props = regionprops(mask*1)
        bbox = ut.extendBBox2D( props[0].bbox, extend_factor=1.2, imshape=mask.shape )

        maska = ut.cropBBox2D( maska, bbox )
        maskb = ut.cropBBox2D( maskb, bbox )

        ## get signed distance transform of each label
        dista = edt.sdf( maska )
        distb = edt.sdf( maskb )

        inds = None
        new_labels = []
        for frame in range(framea+1, frameb):
            p = (frame-framea)/(frameb-framea)
            dist = (1-p) * dista + p * distb
            ## change only pixels that are 0
            frame_crop = ut.cropBBox2D( self.epicure.seglayer.data[frame], bbox )
            tochange = binary_dilation(dist>0, footprint=disk(radius=2)) * (frame_crop<=0)   # expand to touch neighbor label
            
            ## indexes and new values to change
            indmodif = np.argwhere( tochange > 0 ).tolist()
            indmodif = ut.toFullMoviePos( indmodif, bbox, frame )
            if inds is None:
                inds = indmodif
            else:
                inds = np.vstack( (inds, indmodif) )
            new_labels = new_labels + [labela]*len(indmodif)

            ## be sure to remove the boundaries with neighbor labels
            bound_ind = self.ind_boundaries( tochange )
            new_labels = new_labels + [0]*len(bound_ind)
            bound_ind = ut.toFullMoviePos( bound_ind, bbox, frame )
            inds = np.vstack( (inds, bound_ind) )

        ## Go, apply the changes
        self.epicure.change_labels( inds, new_labels )
        ## change the second track to first track value
        self.epicure.replace_label( labelb, labela, frameb )
        if self.epicure.verbose > 1:
            ut.show_duration( start_time, "Interpolation took " )
        if self.epicure.verbose > 0:
            ut.show_info( "Interpolated label "+str(labela)+" from frame "+str(framea+1)+" to "+str(frameb-1) )

        


