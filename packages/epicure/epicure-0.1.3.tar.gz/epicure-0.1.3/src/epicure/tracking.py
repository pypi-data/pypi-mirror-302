from qtpy.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QLineEdit, QComboBox, QLabel, QSpinBox, QCheckBox
from napari import Viewer
import time
from napari.utils.notifications import show_info
from epicure.laptrack_centroids import LaptrackCentroids
from epicure.laptrack_overlaps import LaptrackOverlaps
from laptrack.data_conversion import convert_split_merge_df_to_napari_graph
from epicure.track_optical import trackOptical
import epicure.Utils as ut
from napari.utils import progress

import vispy.color
import pandas as pd
import numpy as np
from skimage.measure import regionprops, regionprops_table
from multiprocessing.pool import ThreadPool as Pool
from functools import partial
import networkx as nx

class Tracking(QWidget):
    """
        Handles tracking of cells, track operations with the Tracks layer
    """
    def __init__(self, napari_viewer, epic):
        super().__init__()
        self.viewer = napari_viewer
        self.epicure = epic
        self.graph = None      ## init 
        self.tracklayer = None      ## track layer with information (centroids, labels, tree..)
        self.track_data = None ## keep the updated data, and update the layer only from time to time (slow to do)
        self.tracklayer_name = "Tracks"  ## name of the layer containing tracks
        self.nframes = self.epicure.nframes
        self.properties = ["label", "centroid"]

        layout = QVBoxLayout()
        
        self.track_update = QPushButton("Update tracks", parent=self)
        layout.addWidget(self.track_update)
        self.track_update.clicked.connect(self.update_track_layer)
        
        ## Track only in one ROI
        #self.track_only_in_roi = QCheckBox(text="Only in ROI")
        #layout.addWidget(self.track_only_in_roi)
        #self.track_only_in_roi.setChecked(False)

        ## Method specific
        self.track_choice = QComboBox()
        layout.addWidget(self.track_choice)
        
        self.track_choice.addItem("Laptrack-Centroids")
        self.create_laptrack_centroids()
        layout.addWidget(self.gLapCentroids)
        
        self.track_choice.addItem("Laptrack-Overlaps")
        self.create_laptrack_overlap()
        layout.addWidget(self.gLapOverlap)
        
        self.track_go = QPushButton("Track", parent=self)
        layout.addWidget(self.track_go)
        self.setLayout(layout)
        self.track_go.clicked.connect(self.do_tracking)

        ## General tracking options
        self.frame_range = QCheckBox( text="Track only some frames" )
        self.frame_range.setChecked( False )
        self.frame_range.clicked.connect( self.show_frame_range )
        self.range_group = QGroupBox( "Frame range" )
        range_layout = QVBoxLayout()
        ntrack = QHBoxLayout()
        ntrack_lab = QLabel()
        ntrack_lab.setText("Track from frame:")
        ntrack.addWidget(ntrack_lab)
        self.start_frame = QSpinBox()
        self.start_frame.setMinimum(0)
        self.start_frame.setMaximum(self.nframes-1)
        self.start_frame.setSingleStep(1)
        self.start_frame.setValue(0)
        ntrack.addWidget(self.start_frame)
        range_layout.addLayout(ntrack)
        
        entrack = QHBoxLayout()
        entrack_lab = QLabel()
        entrack_lab.setText("Until frame:")
        entrack.addWidget(entrack_lab)
        self.end_frame = QSpinBox()
        self.end_frame.setMinimum(1)
        self.end_frame.setMaximum(self.nframes-1)
        self.end_frame.setSingleStep(1)
        self.end_frame.setValue(self.nframes-1)
        entrack.addWidget(self.end_frame)
        range_layout.addLayout(entrack)
        self.start_frame.valueChanged.connect( self.changed_start )
        self.end_frame.valueChanged.connect( self.changed_end )
        
        self.range_group.setLayout( range_layout )
        layout.addWidget( self.frame_range )
        layout.addWidget( self.range_group )
        
        self.show_frame_range()
        self.show_trackoptions()
        self.track_choice.currentIndexChanged.connect(self.show_trackoptions)

    def show_frame_range( self ):
        """ Show/Hide frame range options """
        self.range_group.setVisible( self.frame_range.isChecked() )
        
    ##########################################
    #### Tracks layer and function

    def reset( self ):
        """ Reset Tracks layer and data """
        self.graph = None
        self.track_data = None
        ut.remove_layer( self.viewer, "Tracks" )

    def init_tracks(self):
        """ Add a track layer with the new tracks """
        track_table, track_prop = self.create_tracks()
        
        ## plot tracks
        if len(track_table) > 0:
            self.viewer.add_tracks(
                track_table,
                graph=self.graph, 
                name=self.tracklayer_name,
                properties = track_prop,)
            self.viewer.layers[self.tracklayer_name].visible=True
            self.viewer.layers[self.tracklayer_name].color_by="track_id"
            ut.set_active_layer(self.viewer, "Segmentation")
            self.tracklayer = self.viewer.layers[self.tracklayer_name]
            self.track_data = self.tracklayer.data
            #self.track.display_id = True
            self.color_tracks_as_labels()

    def color_tracks_as_labels(self):
        """ Color the tracks the same as the label layer """
        ## must color it manually by getting the Label layer colors for each track_id
        cols = np.zeros((len(self.tracklayer.data[:,0]),4))
        for i, tr in enumerate(self.tracklayer.data[:,0]):
            cols[i] = (self.epicure.seglayer.get_color(tr))
        self.tracklayer._track_colors = cols
        self.tracklayer.events.color_by()

    def replace_tracks(self, track_df):
        """ Replace all tracks based on the dataframe """
        track_table, track_prop = self.build_tracks(track_df)
        self.tracklayer.data = track_table
        self.track_data = self.tracklayer.data
        self.tracklayer.properties = track_prop
        self.tracklayer.refresh()
        self.color_tracks_as_labels()

    def reset_tracks(self):
        """ Reset tracks and reload them from labels """
        ut.remove_layer(self.viewer, "Tracks")
        self.init_tracks()

    def update_track_layer(self):
        """ Update the track layer (slow) """
        self.viewer.window._status_bar._toggle_activity_dock(True)
        progress_bar = progress(total=1)
        progress_bar.set_description( "Updating track layer" )
        self.tracklayer.data = self.track_data
        progress_bar.close()
        self.color_tracks_as_labels()
        self.viewer.window._status_bar._toggle_activity_dock(False)
    

    def update_tracks(self, labels, refresh=True):
        """ Update the track infos of a few labels """
        print("DEPRECATED")
        if self.track_df is not None:
            ## remove them
            self.track_df = self.track_df.drop( self.track_df[self.track_df['label'].isin(labels)].index ) 
            ## and remeasure them
            seglabels = self.epicure.seg*np.isin(self.epicure.seg, labels)
            dflabels = self.measure_labels( seglabels )
            self.track_df = pd.concat( [self.track_df, dflabels] )
            ## update tracks
            if refresh:
                #self.graph = {}
                print("Graph of division/merges not updated, removed")
                if "Tracks" not in self.viewer.layers:
                    self.init_tracks()
                else:
                    #self.show_tracks()
                    self.viewer.layers["Tracks"].refresh()

    def measure_track_features(self, track_id):
        """ Measure features (length, total displacement...) of given track """
        features = {}
        track = self.get_track_data( track_id )
        start = int(np.min(track[:,1]))
        end = int(np.max(track[:,1]))
        features["Label"] = track_id
        features["TrackDuration"] = end - start + 1
        features["TrackStart"] = start
        features["TrackEnd"] = end
        if (end-start) == 0:
            ## only one frame
            features["TotalDisplacement"] = None
            features["NetDisplacement"] = None
            features["Straightness"] = None
        else:
            features["TotalDisplacement"] = ut.total_distance( track[:,2:4] )
            features["NetDisplacement"] = ut.net_distance( track[:,2:4] )
            if features["TotalDisplacement"] > 0:
                features["Straightness"] = features["NetDisplacement"]/features["TotalDisplacement"]
            else:
                features["Straightness"] = None
        return features

    def measure_features( self, track_id, features ):
        """ Measure features along all the track """
        mask = self.epicure.get_mask( track_id )
        res = {}
        for feat in features:
            res[feat] = []
        for frame in mask:
            props = regionprops( frame )
            if len(props) > 0:
                if "Area" in features:
                    res["Area"].append( props[0].area )
                if "Hull" in features:
                    res["Hull"].append( props[0].area_convex )
                if "Elongation" in features:
                    res["Elongation"].append( props[0].axis_major_length )
                if "Eccentricity" in features:
                    res["Eccentricity"].append( props[0].eccentricity )
                if "Perimeter" in features:
                    res["Perimeter"].append( props[0].perimeter )
                if "Solidity" in features:
                    res["Solidity"].append( props[0].solidity )
        return res

    def measure_specific_feature( self, track_id, featureName ):
        """ Measure some specific feature """
        if featureName == "Similarity":
            import skimage.metrics as imetrics
            movie = self.epicure.get_label_movie( track_id, extend=1.5 )
            sim_scores = []
            for i in range(0, len(movie)-1):
                score = imetrics.normalized_mutual_information( movie[i], movie[i+1] ) 
                sim_scores.append(score)
            return sim_scores

    def measure_labels(self, segimg):
        """ Get the dataframe of the labels in the segmented image """
        resdf = None
        for iframe, frame in progress(enumerate(segimg)):
            frame_table = self.get_one_frame( frame, iframe )
            if resdf is None:
                resdf = pd.DataFrame(frame_table)
            else:
                resdf = pd.concat([resdf, pd.DataFrame(frame_table)])
        return resdf

    def add_track_frame(self, label, frame, centroid, tree=None, group=None):
        """ Add one frame to the track """
        new_frame = np.array([label, frame, centroid[0], centroid[1]])
        self.track_data = np.vstack((self.track_data, new_frame))
            
    def get_track_list(self):
        """ Get list of unique track_ids """
        #return self.track._manager.unique_track_ids()
        return np.unique(self.track_data[:,0])

    def has_track(self, label):
        """ Test if track label is present """
        return label in self.track_data[:,0]
    
    def nb_points(self):
        """ Number of points in the tracks """
        return self.track_data.shape[0]

    def nb_tracks(self):
        """ Return number of tracks """
        #return self.track._manager.__len__()
        return len(self.get_track_list())

    def gaped_track(self, track_id):
        """ Check if there is a gap (missing frame) in a track """
        indexes = self.get_track_indexes(track_id)
        if len(indexes) <= 0:
            return False
        track_frames = self.track_data[indexes,1]
        return ((np.max(track_frames)-np.min(track_frames)+1) > len(track_frames) )

    def gap_frames(self, track_id):
        """ Returns the frame(s) at which the gap(s) are """
        min_frame, max_frame = self.get_extreme_frames( track_id )
        frame = min_frame
        indexes = self.get_track_indexes(track_id)
        track_frames = self.track_data[indexes,1]
        gaps = list(set(range(min_frame, max_frame+1, 1)) - set(track_frames))
        if len(gaps) > 0:
            gaps.sort()
        return gaps
            
    def check_gap(self, tracks=None, verbose=None):
        """ Check if there is a track with a gap, flag it if yes """
        if tracks is None:
            tracks = self.get_track_list()
        gaped = []
        for track in tracks:
            if self.gaped_track( track ):
                gaped.append(track)
        if verbose is None:
            verbose = self.epicure.verbose
        if verbose > 0 and len(gaped)>0:
            ut.show_warning("Gap in track(s) "+str(gaped)+"\n"
            +"Consider doing sanity_check in Editing onglet to fix it")
        return gaped

    def get_track_indexes(self, track_id):
        """ Get indexes of track_id tracks position in the arrays """
        if type(track_id) == int:
            return (np.argwhere( self.track_data[:,0] == track_id )).flatten()
        return (np.argwhere( np.isin( self.track_data[:,0], track_id ) )).flatten()

    def get_track_indexes_from_frame(self, track_id, frame):
        """ Get indexes of track_id tracks position in the arrays from the given frame """
        if type(track_id) == int:
            return (np.argwhere( (self.track_data[:,0] == track_id)*(self.track_data[:,1]>= frame) )).flatten()
        return (np.argwhere( np.isin( self.track_data[:,0], track_id )*(self.track_data[:,1]>= frame) )).flatten()

    def get_index(self, track_id, frame ):
        """ Get index of track_id at given frame """
        if np.isscalar(track_id):
            track_id = [track_id]
        return np.argwhere( (np.isin(self.track_data[:,0], track_id))*(self.track_data[:,1] == frame) )

    def get_small_tracks(self, max_length=1):
        """ Get tracks smaller than the given threshold """
        labels = []
        lengths = []
        positions = []
        for lab in self.get_track_list():
            indexes = self.get_track_indexes(lab)
            length = len(indexes)
            if length <= max_length:
                pos = self.mean_position( indexes, only_first=False )
                labels.append(lab)
                lengths.append(length)
                positions.append(pos)
        return labels, lengths, positions

    def get_track_data(self, track_id):
        """ Return the data of track track_id """
        indexes = self.get_track_indexes( track_id )
        track = self.track_data[indexes,]
        return track

    def get_frame_data( self, track_id, ind ):
        """ Get ind-th data of track track_id """
        track = self.get_track_data( track_id )
        return track[ind]

    def mean_position(self, indexes, only_first=False):
        """ Mean positions of tracks at indexes """
        if len(indexes) <= 0:
            return None
        track = self.track_data[indexes,]
        ## keep only the first frame of the tracks
        if only_first:
            min_frame = np.min(track[:,1])
            track = track[track[:,1]==min_frame,]
        return ( int(np.mean(track[:,1])), int(np.mean(track[:,2])), int(np.mean(track[:,3])) )

    def get_first_frame(self, track_id):
        """ Returns first frame where track_id is present """
        track = self.get_track_data( track_id )
        if len(track) <= 0:
            return None
        return int(np.min(track[:,1]))
    
    def get_last_frame(self, track_id):
        """ Returns last frame where track_id is present """
        track = self.get_track_data( track_id )
        return int(np.max(track[:,1]))
    
    def get_extreme_frames(self, track_id):
        """ Returns the first and last frames where track_id is present """
        track = self.get_track_data( track_id )
        if track.shape[0] > 0:
            return (int(np.min(track[:,1])), int(np.max(track[:,1])) )
        return None, None

    def get_mean_position(self, track_id, only_first=False):
        """ Get mean position of the track """
        indexes = self.get_track_indexes( track_id )
        return self.mean_position( indexes, only_first )

    def update_centroid(self, track_id, frame, ind=None, cx=None, cy=None):
        """ Update track at given frame """
        if ind is None:
            ind = self.get_track_indexes( track_id )
        if len(ind) > 1:
            if self.epicure.verbose > 1:
                print(ind)
                print("Weird")
        if cx is None:
            prop = ut.getPropLabel( self.epicure.seg[frame], track_id )
            self.track_data[ind, 2:4] = prop.centroid[1]
        else:
            self.track_data[ind, 2] = cx
            self.track_data[ind, 3] = cy

    def swap_frame_id(self, tid, otid, frame):
        """ Swap the ids of two tracks at frame """
        ind = int(self.get_index(tid, frame))
        oind = int(self.get_index(otid, frame))
        ## check if one of the label is an extreme of a track and potentially in the graph
        for track_index in [tid, otid]:
            min_frame, max_frame = self.get_extreme_frames( track_index )
            if (min_frame == frame) or (max_frame == frame):
                self.update_graph( track_index, frame )
        self.track_data[[ind, oind],0] = [otid, tid]


    def update_track_on_frame(self, track_ids, frame):
        """ Update (add or modify) tracks at given frame """
        frame_table = regionprops_table(np.where(np.isin(self.epicure.seg[frame], track_ids), self.epicure.seg[frame], 0), properties=self.properties)
        for i, tid in enumerate(frame_table["label"]):
            index = self.get_index(tid, frame)
            if len(index) > 0:
                self.update_centroid( tid, frame, index, int(frame_table["centroid-0"][i]), int(frame_table["centroid-1"][i]) )
            else:
                cur_cell = np.array( [tid, frame, int(frame_table["centroid-0"][i]), int(frame_table["centroid-1"][i])] )
                cur_cell = np.expand_dims(cur_cell, axis=0)
                self.track_data = np.append(self.track_data, cur_cell, axis=0)
    
    def add_one_frame(self, track_ids, frame, refresh=True):
        """ Add one frame from track """
        for tid in track_ids:
            frame_table = regionprops_table(np.uint8(self.epicure.seg[frame]==tid), properties=self.properties)
            cur_cell = np.array( [tid, frame, int(frame_table["centroid-0"]), int(frame_table["centroid-1"])], dtype=np.uint32 )
            cur_cell = np.expand_dims(cur_cell, axis=0)
            self.track_data = np.append(self.track_data, cur_cell, axis=0)

    def remove_one_frame(self, track_id, frame, handle_gaps=True, refresh=True):
        """ 
        Remove one frame from track(s) 
        """
        inds = self.get_index( track_id, frame )
        if np.isscalar(track_id):
            track_id = [track_id]
        check_for_gaps = False
        for tid in track_id:
            ## removed frame is in the extremity of a track, can be in the graph
            first_frame, last_frame = self.get_extreme_frames( tid )
            if first_frame is None:
                continue
            if (first_frame == frame) or (last_frame == frame):
                self.update_graph( tid, frame )
            else:
                check_for_gaps = True
        self.track_data = np.delete(self.track_data, inds, axis=0)
        ## gaps might have been created in the tracks, for now doesn't allow it so split the tracks
        if handle_gaps and check_for_gaps:
            gaped = self.check_gap( track_id, verbose=0 )
            if len(gaped) > 0:
                self.epicure.fix_gaps(gaped)
        
    def get_current_value(self, track_id, frame):
        ind = self.get_index( track_id, frame )
        centx = int(self.track_data[ind, 2])
        centy = int(self.track_data[ind, 3])
        return self.epicure.seg[frame, centx, centy]

    def update_graph(self, track_id, frame):
        """ Update graph if deleted label was linked at that frame, assume keys are unique """
        start_time = time.time()
        if self.graph is not None:
            ## handles current node is last of his branch
            parents = self.last_in_graph( track_id, frame )
            if len(parents) > 0:
                current_label = self.get_current_value( track_id, frame )
                if current_label == 0:
                    for parent in parents:
                        del self.graph[parent]
                else:
                    for parent in parents:
                        self.update_child( parent, track_id, current_label )
            ## handles when current track is first frame of a division
            if self.first_in_graph( track_id, frame ):
                current_label = self.get_current_value( track_id, frame )
                if current_label == 0:
                    del self.graph[track_id]
                else:
                    self.update_key( track_id, current_label ) 
        if self.epicure.verbose > 1:
            ut.show_duration( start_time, header="Graph updated in " )

    def update_child(self, parent, prev_key, new_key):
        """ Change the value of a key in the graph """
        vals = self.graph[parent]
        self.graph[parent] = []
        for val in vals:
            if val == prev_key:
                self.graph[parent].append(new_key)
            else:
                self.graph[parent].append(val)

    def update_key(self, prev_key, new_key):
        """ Change the value of a key in the graph """
        self.graph[new_key] = self.graph.pop(prev_key)

    def last_in_graph(self, track_id, frame):
        """ Check if given label and frame is the last of a branch, in the graph """
        parents = []
        for key, vals in self.graph.items():
            for val in vals:
                if val == track_id:
                    last_frame = self.get_last_frame( val )
                    if last_frame == frame:
                        parents.append(key)
        return parents

    def first_in_graph(self, track_id, frame):
        """ Check if the given label and frame is the first in the branch so the node in the graph """
        if track_id in self.graph.keys():
            first_frame = self.get_first_frame(track_id)
            if first_frame == frame:
                return True
        return False

    def remove_tracks(self, track_ids):
        """ Remove track with given id """
        inds = self.get_track_indexes(track_ids)
        self.track_data = np.delete(self.track_data, inds, axis=0)
       
    def build_tracks(self, track_df):
        """ Create tracks from dataframe (after tracking) """
        track = track_df[["track_id", "frame", "centroid-0", "centroid-1"]]
        #frame_prop = frame_table[["tree_id", "label", "nframes", "group"]]
        return np.array(track, int), None #dict(frame_prop)

    def create_tracks(self):
        """ Create tracks from labels (without tracking) """
        properties = ['label', 'centroid']
        track_table = np.empty((0,4), int)
        if self.epicure.nframes >= 0:
            for iframe, frame in progress(enumerate(self.epicure.seg)):
                frame_track, frame_prop = self.get_one_frame( frame, iframe )
                track_table = np.vstack((track_table, frame_track))
        
        return track_table, None # track_prop

    def add_track_features(self, labels):
        """ Add features specific to tracks (eg nframes) """
        nframes = np.zeros(len(labels), int)
        if self.epicure.verbose > 1:
            print("REPLACE BY COUNT METHOD")
        for track_id in np.unique(labels):
            cur_track = np.argwhere(labels == track_id)
            nframes[ list(cur_track) ] = len(cur_track)
        return nframes
    
    def get_one_frame(self, seg, frame):
        """ Get the regionprops results into the dataframe """
        frame_table = regionprops_table(seg, properties=self.properties)
        ndata = len(frame_table["label"])
        if frame is not None:
            frame_table["frame"] = np.repeat(frame, ndata)
        frame_table["track_id"] = frame_table["label"]
        #frame_table["tree_id"] = [0]*ndata    ##### @Tochange to read div/merge infos ?
        #frame_table["group"] = [0]*ndata    ##### @Tochange to read div/merge infos ?
        #frame_table["nframes"] = [0]*ndata
        frame_table = pd.DataFrame(frame_table)
        frame_track = frame_table[["track_id", "frame", "centroid-0", "centroid-1"]]
        #frame_prop = frame_table[["tree_id", "label", "nframes", "group"]]
        return np.array(frame_track, int), None #dict(frame_prop)


    ##########################################
    #### Tracking functions

    def changed_start(self, i):
        """ Ensures that end frame > start frame """
        if i > self.end_frame.value():
            self.end_frame.setValue(i+1)

    def changed_end(self, i):
        if i < self.start_frame.value():
            self.start_frame.setValue(i-1)

    def find_parents(self, labels, twoframes):
        """ Find in the first frame the parents of labels from second frame """
        
        if self.track_choice.currentText() == "Laptrack-Centroids":
            return self.laptrack_centroids_twoframes(labels, twoframes)
        
        if self.track_choice.currentText() == "Laptrack-Overlaps":
            return self.laptrack_overlaps_twoframes(labels, twoframes)
        
        if self.track_choice.currentText() == "Optictrack":
            if self.epicure.verbose > 1:
                print("Merge propagation with Optitrack not implemented yet")
            return [None]*len(labels)

    def do_tracking(self):
        """ Start the tracking with the selected options """
        if self.frame_range.isChecked():
            start = self.start_frame.value()
            end = self.end_frame.value()
        else:
            start = 0
            end = self.nframes-1
        start_time = time.time()
        self.viewer.window._status_bar._toggle_activity_dock(True)
        self.epicure.suspecting.reset_all_suspects()
        
        if self.track_choice.currentText() == "Laptrack-Centroids":
            if self.epicure.verbose > 1:
                print("Starting track with Laptrack-Centroids")
            self.laptrack_centroids( start, end )
            self.epicure.tracked = 1
        if self.track_choice.currentText() == "Laptrack-Overlaps":
            if self.epicure.verbose > 1:
                print("Starting track with Laptrack-Centroids")
            self.laptrack_overlaps( start, end )
            self.epicure.tracked = 1
        if self.track_choice.currentText() == "Optictrack":
            self.optic_track(start, end )
            self.epicure.tracked = 2
        
        self.epicure.finish_update(contour=2)
        #self.epicure.reset_free_label()
        self.viewer.window._status_bar._toggle_activity_dock(False)
        if self.epicure.verbose > 0:
            ut.show_duration( start_time, header="Tracking done in " )

    def show_trackoptions(self):
        self.gLapCentroids.setVisible(self.track_choice.currentText() == "Laptrack-Centroids")
        self.gLapOverlap.setVisible(self.track_choice.currentText() == "Laptrack-Overlaps")
        #self.gOptic.setVisible(self.track_choice.currentText() == "Optictrack")

    def relabel_nonunique_labels(self, track_df):
        """ After tracking, some track can be splitted and get same label, fix that """
        inittids = np.unique(track_df["track_id"])
        labtracks = []
        saved_data = np.copy(self.epicure.seglayer.data)
        mframes = []
        tids = []
        used = np.unique( saved_data )
        all_labels = np.unique(track_df["label"])
        for tid in inittids:
            cdf = track_df[track_df["track_id"]==tid]
            #print(cdf)
            min_frame = np.min( cdf["frame"] )
            #labtrack = int( cdf["label"][cdf["frame"]==min_frame] )
            for lab in np.unique(cdf["label"]):
                labtracks.append(lab)
                mframes.append( min_frame )
                tids.append(tid)
        if len(labtracks) != len(np.unique(labtracks)):
            ## some labels are present several times
            used = used.tolist()
            for lab in all_labels :
                indexes = list(np.where(np.array(labtracks)==lab)[0])
                if len(indexes)>1:
                    minframes = [mframes[indy] for indy in range(len(labtracks)) if labtracks[indy]==lab]
                    indmin = indexes[ np.argmin( minframes ) ]
                    ## for the other(s), change the label
                    newvals = ut.get_free_labels( used, len(indexes) )
                    used = used + newvals
                    for i, ind in enumerate(indexes):
                        if ind != indmin:
                            tid = tids[ind]
                            newval = newvals[i]
                            track_df.loc[ (track_df["track_id"]==tid)  & (track_df["label"]==lab) , "label"] = newval
                            for frame in track_df["frame"][(track_df["track_id"]==tid) & (track_df["label"]==newval)]:
                                mask = (saved_data[frame]==lab)
                                self.epicure.seglayer.data[frame][mask] = newval
        

    def relabel_trackids(self, track_df, splitdf, mergedf):
        """ Change the trackids to take the first label of each track """
        replace_map = dict()
        new_trackids = track_df['track_id'].copy() 
        new_splitdf = splitdf.copy()
        new_mergedf = mergedf.copy()
        for tid in np.unique(track_df['track_id']):
            ctrack_df = track_df[track_df['track_id']==tid]
            newval = ctrack_df["label"][ctrack_df["frame"]==np.min(ctrack_df["frame"])]
            ## have to replace if different
            if tid != int(newval):
                newval = int(newval)
                toreplace = track_df['track_id']==tid
                new_trackids[toreplace] = newval
                if not new_splitdf.empty:
                    new_splitdf["parent_track_id"][splitdf["parent_track_id"]==tid] = newval
                    new_splitdf["child_track_id"][splitdf["child_track_id"]==tid] = newval
                if not new_mergedf.empty:
                    new_mergedf["parent_track_id"][ mergedf["parent_track_id"]==tid ] = newval
                    new_mergedf["child_track_id"][ mergedf["child_track_id"]==tid ] = newval
        return new_trackids, new_splitdf, new_mergedf

    def change_labels(self, track_df):
        """ Change the labels at each frame according to tracks """
        frames = track_df["frame"]
        ## change the other ones
        for frame in np.unique(frames):
            self.change_frame_labels(frame, track_df)

    def change_frame_labels(self, frame, track_df):
        """ Change the labels at given frame according to tracks """
        frame_df = track_df[track_df["frame"]==frame]
        #coordinates = frame_df[['centroid-0', 'centroid-1']].astype(int).values
        track_ids = frame_df['track_id'].astype(int).values
        old_labels = frame_df["label"].astype(int).values
        seglayer = np.copy(self.epicure.seglayer.data[frame])
        for i, lab in enumerate(old_labels):
            mask = (seglayer==lab)
            self.epicure.seglayer.data[frame][mask] = track_ids[i]

    def label_to_dataframe( self, labimg, frame ):
        """ from label, get dataframe of centroids with properties """
        df = pd.DataFrame(regionprops_table(labimg, properties=self.region_properties))
        df["frame"] = frame
        return df
    
    def labels_to_centroids(self, start_frame, end_frame, locked=True):
        """ Get centroids of each cell in dataframe """
        regionprops = []
        #if self.epicure.process_parallel:
        #    with Pool(self.epicure.nparallel) as pool:
        #        regionprops = pool.map( self.label_frame_todf, range(start_frame, end_frame+1) )
        #    regionprops_df = pd.concat(regionprops)
        #else:
        for frame in range(start_frame, end_frame+1):
            df = self.label_frame_todf(frame)
            regionprops.append(df)
        regionprops_df = pd.concat(regionprops)
        return regionprops_df
    
    def labels_ready(self, start_frame, end_frame, locked=True):
        """ Get labels of unlocked cells to track """
        res_labels = []
        if self.epicure.process_parallel:
            with Pool(self.epicure.nparallel) as pool:
                labels = pool.map( self.current_label_frame, range(start_frame, end_frame+1) )
            res_labels = np.array(labels)
        else:
            for frame in range(start_frame, end_frame+1):
                labels = self.current_label_frame(frame)
                res_labels.append(labels)
            res_labels = np.array(res_labels)
        return res_labels
    
    def label_frame_todf( self, frame ):
        """ For current frame, get label frame image then dataframe of centroids """
        clabel = self.current_label_frame(frame)
        return self.label_to_dataframe( clabel, frame )
    
    def current_label_frame( self, frame ):
        """ For current frame, get label frame image """
        clabel = None
        #if self.track_only_in_roi.isChecked():
        #    clabel = self.epicure.only_current_roi(frame)
        if clabel is None:
            clabel = self.epicure.seg[frame]
        return clabel

    def after_tracking(self, track_df, split_df, merge_df, progress_bar, indprogress):
        """ Steps after tracking: get/show the graph from the track_df """
        graph = None
        progress_bar.set_description( "Update labels and tracks" )
        ## shift all by 1 so that doesn't start at 0
        if len(split_df) > 0:
            split_df[["parent_track_id"]] += 1
            split_df[["child_track_id"]] += 1
        if len(merge_df) > 0:
            merge_df[["parent_track_id"]] += 1
            merge_df[["child_track_id"]] += 1
        track_df[["track_id"]] += 1
       
        ## relabel if some track have the same label
        self.relabel_nonunique_labels(track_df)
        ## relabel track ids so that they are equal to the first label of the track
        newtids, split_df, merge_df = self.relabel_trackids(track_df, split_df, merge_df)
        track_df["track_id"] = newtids
        self.change_labels(track_df)

        # create graph of division/merging
        self.graph = convert_split_merge_df_to_napari_graph(split_df, merge_df)

        progress_bar.update(indprogress+1)
        
        ## update display if active
        self.replace_tracks(track_df)

        progress_bar.update(indprogress+2)
        ## update the list of suspects ?
        #self.epicure.update_epicells()
        return graph


    
