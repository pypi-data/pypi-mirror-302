
    ########## Suggestion functions 
    def init_suggestion(self):
        """ Initialize the layer that will contains propostion of tracks/segmentations """
        #suggestion = np.zeros(self.imgshape, dtype="uint16")
        #self.suggestion = self.viewer.add_labels(suggestion, blending="additive", name="Suggestion")
        self.suggestion = None
        
        @self.seglayer.mouse_drag_callbacks.append
        def click(layer, event):
            if event.type == "mouse_press":
                if 'Alt' in event.modifiers:
                    if event.button == 1:
                        pos = event.position
                        # alt+left click accept suggestion under the mouse pointer (in all frames)
                        self.accept_suggestion(pos)
    
    def locked_checked(self):
        return (("CheckMap" in self.viewer.layers) and (self.editing.lock_checked.isChecked()) )

    def reset_suggestion(self):
        """ erase all suggestions """
        self.suggestion.data = np.zeros(self.imgshape, dtype="uint16")

    def accept_suggestion(self, pos):
        """ Accept the modifications of the label at position pos (all the label) """
        #seglayer = self.viewer.layers["Segmentation"]
        label = self.suggestion.data[tuple(map(int, pos))]
        if label > 0:
            found = self.suggestion.data==label
            self.suspecting.exonerate( found, self.seglayer ) 
            indices = np.argwhere( found )
            ut.setNewLabel( self.seglayer, indices, label, add_frame=None )
            self.suggestion.data[self.suggestion.data==label] = 0
            self.suggestion.refresh()
    
    def add_suggestion(self, label, new_label):
        self.suggestion.data[self.seglayer.data == label] = new_label


        ### In tracking
        self.suggesting = False


        #self.check_suggestion = QCheckBox(text="Suggest corrections")
        #layout.addWidget(self.check_suggestion)
        #self.check_suggestion.stateChanged.connect( self.checked_suggestion )
        #self.checked_suggestion()
        #self.check_suggestion.setChecked(False)
    def checked_suggestion(self):
        self.suggesting = self.check_suggestion.isChecked()
       ut.set_visibility(self.viewer, "Suggestion", self.suggesting)
