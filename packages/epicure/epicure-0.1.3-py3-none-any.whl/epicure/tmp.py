
    def check_labels_epicell(self):
        """ Check all labels if has correct corresponding epicell """
        props = regionprops(self.epicure.seg)
        for prop in props:
            label = prop.label
            if label > 0:
                if label in self.epicure.epicells.keys():
                    self.epicure.epicells[label].check_epicell(label, prop.bbox)
                else:
                    print("Label "+str(label)+" missing in epicells list")
                    self.epicure.add_epicell(label, prop.bbox)
                    print("---> corrected")
    ############# Edit epicells
    def has_cell(self, label):
        """ Check if the epicell with label is present """
        return label in self.epicells.keys()

    def epicell_population(self):
        """ Initialize the set of cells (tracks) """
        self.epicells = {}
        tracks = self.tracking.get_track_list()
        for lab in tracks:
            self.add_epicell(label)

    def add_epicell(self, lab):
        """ Add a new epicell """
        epice = EpiCell(self)
        epice.set_label(lab)
        self.epicells[lab] = epice
    
    def add_one_frame_to_epicell(self, label, frame, bbox=None):
        """ Add one frame to the epicell label """
        if label in self.epicells.keys():
            self.epicells[label].add_one_frame(frame, bbox)
        else:
            self.add_epicell(label)
    
    def add_one_frame_epicells(self, labels, frame, bbox=None, refresh=True):
        """ Add one frame to the epicels """
        bb = None
        for i, lab in enumerate(labels):
            if bbox is not None:
                bb = bbox[i]
            self.add_one_frame_to_epicell(lab, frame, bb)
        if self.tracked > 0:
            self.tracking.update_tracks( labels, refresh=refresh )

    def delete_epicell(self, lab):
        """ Remove epicell of label lab """
        if lab in self.epicells.keys():
            del self.epicells[lab]
            if self.tracked > 0:
                self.tracking.remove_track( lab, refresh=False )
    
    def remove_if_epicell(self, lab):
        """ Remove epicell of label lab if it's absent """
        if lab in self.epicells.keys():
            if lab not in np.unique(self.seg):
                del self.epicells[lab]
                return True
        return False
    
    def remove_one_frame_epicells(self, labels, frame, refresh=True):
        """ Remove one frame to epicells with the labels in the list """
        for lab in labels:
            if lab in self.epicells.keys():
                self.epicells[lab].remove_one_frame(frame)
        if self.tracked > 0:
            self.tracking.update_tracks( labels, refresh=refresh )

    def remove_epicells(self, labels):
        """ Remove epicells with the labels in the list """
        for lab in labels:
            self.remove_epicell(lab)

    def update_changed_labels( self, img_before, img_after, added=True, removed=True ):
        """ Update epicells from changes between the two labelled images """
        print("Updating changed labels")
        if len(img_before.shape) > 2:
            for i, frame in enumerate(img_before):
                self.update_changed_labels_oneframe( i, frame, img_after[i], added=added, removed=removed )
        else:
            self.update_changed_labels_oneframe( None, img_before, img_after, added=added, removed=removed )
    
    def update_changed_labels_oneframe( self, frame, img_before, img_after, added=True, removed=True ):
        """ Update epicells from changes between the two labelled images at frame """
        ## Look for removed labels
        if added:
            removed_labels = np.setdiff1d( img_before, img_after )
            self.remove_one_frame_epicells( removed_labels, frame, refresh=not removed )
        ## Look for added labels
        if removed:
            added_labels = np.setdiff1d( img_after, img_before )
            self.add_one_frame_epicells( added_labels, frame, bbox=None, refresh=True )

    def update_epicell( self, label, frame ):
        """ Update the bounding box of epicell label, remove if necessary """
        if label not in self.epicells.keys():
            print("Cell "+str(label)+" not found")
            return
        ## get cell bounding box
        bbox = ut.getBBoxLabel( self.seg[frame], label )
        ## cell has been totally erased from current frame, remove it
        if bbox is None:
            self.remove_one_frame_epicells( [label], frame, refresh=True )
            return
        ## cell is still there, update its bounding box
        self.epicells[label].update_xy_bbox( bbox )
        
    def update_some_epicells(self, labels):
        """ Update if necessary the listed epicells """
        print("update some epicell, can remove ?")
        if 0 in labels:
            labels.remove(0)
        all_labels = np.unique(self.seg)
        all_epicells = self.epicells.keys()
        for lab in labels:
            ## label has been removed
            if lab not in all_labels:
                self.delete_epicell(lab)
            else:
                ## label has been created
                if lab not in all_epicells:
                    self.add_epicell(lab)
        ## update their tracks as well
        self.tracking.update_tracks(labels)

    def update_epicells(self):
        """ Update the epicells dict to be sure it's udpated """
        all_labels = list(np.unique( self.seg ))
        all_epicells = set(self.epicells.keys())
        if 0 in all_labels:
            all_labels.remove(0)
        all_labels = set(all_labels)
        ## handle left epicells (no more in the segmentation)
        toremove = all_epicells - all_labels
        if len(toremove) > 0:
            for lab in toremove:
                if lab > 0:
                    self.delete_epicell(lab)
        ## Add missing labels
        toadd = all_labels - all_epicells
        if len(toadd) > 0:
            for lab in toadd:
                if lab > 0:
                    self.add_epicell(lab)
        ## Update tracks
        if self.tracked > 0:
            self.tracking.update_tracks( all_labels )

    def remove_phantom_epicells(self):
        """ If some epicells don't have label anymore, remove it """
        all_epicells = set(self.epicells.keys())
        labels = set(self.seg.flatten())
        if 0 in labels:
            labels.remove(0)
        for epice in all_epicells:
            if epice not in labels:
                print("Removing phantom epicell "+str(epice))
                self.delete_epicell(epice)


    def swap_epicells(self, lab, other_lab):
        """ Swap the label of the epicells """
        epice = self.epicells.pop(lab)
        other_epice = self.epicells.pop(other_lab)
        self.epicells[lab] = other_epice
        other_epice.set_label( lab )
        self.epicells[other_lab] = epice
        epice.set_label( other_lab )
        self.tracking.update_tracks([lab, other_lab])
    
    def update_epicells_xy_bbox(self, labels, frame):
        """ Update the bounding box of the epicells at current frame """
        segt = self.seg[frame]
        for lab in labels:
            if lab > 0:
                self.epicells[lab].update_xy_bbox( bbox=None, img=segt )
        self.tracking.update_tracks(labels)



        ## test color tracks
        #labels = np.unique(self.epicure.seglayer.data)
        #colors = []
        #collabs = []
        #cmap = self.viewer.layers["Segmentation"]
        #for lab in labels:
        #    if lab == 0:
        #        col = np.array([0,0,0,0])
        #    else:
        #        col = cmap.get_color(lab)
        #    colors.append(col)
        #    collabs.append( (lab)/np.max(labels) )
        #self.viewer.layers["Tracks"].colormaps_dict["track_id"] = vispy.color.Colormap(np.array(colors), np.array(collabs))
    
        