############ Laptrack centroids option
    
    def create_laptrack_centroids(self):
        """ GUI of the laptrack option """
        self.gLapCentroids = QGroupBox("Laptrack-Centroids")
        glap_layout = QVBoxLayout()
        mdist = QHBoxLayout()
        mdist_lab = QLabel()
        mdist_lab.setText("Max distance")
        mdist.addWidget(mdist_lab)
        self.max_dist = QLineEdit()
        self.max_dist.setText("15.0")
        mdist.addWidget(self.max_dist)
        glap_layout.addLayout(mdist)
        ## splitting ~ cell division
        scost = QHBoxLayout()
        scost_lab = QLabel()
        scost_lab.setText("Splitting cutoff")
        scost.addWidget(scost_lab)
        self.splitting_cost = QLineEdit()
        self.splitting_cost.setText("1")
        scost.addWidget(self.splitting_cost)
        glap_layout.addLayout(scost)
        ## merging ~ error ?
        mcost = QHBoxLayout()
        mcost_lab = QLabel()
        mcost_lab.setText("Merging cutoff")
        mcost.addWidget(mcost_lab)
        self.merging_cost = QLineEdit()
        self.merging_cost.setText("1")
        mcost.addWidget(self.merging_cost)
        glap_layout.addLayout(mcost)

        self.check_penalties = QCheckBox(text="Add features cost")
        glap_layout.addWidget(self.check_penalties)
        self.create_penalties()
        glap_layout.addWidget(self.bpenalties)
        self.check_penalties.setChecked(True)
        self.check_penalties.stateChanged.connect(self.show_penalties)
        self.gLapCentroids.setLayout(glap_layout)

    def show_penalties(self):
        self.bpenalties.setVisible(not self.bpenalties.isVisible())

    def create_penalties(self):
        self.bpenalties = QGroupBox("Features cost")
        pen_layout = QVBoxLayout()
        areaCost = QHBoxLayout()
        penarea_lab = QLabel()
        penarea_lab.setText("Area difference:")
        self.area_cost = QLineEdit()
        self.area_cost.setText("2")
        areaCost.addWidget(penarea_lab)
        areaCost.addWidget(self.area_cost)
        pen_layout.addLayout(areaCost)
        solidCost = QHBoxLayout()
        pensol_lab = QLabel()
        pensol_lab.setText("Solidity difference:")
        self.solidity_cost = QLineEdit()
        self.solidity_cost.setText("0")
        solidCost.addWidget(pensol_lab)
        solidCost.addWidget(self.solidity_cost)
        pen_layout.addLayout(solidCost)
        self.bpenalties.setLayout(pen_layout)

    def laptrack_centroids_twoframes(self, labels, twoframes):
        """ Perform tracking of two frames with current parameters """
        laptrack = LaptrackCentroids(self, self.epicure)
        laptrack.max_distance = float(self.max_dist.text())
        self.region_properties = ["label", "centroid"]
        if self.check_penalties.isChecked():
            self.region_properties.append("area")
            self.region_properties.append("solidity")
            laptrack.penal_area = float(self.area_cost.text())
            laptrack.penal_solidity = float(self.solidity_cost.text())
        laptrack.set_region_properties(with_extra=self.check_penalties.isChecked())
            
        df = self.twoframes_centroid(twoframes)
        if set(np.unique(df["label"])) == set(labels):
            ## no other labels
            return [None]*len(labels) 
        laptrack.splitting_cost = False ## disable splitting option
        laptrack.merging_cost = False ## disable merging option
        parent_labels = laptrack.twoframes_track(df, labels)
        return parent_labels
    
    def twoframes_centroid(self, img):
        """ Get centroids of first frame only """
        df0 = self.label_to_dataframe( img[0], 0 )
        df1 = self.label_to_dataframe( img[1], 1 )
        return pd.concat([df0, df1])
    
    def laptrack_centroids(self, start, end):
        """ Perform track with laptrack option and chosen parameters """
        ## Laptrack tracker
        laptrack = LaptrackCentroids(self, self.epicure)
        laptrack.max_distance = float(self.max_dist.text())
        laptrack.splitting_cost = float(self.splitting_cost.text())
        laptrack.merging_cost = float(self.merging_cost.text())
        self.region_properties = ["label", "centroid"]
        if self.check_penalties.isChecked():
            self.region_properties.append("area")
            self.region_properties.append("solidity")
            laptrack.penal_area = float(self.area_cost.text())
            laptrack.penal_solidity = float(self.solidity_cost.text())
        laptrack.set_region_properties(with_extra=self.check_penalties.isChecked())

        progress_bar = progress(total=5)
        progress_bar.set_description( "Prepare tracking" )
        if self.epicure.verbose > 1:
            print("Convert labels to centroids: use track info ?")
        df = self.labels_to_centroids(start, end, locked=True)
        progress_bar.update(1)
        if self.epicure.verbose > 1:
            print("GO tracking")
        progress_bar.set_description( "Do tracking with LapTrack Centroids" )
        track_df, split_df, merge_df = laptrack.track_centroids(df)
        progress_bar.update(2)
        if self.epicure.verbose > 1:
            print("After tracking, update everything")
        self.after_tracking(track_df, split_df, merge_df, progress_bar, 2)
        progress_bar.update(5)
        progress_bar.close()
    
