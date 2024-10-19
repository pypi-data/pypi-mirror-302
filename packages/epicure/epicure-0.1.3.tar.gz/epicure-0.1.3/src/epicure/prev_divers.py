
    ######## Cell trajectory
    def one_cell_movie(self, label):
        """ Isolate the movie of one cell """
        if label not in np.unique(self.seg):
            ut.show_error("Cell "+str(label)+" not found")
        bbox = ut.getBBoxLabel(self.seg, label)
        print(bbox)
        ## prepare the movie
        movshape = []
        extend = 1
        for i in range(3):
            if i > 0:
                extend = 1.1  ## keep a little outside the cell
            movshape.append( int((bbox[i+3]-bbox[i])*extend) )
        cellmovie = np.zeros( tuple(movshape) )
        ## get the center of the cell, copy sym and place at the center
        for frame in range(bbox[0], bbox[3]+1, 1):
            tseg = ut.get_frame()
    

    #### prev
    def reset_checked(self):
        """ erase all cells """
        self.epicells = {}
        self.groups = {}

    def is_checked(self, label):
        """ returns if label already checked or not """
        if self.epicells is None:
            return False
        return label in self.epicells.keys()

    def add_epicell(self, label, group="Checked"):
        """ Create a new (checked) branch, unmodifiable """
        epice = EpiCell(self)
        epice.create_epicell(label, group)
        self.epicells[label] = epice
        ## add new group if necessary
        if group not in self.groups:
            self.groups[group] = len(self.groups)+1
            self.outputing.update_selection_list()

    def remove_epicell(self, label):
        """ Uncheck the branch, remove it """
        if self.epicells.get(label) is None:
            print("No checked cell to remove")
        else:
            epice = self.epicells[label]
            self.epicells.pop(label) ## ? remove from dict 
            del epice
            print("Epicell removed")

    
    def reserve_labels(self, trackids, splitdf, mergedf):
        """ Unsure that trackids do not contain a checked label """
        if self.epicells is None:
            return trackids
        newval = np.max(trackids)+1
        for tid in np.unique(trackids):
            if tid in self.epicells.keys():
                #print("reserving "+str(tid))
                while newval in self.epicells.keys():
                    newval = newval + 1
                trackids[trackids==tid] = newval
                if len(splitdf) > 0:
                    splitdf = splitdf.replace(to_replace=tid, value=newval)
                if len(mergedf) > 0:
                    mergedf = mergedf.replace(to_replace=tid, value=newval)
                newval = newval + 1
        return trackids, splitdf, mergedf

    ############ Previous Get unused label
    def get_free_label(self):
        """ Get the smallest unused label """
        if self.unused_label is None:
            self.unused_label = ut.get_free_label(self.seglayer)
            return self.unused_label
        #if self.unused_label in np.unique(self.seglayer.data):
        #    self.update_free_label()
        return self.unused_label
    
    def free_label(self):
        """ Get the smallest unused label and update it """
        res = self.get_free_label()
        self.update_free_label()
        return res

    def relabel(self):
        """ Relabel all labels to have consecutive values """
        ut.relabel_layer(self.seglayer)
        self.unused_label = np.max(self.seglayer.data)+1

    def reset_free_label(self):
        """ Get the first smallest label """
        self.unused_label = ut.get_free_label(self.seglayer)

    def update_free_label(self):
        """ Update the value of smallest unused label """
        self.unused_label = self.unused_label + 1 #ut.get_next_label(self.seglayer, self.unused_label)

    def removed_label(self, label):
        """ Label has been removed, update what depended on it """
        if self.unused_label is None:
            self.unused_label = self.get_free_label()
        #else:
        #    if label < self.unused_label:
        #        self.unused_label = label

    ######### Replace a label by another one, handle all dependencies
    def replace_label(self, old_label, new_label, check_new_label=True):
        """ Replace label by new one, update everything """
        ## if needed, check if the new label is present and change it if yes
        if check_new_label:
            if new_label in np.unique(self.seglayer.data):
                self.replace_label(new_label, np.max(self.seglayer.data+1, False))
        ## change the label by the new one
        mask = self.seglayer.data == old_label
        np.place(self.seglayer.data, mask, new_label)


   ################"" Check
    def check_cell(self, event):
        """ Mark cell as checked and remove suspect """
        tframe = ut.current_frame(self.viewer, self.epicure.dim)
        #suglayer = self.viewer.layers["Suggestion"]
        #ut.setCellValue(checklayer, self.seglayer, event, 1, tframe, tframe)
        #ut.setCellValue(suglayer, self.seglayer, event, 0, tframe, tframe)
        ## Exonerate suspects in that cell
        self.epicure.suspecting.exonerate_from_event(event)
        ## Branch options
        label = ut.getCellValue( self.seglayer, event ) 
        group = self.check_group.text()
        self.epicure.add_epicell( label, group )
        if "Checked" in self.viewer.layers:
            self.epicure.draw_update_epicell( label, group )
    
    def uncheck_cell(self, event):
        """ Mark cell as uncheck """
        #checklayer = self.viewer.layers["CheckMap"]
        tframe = ut.current_frame(self.viewer, self.epicure.dim)
        #ut.setCellValue(checklayer, self.seglayer, event, 0, tframe, tframe)
        ## Branch options
        label = ut.getCellValue( self.seglayer, event ) 
        self.epicure.remove_epicell( label )
        if "Checked" in self.viewer.layers:
            self.epicure.draw_update_epicell( label, 0 )
