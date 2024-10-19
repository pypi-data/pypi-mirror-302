import numpy as np
import epicure.Utils as ut
from skimage.measure import regionprops, regionprops_table
import pandas as pand

""" 
Cell object (several frames)
"""

class EpiCell():
    """
        Contains informations about a cell (branch)
        Cell is checked section of the track of the same cell without division 
        It must have a label which is the label in the segmentation layer
        Can be assigned to a group "checked" or other type
        Checked means that it cannot be modified, out of the computations
    """

    def __init__(self, epicure):
        self.label = None
        self.bbox = None
        self.epicure = epicure
        self.group = None
        self.locked = False
        self.trackid = None
        self.cells = None
        #self.cells = {}

    def lock(self, lock=True):
        """ Lock/Unlock the cell (cannot be modified) """
        self.locked = lock

    def set_label(self, label):
        """ Set the cell label """
        self.label = label

    def set_bounds(self, bbox=None):
        """ Set/update the bounding infos of the cell """
        if bbox is not None:
            self.bbox = np.array(bbox)
        else:
            self.bbox = ut.getBBoxLabel( self.epicure.seg, self.label)

    def remove_one_frame(self, frame):
        """ Cell deleted on one frame """
        ## 2D image
        if frame is None:
            self.epicure.delete_epicell(self.label)
            return 1
        ## Delete if first frame of the epicell
        if frame == self.bbox[0]:
            self.bbox[0] += 1
            ## check if cell has been totally removed
            if self.bbox[0] >= self.bbox[3]:
                self.epicure.delete_epicell(self.label)
            return 1
        ## Delete if last frame of the epicell
        if frame == (self.bbox[3]-1):
            self.bbox[3] -= 1
            ## check if cell has been totally removed
            if self.bbox[0] >= self.bbox[3]:
                self.epicure.delete_epicell(self.label)
            return 1
        ut.show_error("Problem with the cell "+str(self.label))
        return -1

    def add_one_frame(self, frame, bbox=None):
        """ Add one frame to current epicell """
        if frame < self.bbox[0]:
            if frame < (self.bbox[0]-1):
                print("Non consecutive addition of label, sure ?")
            self.bbox[0] = frame
        if frame > self.bbox[self.epicure.dim]:
            if frame > (self.bbox[self.epicure.dim]+1):
                print("Non consecutive addition of label, sure ?")
            self.bbox[self.epicure.dim] = frame+1
        self.set_xy_bbox(bbox)

    def set_xy_bbox(self, frame, bbox=None):
        """ Set or update the xy sizes of the bounding box """
        if bbox is not None:
            d3 = 1*(self.epicure.dim==3)
            for i in range(2):
                self.bbox[d3+i] = bbox[i]
                self.bbox[self.epicure.dim+d3+i] = bbox[2+i]
        else:
            self.set_bounds() 

    def update_xy_bbox(self, bbox=None, img=None):
        """ Update the x,y sizes of the bounding box """
        d3 = 1*( self.epicure.dim == 3 )
        if bbox is None:
            bbox = ut.getBBoxLabel( img, self.label )
        ## update it with current bbox
        for i in range(2):
            self.bbox[d3+i] = min(self.bbox[d3+i], bbox[i])
            self.bbox[self.epicure.dim+d3+i] = max(self.bbox[self.epicure.dim+d3+i], bbox[2+i])

    def check_epicell(self, label, bbox):
        """ Check that infos in the epicell are correct """
        if self.label != label:
            print("Cell "+str(label)+" does not match epicell "+str(self.label))
            return False
        for i in range(self.epicure.dim*2):
            if self.bbox[i] != bbox[i]:
                print("Cell "+str(self.label)+" bounding box wrong")
                return False
        return True
    

    def measure_epicell(self):
        """ Measure the cell from its label """
        cellimg = np.uint8(self.epicure.seg == label)
        if self.epicure.dim == 3:
            for t, timg in enumerate(cellimg):
                if np.sum(timg) > 0:
                    intimg = self.epicure.img[t]
                    self.cells_of_frame(t, timg, intimg)
        else:
            intimg = self.epicure.img
            self.cells_of_frame(0, self.epicure.seg, intimg)
    
    def cells_of_frame(self, t, frameimg, intimg):
        """ Create all the cells (labels) of given frame """
        properties = ["label", "area", "area_convex", "axis_major_length", "axis_minor_length", "centroid", "eccentricity", "orientation", "perimeter", "solidity"]
        frame_table = pand.DataFrame(regionprops_table(frameimg, intensity_image=intimg, properties=properties))
        self.cells[t] = []
        for ind in range(frame_table.shape[0]):
            if frame_table["label"][ind] > 0:
                cell_measures = {}
                for mes in frame_table.keys():
                    cell_measures[mes] = frame_table[mes][ind]
                cell_measures["group"] = self.group
                self.cells[t].append(cell_measures)
   
    def write_epicell(self):
        """ Output the cell to file """
        return str(self.group)+"-"+str(self.label)

    def show_epicell(self):
        """ Print infos about the cell """
        print("Epicell label "+str(self.label))
        print("Bounding box: ")
        print(self.bbox)

    def to_track(self):
        df = pand.DataFrame()
        ## see how to create to track object
        for frame, cell in self.cells.items():
            print(cell)
            #df["frame"].append(frame)

    def add_cell(self, epicell):
        """ add the cell object to the branch """
        self.cells.append(epicell)