############"" Lock        
    #######################
    ## Lock options
    def reset_locked(self):
        """ Unlock all cells """
        for cell in self.epicells.values():
            cell.lock(False)
        self.nlocked = 0
    
    def is_locked(self, label):
        """ returns if label is locked or not """
        if self.nlocked == 0:
            return False
        if label in self.epicells.keys():
            return self.epicells[label].locked
        return False
    
    def locked_event(self, event):
        """ Check if label under event positon is locked or not """
        if self.nlocked > 0:
            label = ut.getCellValue(self.seglayer, event)
            return self.locked_label(label)
        return False
    
    def locked_pos(self, pos):
        """ Check if current position can be edited or not (checked) """
        if self.nlocked > 0:
            label = self.seg[ut.tuple_int(pos)]
            return self.locked_label(label)
        return False
    
    def locked_label(self, label):
        """ Check if given cell is locked or not """
        return (self.nlocked >0) and (self.epicells.get(label) is not None) and (self.epicells[label].locked)

    def get_locked_labels(self):
        """ List of locked labels """
        if self.nlocked <= 0:
            return []
        return [label for label, cell in self.epicells.items() if cell.locked]
    
    def get_only_unlocked(self, frame):
        """ Returns the labels at frame that are not locked """ 
        if self.nlocked == 0:
            return self.seg[frame]
        return self.only_unlocked_labels(frame)
    
    def only_unlocked_labels(self, frame):
        """ Put all locked labels to 0 """
        freelab = np.copy(self.seg[frame])
        return self.only_unlocked(freelab)
    
    def only_unlocked(self, img):
        """ Put all locked labels to 0 """
        mask = np.isin(img, self.get_locked_labels())
        img[mask] = 0
        return img
    
    def clear_locked_labels(self, img):
        """ Put locked labels to 0 in the img """
        if self.nlocked == 0:
            return img
        lockedmask = np.isin(img, self.get_locked_labels())
        img[lockedmask] = 0
        return img
    
    def draw_locked(self):
        """ Draw all the epicells that are locked """
        locked = np.zeros(self.seg.shape, np.uint8)
        if self.epicells is None:
            return locked
        for label, cell in self.epicells.items():
            if cell.locked:
                np.place(locked, self.seg==label, 1)
        return locked
    
    def draw_update_locked(self, label, lock):
        lay = self.viewer.layers[self.locked_name]
        lay.data[self.seg==label] = lock
        lay.refresh()


    def reserve_labels(self, trackids, splitdf, mergedf):
        """ Unsure that trackids do not contain a checked label """
        locked_labels = self.get_locked_labels()
        if len(locked_labels) > 0:
            newval = np.max(trackids)+1
            for tid in np.unique(trackids):
                if tid in locked_labels:
                    #print("reserving "+str(tid))
                    while newval in locked_labels:
                            newval = newval + 1
                    trackids[trackids==tid] = newval
                    if len(splitdf) > 0:
                        splitdf = splitdf.replace(to_replace=tid, value=newval)
                    if len(mergedf) > 0:
                        mergedf = mergedf.replace(to_replace=tid, value=newval)
                    newval = newval + 1
        return trackids, splitdf, mergedf
        
        #self.nlocked = 0           ## Number cells that are locked
        #self.locked_name = "Locked"   ## name of the locked layer