############ Laptrack overlap option

    def create_laptrack_overlap(self):
        """ GUI of the laptrack overlap option """
        self.gLapOverlap = QGroupBox("Laptrack-Overlaps")
        glap_layout = QVBoxLayout()
        miou = QHBoxLayout()
        miou_lab = QLabel()
        miou_lab.setText("Min IOU")
        miou.addWidget(miou_lab)
        self.min_iou = QLineEdit()
        self.min_iou.setText("0.1")
        miou.addWidget(self.min_iou)
        glap_layout.addLayout(miou)
        
        scost = QHBoxLayout()
        scost_lab = QLabel()
        scost_lab.setText("Splitting cost")
        scost.addWidget(scost_lab)
        self.split_cost = QLineEdit()
        self.split_cost.setText("0.2")
        scost.addWidget(self.split_cost)
        glap_layout.addLayout(scost)
        
        mcost = QHBoxLayout()
        mcost_lab = QLabel()
        mcost_lab.setText("Merging cost")
        mcost.addWidget(mcost_lab)
        self.merg_cost = QLineEdit()
        self.merg_cost.setText("0.2")
        mcost.addWidget(self.merg_cost)
        glap_layout.addLayout(mcost)

        self.gLapOverlap.setLayout(glap_layout)

    def laptrack_overlaps(self, start, end):
        """ Perform track with laptrack overlap option and chosen parameters """
        ## Laptrack tracker
        laptrack = LaptrackOverlaps(self, self.epicure)
        miniou = float(self.min_iou.text())
        if miniou >= 1.0:
            miniou = 1.0
        laptrack.cost_cutoff = 1.0 - miniou
        laptrack.splitting_cost = float(self.split_cost.text())
        laptrack.merging_cost = float(self.merg_cost.text())
        self.region_properties = ["label", "centroid"]

        progress_bar = progress(total=6)
        progress_bar.set_description( "Prepare tracking" )
        labels = self.labels_ready(start, end, locked=True)
        progress_bar.update(1)
        progress_bar.set_description( "Do tracking with LapTrack Overlaps" )
        track_df, split_df, merge_df = laptrack.track_overlaps(labels)
        progress_bar.update(2)
        
        ## get dataframe of coordinates to create the graph 
        df = self.labels_to_centroids(start, end, locked=True)
        progress_bar.update(3)
        coordinate_df = df.set_index(["frame", "label"])
        tdf = track_df.set_index(["frame", "label"])
        track_df2 = pd.merge( tdf, coordinate_df, right_index=True, left_index=True).reset_index()
        self.after_tracking(track_df2, split_df, merge_df, progress_bar, 3)
        progress_bar.update(6)
        progress_bar.close()
    
    def laptrack_overlaps_twoframes(self, labels, twoframes):
        """ Perform tracking of two frames with current parameters """
        laptrack = LaptrackOverlaps(self, self.epicure)
        miniou = float(self.min_iou.text())
        if miniou >= 1.0:
            miniou = 1.0
        laptrack.cost_cutoff = 1.0 - miniou
        self.region_properties = ["label", "centroid"]

        laptrack.splitting_cost = False ## disable splitting option
        laptrack.merging_cost = False ## disable merging option
        parent_labels = laptrack.twoframes_track(twoframes, labels)
        return parent_labels

    def create_optictrack(self):
        """ GUI of the Optical track option """
        self.gOptic = QGroupBox("Optictrack")
        gOptic_layout = QVBoxLayout()
        miou = QHBoxLayout()
        miou_lab = QLabel()
        miou_lab.setText("Min IOU")
        miou.addWidget(miou_lab)
        self.min_iou = QLineEdit()
        self.min_iou.setText("0.25")
        miou.addWidget(self.min_iou)
        gOptic_layout.addLayout(miou)
        rad = QHBoxLayout()
        rad_lab = QLabel()
        rad_lab.setText("Flow radius")
        rad.addWidget(rad_lab)
        self.rad = QLineEdit()
        self.rad.setText("10")
        rad.addWidget(self.rad)
        gOptic_layout.addLayout(rad)
        self.show_opticed = QCheckBox("Show flowed segmentation")
        self.show_opticed.setChecked(False)
        gOptic_layout.addWidget(self.show_opticed)
        self.gOptic.setLayout(gOptic_layout)

    def optic_track(self, start, end):
        """ Perform track with optical flow registration + best match """
        optic = trackOptical(self, self.epicure)
        miniou = float(self.min_iou.text())
        radius = float(self.rad.text())
        opticed = self.show_opticed.isChecked()
        optic.set_parameters(miniou, radius, opticed)
        optic.track_by_optical_flow( self.viewer, start, end )

